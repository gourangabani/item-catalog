#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect, \
    flash
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, join, sessionmaker
from database_setup import Base, category, item

app = Flask(__name__)

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(category).all()
    items = session.query(item).order_by(item.item_id.desc()).limit(10)
    return render_template('home.html', fetched_categories=categories,
                           fetched_items=items)


@app.route('/catalog/<string:category_input>/items/')
def items_in_category(category_input):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = \
        session.query(category).filter_by(category_name=category_input).one()
    items = \
        session.query(item).filter_by(item_category_name=category_input).all()
    return render_template('items_in_category.html',
                           fetched_category=categories,
                           fetched_items=items)


@app.route('/catalog/<string:category_input>/<string:item_input>/')
def item_description(category_input, item_input):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    items = session.query(item).filter_by(item_name=item_input).one()
    return render_template('item_description.html', fetched_item=items)


@app.route('/catalog/add/', methods=['GET', 'POST'])
def new_item():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        to_be_added_item = item(item_name=request.form['item_name'],
                                item_description=request.form['item_description'
                                ],
                                item_category_name=request.form['item_category_name'
                                ])
        all_categories = session.query(category).all()
        session.add(to_be_added_item)
        session.commit()
        return redirect(url_for('home'))
    else:
        all_categories = session.query(category).all()
        return render_template('new_item.html',
                               fetched_categories=all_categories)


@app.route('/catalog/<string:item_input>/edit/', methods=['GET', 'POST'
           ])
def edit_item(item_input):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        to_be_edited_item = \
            session.query(item).filter_by(item_name=item_input).one()
        all_categories = session.query(category).all()
        if request.form['item_name']:
            to_be_edited_item.item_name = request.form['item_name']
        if request.form['item_description']:
            to_be_edited_item.item_description = \
                request.form['item_description']
        if request.form['item_category_name']:
            to_be_edited_item.item_category_name = \
                request.form['item_category_name']
        session.add(to_be_edited_item)
        session.commit()
        return redirect(url_for('item_description',
                        category_input=to_be_edited_item.item_category_name,
                        item_input=item_input))
    else:
        to_be_edited_item = \
            session.query(item).filter_by(item_name=item_input).one()
        all_categories = session.query(category).all()
        return render_template('edit_item.html',
                               fetched_item=to_be_edited_item,
                               fetched_categories=all_categories)


@app.route('/catalog/<string:item_input>/delete/', methods=['GET',
           'POST'])
def delete_item(item_input):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        to_be_deleted_item = \
            session.query(item).filter_by(item_name=item_input).one()
        session.delete(to_be_deleted_item)
        session.commit()
        return redirect(url_for('items_in_category',
                        category_input=to_be_deleted_item.item_category_name))
    else:
        to_be_deleted_item = \
            session.query(item).filter_by(item_name=item_input).one()
        return render_template('delete_item.html',
                               fetched_item=to_be_deleted_item)

if __name__ == '__main__':
    app.debug = True  # remove
    app.run(host='0.0.0.0', port=8000)
    app.secret_key = 'secret_key'
