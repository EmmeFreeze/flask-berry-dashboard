# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import os
import sqlite3

@blueprint.route('/index')
@login_required
def index():
    DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), r"../checklist.db"
)
    # Connect to the database and query for data
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    categories = []
    # Query the database for categories
    c.execute("SELECT * FROM Categories")
    categories_rows = c.fetchall()
    for category_row in categories_rows:
        category_id, category_name = category_row
        # Query the database for locations associated with the current category
        c.execute("SELECT * FROM Locations WHERE category_id = ?", (category_id,))
        locations_rows = c.fetchall()
        locations = []
        for location_row in locations_rows:
            location_id, location_name, _ = location_row
            # Query the database for objects associated with the current location
            c.execute(
                "SELECT object_name, req_quantity FROM Objects WHERE location_id = ?",
                (location_id,),
            )
            objects_rows = c.fetchall()
            objects = []
            for object_row in objects_rows:
                object_name, object_quantity = object_row
                objects.append(
                    {"object_name": object_name, "object_quantity": object_quantity}
                )
            # Add the current location to the list of locations
            locations.append(
                {"location_name": location_name, "location_objects": objects}
            )
        # Add the current category to the list of categories
        categories.append({"category_name": category_name, "locations": locations})

    # Close the connection to the database
    conn.close()
    return render_template('pages/index.html', segment='index', categories=categories)

@blueprint.route('/typography')
@login_required
def typography():
    return render_template('pages/typography.html')

@blueprint.route('/color')
@login_required
def color():
    return render_template('pages/color.html')

@blueprint.route('/icon-tabler')
@login_required
def icon_tabler():
    return render_template('pages/icon-tabler.html')

@blueprint.route('/sample-page')
@login_required
def sample_page():
    return render_template('pages/sample-page.html')  

@blueprint.route('/accounts/password-reset/')
def password_reset():
    return render_template('accounts/password_reset.html')

@blueprint.route('/accounts/password-reset-done/')
def password_reset_done():
    return render_template('accounts/password_reset_done.html')

@blueprint.route('/accounts/password-reset-confirm/')
def password_reset_confirm():
    return render_template('accounts/password_reset_confirm.html')

@blueprint.route('/accounts/password-reset-complete/')
def password_reset_complete():
    return render_template('accounts/password_reset_complete.html')

@blueprint.route('/accounts/password-change/')
def password_change():
    return render_template('accounts/password_change.html')

@blueprint.route('/accounts/password-change-done/')
def password_change_done():
    return render_template('accounts/password_change_done.html')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
