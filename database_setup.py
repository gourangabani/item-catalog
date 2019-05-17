import os, sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class category(Base):
    __tablename__ = 'table_categories'
    category_id = Column(String, primary_key = True)
    category_name = Column(String, nullable = False)
    category_logo_filename = Column(String)

class item(Base):
    __tablename__ = 'table_items'
    item_id = Column(String, primary_key = True)
    item_name = Column(String, nullable = False)
    item_description = Column(String)
    category_id = Column(String, ForeignKey('category.category_id'))
    category_relationship = relationship(category)

engine = create_engine('sqlite:///item_catalog.db')

Base.metadata.create_all(engine)
