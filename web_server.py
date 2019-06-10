#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import string
import httplib2
import json
import requests
from flask import Flask, render_template, url_for, request, redirect, \
    flash, make_response, jsonify
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, join, sessionmaker
from database_setup import Base, category, item
from oauth2client.client import flow_from_clientsecrets, \
    FlowExchangeError

app = Flask(__name__)
app.secret_key = 'secret_key'

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# OAuth Client ID

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())[
    'web']['client_id']

# User Login Status Tracker

login_session = {}


# Home

@app.route('/')
@app.route('/catalog/')
def home():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(category).all()
    items = session.query(item).order_by(item.item_id.desc()).limit(10)
    if 'username' not in login_session:
        return render_template('home.html',
                               fetched_categories=categories,
                               fetched_items=items)
    else:
        return render_template('home_logged_in.html',
                               fetched_categories=categories,
                               fetched_items=items)


# Category

@app.route('/catalog/<string:category_input>/items/')
def items_in_category(category_input):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = \
        session.query(category).filter_by(category_name=category_input).one()
    items = \
        session.query(item).filter_by(item_category_name=category_input).all()
    if 'username' not in login_session:
        return render_template('items_in_category.html',
                               fetched_category=categories,
                               fetched_items=items)
    else:
        return render_template('items_in_category_logged_in.html',
                               fetched_category=categories,
                               fetched_items=items)


# Item Description

@app.route('/catalog/<string:category_input>/<string:item_input>/')
def item_description(category_input, item_input):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    items = session.query(item).filter_by(item_name=item_input).one()
    if 'username' not in login_session:
        return render_template('item_description.html',
                               fetched_item=items)
    else:
        return render_template('item_description_logged_in.html',
                               fetched_item=items)


# New Item

@app.route('/catalog/add/', methods=['GET', 'POST'])
def new_item():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    else:
        author = login_session['username']
        if request.method == 'POST':
            to_be_added_item = item(
                item_name=request.form['item_name'],
                item_description=request.form['item_description'],
                item_category_name=request.form['item_category_name'],
                item_author=author)
            session.add(to_be_added_item)
            session.commit()
            return redirect(url_for('home'))
        else:
            all_categories = session.query(category).all()
            return render_template('new_item.html',
                                   fetched_categories=all_categories)


# Edit Item

@app.route('/catalog/<string:item_input>/edit/', methods=['GET', 'POST'
                                                          ])
def edit_item(item_input):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            to_be_edited_item = \
                session.query(item).filter_by(item_name=item_input).one()
            if to_be_edited_item.item_author == login_session['username']:
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
                return redirect(
                    url_for(
                        'item_description',
                        category_input=to_be_edited_item.item_category_name,
                        item_input=item_input))
            else:
                flash("You are not authorised to make this change.")
                return render_template('wrong_author.html')
        else:
            to_be_edited_item = \
                session.query(item).filter_by(item_name=item_input).one()
            all_categories = session.query(category).all()
            return render_template('edit_item.html',
                                   fetched_item=to_be_edited_item,
                                   fetched_categories=all_categories)


# Delete Item

@app.route('/catalog/<string:item_input>/delete/', methods=['GET',
                                                            'POST'])
def delete_item(item_input):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            to_be_deleted_item = \
                session.query(item).filter_by(item_name=item_input).one()
            if to_be_deleted_item.item_author == login_session['username']:
                session.delete(to_be_deleted_item)
                session.commit()
                return redirect(
                    url_for(
                        'items_in_category',
                        category_input=to_be_deleted_item.item_category_name))
            else:
                flash("You are not authorised to delete this item.")
                return render_template('wrong_author.html')
        else:
            to_be_deleted_item = \
                session.query(item).filter_by(item_name=item_input).one()
            return render_template('delete_item.html',
                                   fetched_item=to_be_deleted_item)


# Login

@app.route('/login/')
def show_login():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Login Successful

@app.route('/authenticated', methods=['POST'])
def authenticated_success():

    # Validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'
                                            ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data
    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets('client_secret.json',
                                             scope='openid')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
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
        response = \
            make_response(json.dumps("Token's client ID does not match app's."
                                     ), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'
                                     ), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    output = '<h1 class="text-white mt-5 mb-2">Welcome, ' \
        + login_session['username'] \
        + "!</h1><a href='http://localhost:8000/catalog'>\
        <h6 class='text-white mt-5 mb-2'>\
        Click here if you aren't redirected in a second.</h6></a>"
    return output


# Logout

@app.route('/logout/')
def do_logout():
    access_token = login_session.get('access_token')
    if access_token is None:
        output = '401. No user is connected.'
        redirect_url = 'http://localhost:8000/login'
        return render_template('logout.html', message=output,
                               url=redirect_url)
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        output = 'Successful!'
        redirect_url = 'http://localhost:8000/catalog'
        return render_template('logout.html', message=output,
                               url=redirect_url)
    else:
        output = '400. Failed to revoke token for given user.'
        redirect_url = 'http://localhost:8000/catalog'
        return render_template('logout.html', message=output,
                               url=redirect_url)


# JSON Endpoint

@app.route('/catalog/json')
def jsonify_items_in_categories():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    items = session.query(item).all()
    categories = session.query(category).all()
    return jsonify(Category=[category_index.serialize
                             for category_index in categories],
                   Item=[item_index.serialize for item_index in items])

# JSON Endpoint for individual items


@app.route('/catalog/<string:category_input>/<string:item_input>/json/')
def jsonify_individual_items(category_input, item_input):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    requested_item = session.query(item).filter_by(item_name=item_input).one()
    return jsonify(Item=[requested_item.serialize])


# Execution

if __name__ == '__main__':
    app.debug = True  # remove
    app.run(host='0.0.0.0', port=8000)
