from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from . import routes

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)