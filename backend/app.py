from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import os


def create_app():
    app = Flask(__name__)
    path = os.path.abspath(os.path.dirname(__file__))
    def render_svg(name):
        fn = open(path+'/static/svg/'+name+'.svg',"r")
        svg = fn.read()
        fn.flush()
        fn.close()
        context = {'svg':svg}
        return render_template('index.html',**context)

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
