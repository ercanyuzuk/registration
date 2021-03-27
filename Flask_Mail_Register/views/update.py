from flask import Flask, render_template, request, Blueprint, flash, redirect, url_for
from flask_mail import Mail, Message
from random import randint
import re
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

Update = Blueprint('Update', __name__, static_folder='static',
                   template_folder='templates')

mysql = MySQL()
mail = Mail()
otp = randint(000000, 999999)


class degerler():
    mail = str()


genel = degerler()


@Update.route("/update", methods=["GET", "POST"])
def reset():

    return render_template("update.html")


@Update.route("/control", methods=["GET", "POST"])
def control():
    genel.email = request.form.get('email')
    cursor = mysql.connection.cursor()
    sorgu = 'SELECT * FROM users WHERE mail = %s'
    result = cursor.execute(sorgu, (genel.email,))
    account = cursor.fetchall()

    if account:

        msg = Message(
            subject='OTP', sender='destek@tesannetwork.com', recipients=[genel.email])
        msg.body = str(otp)
        mail.send(msg)
        return render_template("control.html")
    else:
        flash('Email adresi sistemde gözükmüyor', 'danger')
        return render_template("update.html")


@Update.route("/confirm", methods=["GET", "POST"])
def confirm():
    user_otp = request.form['otp']

    if otp == int(user_otp):

        flash('Kullanıcı Doğrulama Başarılı', 'success')
        return render_template('confirm.html')

    flash('Kullanıcı Doğrulama Geçersiz', 'danger')

    return render_template("confirm.html")


@Update.route("/rstpasww", methods=["GET", "POST"])
def rstpasww():

    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    newhash_password = sha256_crypt.encrypt(request.form.get('password'))

    if password == confirm_password:
        cursor = mysql.connection.cursor()
        sorgu = "update users set password=%s where mail=%s"
        cursor.execute(sorgu, (newhash_password, genel.email))
        mysql.connection.commit()

        flash('Parolanızı değiştirme başarılı', 'success')
        return redirect(url_for('Login.login'))
    else:
        flash('Parola eşleşmiyor', 'danger')
        return render_template('confirm.html')
