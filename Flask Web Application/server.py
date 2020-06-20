from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from jinja2 import Markup
import mysql.connector as sql

# infoDict['js']= Markup(js)


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.debug = True
app.secret_key = "super secret key"


def require_db_connection():
    #  Here i am making a connection with mysql database hosted by the xampp server!
    db = sql.connect(
        host="localhost",
        user="root",
        password="",
        database="project_wang_reda"
    )
    #  Then i am making a cursor to execute sql commands in the following below functions and decorators

    return db, db.cursor()

