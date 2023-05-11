from flask_app import app
from flask_app.controller import armadillo_controller
from flask_app.controller import playground_controller

if __name__ == '__main__':
    app.run(debug=True)