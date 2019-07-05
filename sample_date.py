#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, category, item

engine = create_engine('postgresql://catalog:catalog@localhost/item-catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Categories

session.add(category(category_name="Soccer",
                     category_logo_filename="images/soccer_logo.png"))
session.add(category(category_name="Baseball",
                     category_logo_filename="images/baseball_logo.png"))
session.add(category(category_name="Frisbee",
                     category_logo_filename="images/frisbee_logo.png"))
session.add(category(category_name="Skating",
                     category_logo_filename="images/skating_logo.png"))
session.add(category(category_name="Basketball",
                     category_logo_filename="images/basketball_logo.png"))
session.add(category(category_name="Ice Hockey",
                     category_logo_filename="images/ice-hockey_logo.png"))
session.add(category(category_name="Snowboarding",
                     category_logo_filename="images/snowboarding_logo.png"))
session.add(category(category_name="Skateboarding",
                     category_logo_filename="images/skateboarding_logo.png"))
session.add(category(category_name="Rock Climbing",
                     category_logo_filename="images/rock-climbing_logo.png"))
                     
session.commit()