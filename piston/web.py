import re
from flask import Flask, redirect, url_for, session, current_app
from flask_assets import Environment
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown
from .utils import strfdelta, strfage
from flask_socketio import SocketIO
import html2text
import lxml.html


app = Flask(__name__)
socketio = SocketIO(app)
Bootstrap(app)
webassets = Environment(app)
markdown = Markdown(
    app,
    extensions=['meta',
                'tables'
                ],
    safe_mode=True,
    output_format='html4'
)

from . import web_assets, web_views


def is_html(body):
    return lxml.html.fromstring(body).find('.//*') is not None


@app.template_filter('age')
def _jinja2_filter_age(date, fmt=None):
    return strfage(date, fmt)


@app.template_filter('excert')
def _jinja2_filter_datetime(data):
    words = data.split(" ")
    return " ".join(words[:100])


@app.template_filter('parseBody')
def _jinja2_filter_parseBody(body):
    body = re.sub(
        r"^(https?:.*/(.*\.(jpg|png|gif))?.*)",
        r"\n![](\1)\n",
        body, flags=re.MULTILINE)
    if is_html(body):
        body = html2text.html2text(body)
    return body


@app.template_filter('currency')
def _jinja2_filter_currency(value):
    return "{:,.3f}".format(value)


def run():
    socketio.run(app, debug=True, port=app.config.get("PORT", 5054))

    # FIXME: Don't use .run()
    # from gevent.wsgi import WSGIServer
    # from yourapplication import app
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()

app.config["GOOGLE_ANALYTICS_ID"] = ""
app.config["SECRET_KEY"] = "abcdefghijklmnopqrstuvwxyz"
