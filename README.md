# Catalog-App
Catalog App is an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Requirements
In order to run this program you will need the following:

1. Computer (Windows or Mac OS)
2. Working knowlage of using the command-line.
  
## Instructions

1. Install Vagrant and VirtualBox
2. Clone the fullstack-nanodegree-vm
3. Launch the Vagrant VM (vagrant up)
4. Copy the Flask application locally in the vagrant/catalog directory (which will automatically be synced to /vagrant/catalog within the VM).
5. Run your application within the VM (python /vagrant/catalog/application.py)
6. Execute 'python lostsofitems.py' in the command line.
7. Execute 'python application.py' in the command line.
8. Access and test the application by visiting http://localhost:8000 locally
9. Enjoy!

## Project Display Example

In this sample project, the homepage displays all current categories along with the latest added items:
http://localhost:8000/
Example front page of the catalog app:
https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0c98_localhost8080/localhost8080.png

Selecting a specific category shows you all the items available for that category:
http://localhost:8000/catalog/Snowboarding/items
Example category page:
https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0d0e_snowboarding/snowboarding.png


Selecting a specific item shows you specific information of that item:
http://localhost:8000/catalog/Snowboarding/Snowboard
Example item page:
https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0d7a_item/item.png


After logging in, a user has the ability to add, update, or delete item info:
http://localhost:8000/ (logged in)
Logged-in view of the catalog app, showing a Logout button:
https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0df0_edititem/edititem.png


Item description page when logged in, showing Edit and Delete buttons.
http://localhost:8000/catalog/Snowboarding/Snowboard (logged in)
Example:
https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0e51_snowboardloggedin/snowboardloggedin.png

Edit view:
http://localhost:8000/catalog/Snowboard/edit (logged in)
Example:
https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0e8c_snowboardedit/snowboardedit.png


Delete confirmation dialog:
http://localhost:8000/catalog/Snowboard/delete (logged in)
Example:
https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0ec8_snowboarddelete/snowboarddelete.png


The application provides a JSON endpoint:
http://localhost:8000/catalog.json
Example JSON endpoint output:
https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0f11_catalogjson/catalogjson.png


