#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Categories

class category(Base):

    __tablename__ = 'table_categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)
    category_logo_filename = Column(String)

    @property
    def serialize(self):
        return {'id': self.category_id, 'name': self.category_name}


# Items

class item(Base):

    __tablename__ = 'table_items'
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    item_description = Column(String)
    item_category_name = Column(Integer,
                                ForeignKey('table_categories.category_id'))
    item_category_relationship = relationship(category)

    @property
    def serialize(self):
        return {
            'category': self.item_category_name,
            'id': self.item_id,
            'name': self.item_name,
            'description': self.item_description
            }


engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.create_all(engine)
