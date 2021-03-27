from flask import Flask, Blueprint
from flask_mail import Mail, Message
from views.homepage import main
from views.login import Login
from views.register import reg
from flask_mysqldb import MySQL
from views.update import Update

app = Flask(__name__)
app.secret_key = 'deneme'

mail = Mail(app)
app.config["MAIL_SERVER"] = 'yourmailserverip'
app.config["MAIL_PORT"] = 25
app.config["MAIL_USERNAME"] = 'yourmailaddress'
app.config['MAIL_PASSWORD'] = 'mailpassword'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "******"
app.config["MYSQL_DB"] = "myapp"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_PORT"] = 3306

mysql = MySQL(app)


app.register_blueprint(main)
app.register_blueprint(reg)
app.register_blueprint(Login)
app.register_blueprint(Update)

if __name__ == "__main__":
    app.run(debug=True)
