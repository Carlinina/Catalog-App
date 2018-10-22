from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash

from sqlalchemy import create_engine, asc, desc, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from pprint import pprint

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///sportscatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/logout')
def showLogout():
    # return "The current session state is %s" % login_session['state']
    return render_template('logout.html')


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response
        (json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['email']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # See if a user exists, if it doesn't make a new one
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    # print login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/\
            revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if login_session.get('access_token'):
        del login_session['access_token']
    if login_session.get('gplus_id'):
        del login_session['gplus_id']
    if login_session.get('username'):
        del login_session['username']
    if login_session.get('email'):
        del login_session['email']
    if login_session.get('picture'):
        del login_session['picture']
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps
                                 ('Failed to revoke token for given user.',
                                  400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Catalog Information
@app.route('/catalog.json')
def showCategoriesJSON():
    engine = create_engine('sqlite:///sportscatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).order_by(asc(Category.id))
    listJson = []
    for category in categories:
        cat = category.serialize
        listItems = session.query(Item).filter_by(category=category)
        serializedItems = []
        for item in listItems:
            serializedItems.append(item.serialize)
        cat["Sport_Items"] = serializedItems
        listJson.append(cat)
    return jsonify(Categories_with_Items=listJson)


# Show all categories and last items
@app.route('/', methods=['GET', 'POST'])
@app.route('/catalog/', methods=['GET', 'POST'])
def showCategories():
    engine = create_engine('sqlite:///sportscatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).order_by(desc(Item.id)).limit(9)
    # After logging in, a user has the ability to add, update,
    # or delete item info.
    if 'access_token' in login_session:
        loggedin = True
    else:
        loggedin = False
    # return json.dumps(login_session)
    return render_template('categories2.html', categories=categories,
                           items=items, loggedin=loggedin)


# Selecting a specific category shows you all the items
# available for that category.
@app.route('/catalog/<category_name>/items', methods=['GET', 'POST'])
def showItems(category_name):
    engine = create_engine('sqlite:///sportscatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(name=category_name).one()
    category_items = session.query(Item).filter_by(category_id=category.id)
    number_items = category_items.count()
    if 'access_token' in login_session:
        loggedin = True
    else:
        loggedin = False
    return render_template('category_items.html', categories=categories,
                           items=category_items, category=category,
                           number_items=number_items, loggedin=loggedin)


# Selecting a specific item shows you specific information of that item.
@app.route('/catalog/<category_name>/<item_title>', methods=['GET', 'POST'])
def ItemDescription(category_name, item_title):
    engine = create_engine('sqlite:///sportscatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(name=category_name).one()
    category_items = session.query(Item).filter_by(category_id=category.id)
    item_title = session.query(Item).filter_by(title=item_title).first()

    if 'access_token' in login_session:
        loggedin = True
    else:
        loggedin = False
    return render_template('item_description.html', item_title=item_title,
                           loggedin=loggedin)


@app.route('/catalog/<item_title>/edit', methods=['GET', 'POST'])
def editItem(item_title):
    engine = create_engine('sqlite:///sportscatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedItem = session.query(Item).filter_by(title=item_title).one()
    categories = session.query(Category).order_by(asc(Category.name))
    if 'access_token' in login_session:
        loggedin = True
    else:
        loggedin = False
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            category = session.query(Category).\
                       filter_by(name=request.form['category']).one()
            editedItem.category = category
        session.add(editedItem)
        session.commit()
        flash('Item %s Successfully Edited' % editedItem.title)
        return redirect(url_for('showCategories',
                        categories=categories, loggedin=loggedin))
    else:
        return render_template('edit_item.html', item=editedItem,
                               categories=categories, loggedin=loggedin)


# Delete a item
@app.route('/catalog/<item_title>/delete', methods=['GET', 'POST'])
def deleteItem(item_title):
    engine = create_engine('sqlite:///sportscatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).order_by(asc(Category.name))
    itemToDelete = session.query(Item).filter_by(title=item_title).first()

    if 'access_token' in login_session:
        loggedin = True
    else:
        loggedin = False
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item %s Successfully Deleted' % itemToDelete.title)
        return redirect(url_for('showCategories', categories=categories,
                        loggedin=loggedin))
    else:
        return render_template('delete_item.html', item=itemToDelete,
                               categories=categories, loggedin=loggedin)


# Create a new item
@app.route('/add/item', methods=['GET', 'POST'])
def addItem():
    engine = create_engine('sqlite:///sportscatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).order_by(asc(Category.name))
    if 'access_token' in login_session:
        loggedin = True
    else:
        loggedin = False
    if request.method == 'POST':
        user = session.query(User).\
               filter_by(email=login_session['email']).one()
        category = session.query(Category).\
            filter_by(name=request.form['category']).one()
        newItem = Item(title=request.form['title'],
                       description=request.form['description'],
                       category=category, category_id=category.id, user=user,
                       user_id=user.id)
        session.add(newItem)
        flash('New Item %s Successfully Created' % newItem.title)
        session.commit()
        items = session.query(Item).order_by(desc(Item.id)).limit(9)

        return redirect(url_for('showCategories', categories=categories,
                        items=items, loggedin=loggedin))
    else:
        return render_template('add_item.html',
                               categories=categories, loggedin=loggedin)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
