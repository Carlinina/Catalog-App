# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///sportscatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create first user
User1 = User(name="Carla Rodriguez Cuesta",
             email="carlarodriguezcuesta@gmail.com",
             picture='https://as01.epimg.net/tikitakas/imagenes/2018/07/12/\
             portada/1531406570_709235_1531407095_noticia_normal.jpg')
session.add(User1)
session.commit()

# Items for Soccer
category1 = Category(user_id=1, name="Soccer")

session.add(category1)
session.commit()

Item1 = Item(user_id=1, title="Soccer cleats", description="what the English \
             call boots, are like baseball or softball cleats but the cleats \
             are short and made of rubber (metal cleats are not allowed).",
             category=category1)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1, title="Shin Guards", description="Soccer is definitely \
             a contact sport. Shin guards help reduce the chance of injury \
             to the shin (tibia), the third-most likely area of the body to \
             be injured playing soccer, according to a recent study.",
             category=category1)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="Soccer ball", description="The ball's \
             spherical shape, as well as its size, weight, and material \
             composition, are specified by Law 2 of the Laws of the Game \
             maintained by the International Football Association Board.",
             category=category1)

session.add(Item3)
session.commit()

# Items for Basketball
category2 = Category(user_id=1, name="Basketball")

session.add(category2)
session.commit()


Item1 = Item(user_id=1, title="Shoes", description="One needs specialized \
             shoes when playing basketball. It should be able to give \
             better support to the ankle as compared to running shoes.",
             category=category2)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title="Basketball Shooting Equipment",
             description="The hoop or basket is a horizontal metallic \
             rim, circular in shape. This rim is attached to a net and \
             helps one score a point. The rim is mounted about 4 feet \
             inside the baseline and 10 feet above the court.",
             category=category2)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="Backboard", description="The backboard is \
             the rectangular board that is placed behind the rim. It helps \
             give better rebound to the ball. The backboard is about 1800mm \
             in size horizontally and 1050mm vertically. Many times, \
             backboards are made of acrylic, aluminum, steel or glass.",
             category=category2)

session.add(Item3)
session.commit()


# Items for Baseball
category3 = Category(user_id=1, name="Baseball")

session.add(category3)
session.commit()


Item1 = Item(user_id=1, title="Bat", description="A rounded, solid wooden \
             or hollow aluminum bat. Wooden bats are traditionally made \
             from ash wood, though maple and bamboo is also sometimes \
             used. Aluminum bats are not permitted in professional \
             leagues, but are frequently used in amateur leagues.",
             category=category3)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title="Glove", description="Leather gloves worn by \
             players in the field. Long fingers and a webbed KKK between \
             the thumb and first finger allows the fielder to catch the \
             ball more easily.", category=category3)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="Catcher's helmet", description="Protective \
             helmet with face mask worn by the catcher. Newer styles \
             feature a fully integrated helmet and mask, similar to a \
             hockey goalie mask. More traditional versions were a separate \
             mask worn over a helmet similar to a batting helmet, but with \
             no ear protection and worn backwards.", category=category3)

session.add(Item3)
session.commit()

Item4 = Item(user_id=1, title="Uniform", description="Shirt and pants \
             worn by all players, coaches and managers. Each team \
             generally has a unique pattern of colors and designs. \
             Traditionally, the home team's uniform is predominantly \
             white with the team's nickname, and the visiting team's is \
             predominantly gray with (usually, but not always) the team's \
             city. Teams often have white, gray and colored jerseys; \
             colored jerseys can be worn at home or on the road, depending \
             on the team's preference.", category=category3)

session.add(Item4)
session.commit()

Item5 = Item(user_id=1, title="Baseball cap", description="Hat worn by \
             all players. Designed to shade the eyes from the sun, this \
             hat design has become popular with the general public.",
             category=category3)

session.add(Item5)
session.commit()


# Items for Frisbee
category4 = Category(user_id=1, name="Frisbee")

