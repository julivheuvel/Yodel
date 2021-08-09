from flask_app import app, socketio, mail
from flask_app.controllers import users, yodels










if __name__ == "__main__":
    socketio.run(app,debug=True)