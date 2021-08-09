from flask import Flask
from flask_mail import Mail, Message
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app)


app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'ee3397196@gmail.com'
app.config['MAIL_PASSWORD'] = 'rqmguctuazecwtzx'
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['MAIL__MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)




app.secret_key = "yodellingyodels"