session.add(category4)
session.commit()


Item1 = Item(user_id=1, title="Frisbee Cleat", description="Shoes.",
             category=category4)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title="Frisbee", description="Flying disc that \
             is generally plastic and roughly 20 to 25 \
             centimetres (8 to 10 in) in diameter with a pronounced lip.",
             category=category4)

session.add(Item2)
session.commit()


# Items for Snowboarding
category5 = Category(user_id=1, name="Snowboarding")

session.add(category5)
session.commit()


Item1 = Item(user_id=1, title="Snowboard", description="A board \
             resembling a short, broad ski, used for sliding downhill \
             on snow.", category=category5)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title="Snowboard Boots", description="These \
             specialized boots will connect you to your board through \
             the bindings. You can also rent these at the resort, but \
             it is not recommended. Snowboard boots are designed \
             to conform to your feet specifically, so owning your \
             own pair will be far more comfortable.", category=category5)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="Snowboard Helmet", description="Your \
             brain is the most important organ in your body, so wearing \
             a helmet should be an easy decision. As a beginner, you \
             may struggle with control, so protecting your head is \
             paramount. If you do not own a helmet, the resort will \
             have various options to rent one that ensure you will \
             find one that fits.", category=category5)

session.add(Item3)
session.commit()
# Items for Rock Climbing
category6 = Category(user_id=1, name="Climbing")

session.add(category6)
session.commit()


Item1 = Item(user_id=1, title="Rope", description="Climbing ropes \
             are typically of kernmantle construction, consisting \
             of a core (kern) of long twisted fibres and an outer sheath \
             (mantle) of woven coloured fibres.", category=category6)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title="Harnesses", description="a system \
             used for connecting the rope to the climber. There are \
             two loops at the front of the harness where the climber \
             ties into the rope at the working end using a figure-eight \
             knot.", category=category6)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="Climbing shoes", description="Specifically \
             designed foot wear is usually worn for climbing. \
             To increase the grip of the foot on a climbing wall or rock \
             face due to friction, the shoe is soled with a vulcanized \
             rubber layer.", category=category6)

session.add(Item3)
session.commit()

# Items for Foosball
category7 = Category(user_id=1, name="Foosball")

session.add(category7)
session.commit()


Item1 = Item(user_id=1, title="Table soccer", description="It's \
             a table-top game that is loosely based on football.",
             category=category7)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title="Foosball gloves", description="Gloves \
             of genuine leather is made specifically for table football \
             to ensure better grip and control.",
             category=category7)

session.add(Item2)
session.commit()


# Items for Skating
category8 = Category(user_id=1, name="Skating")

session.add(category8)
session.commit()


Item1 = Item(user_id=1, title="Skates", description="a metal frame \
             that can be fitted to the sole of a shoe and to which \
             is attached a runner or a set of wheels for gliding over \
             ice or a surface other than ice.",
             category=category8)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title="Soakers", description="Soakers are terry \
             cloth blade covers that protect and keep figure skating \
             blades dry. After drying your blades thoroughly, soakers \
             should be placed over figure skating blades and then, the \
             skates with the soakers on should be placed in the skate bag.",
             category=category8)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="Towel", description="Figure skaters must \
             always dry blades thoroughly after skating.",
             category=category8)

session.add(Item3)
session.commit()
# Items for Hockey
category9 = Category(user_id=1, name="Hockey")

session.add(category9)
session.commit()


Item1 = Item(user_id=1, title="Stick", description="Your hockey \
             stick is like your weapon on the battlefield. After \
             choosing the most suitable hockey stick for yourself, \
             you will learn to use it and after a while, be so \
             comfortable with it that it becomes a part of you.",
             category=category9)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title="T-shirt", description="A short-sleeved \
             casual top, generally made of cotton, having the shape \
             of a T when spread out flat.",
             category=category9)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="Helmet", description="Head Protection.",
             category=category9)

session.add(Item3)
session.commit()

print "added categories and items!"
