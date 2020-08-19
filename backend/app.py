from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def sample():
        return render_template('practice.html')

    return app
