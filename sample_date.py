from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, category, item

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Categories

session.add(category(category_name="Soccer", category_logo_filename="images/soccer_logo.png"))
session.add(category(category_name="Baseball", category_logo_filename="images/baseball_logo.png"))
session.add(category(category_name="Frisbee", category_logo_filename="images/frisbee_logo.png"))
session.add(category(category_name="Skating", category_logo_filename="images/skating_logo.png"))
session.add(category(category_name="Basketball", category_logo_filename="images/basketball_logo.png"))
session.add(category(category_name="Ice Hockey", category_logo_filename="images/ice-hockey_logo.png"))
session.add(category(category_name="Snowboarding",
                     category_logo_filename="images/snowboarding_logo.png"))
session.add(category(category_name="Skateboarding",
                     category_logo_filename="images/skateboarding_logo.png"))
session.add(category(category_name="Rock Climbing",
                     category_logo_filename="images/rock-climbing_logo.png"))

# Items

session.add(item(item_name="Football", item_category_name="Soccer",
                 item_description="A football, soccer ball, or association football ball is the ball used in the sport of association football. "))
session.add(item(item_name="Shin Guards", item_category_name="Soccer",
                 item_description="A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury."))
session.add(item(item_name="Basketball", item_category_name="Basketball",
                 item_description="A basketball is a spherical ball used in basketball games."))
session.add(item(item_name="Bat", item_category_name="Baseball",
                 item_description="A baseball bat is a smooth wooden or metal club used in the sport of baseball to hit the ball after it is thrown by the pitcher."))
session.add(item(item_name="Helmet", item_category_name="Baseball",
                 item_description="A batting helmet is worn by batters in the game of baseball or softball."))
session.add(item(item_name="Glove", item_category_name="Baseball",
                 item_description="A baseball glove or mitt is a large leather glove worn by baseball players of the defending team, which assists players in catching and fielding balls hit by a batter or thrown by a teammate."))

session.commit()
