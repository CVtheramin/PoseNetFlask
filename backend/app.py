from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename


def create_app():
    app = Flask(__name__)

    def render_svg(name):
        svg = file('static/svg/+'+name+'.svg').read()
        return render_template('index.html',{'svg':svg})

    @app.route('/')
    def index():
        return render_svg('index')

    @app.route('/about')
    def about():
        return render_svg('about')

    @app.route('/play')
    def play():
        return render_svg('play')

    @app.route('/remix')
    def remix():
        return render_svg('remix')

    @app.route('/dance')
    def dance():
        return render_svg('dance')

    return app
