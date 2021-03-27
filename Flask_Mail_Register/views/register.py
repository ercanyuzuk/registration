# Email Varification Using OTP in Flask

from flask import Flask, render_template, request, Blueprint, flash, redirect, url_for
from flask_mail import Mail, Message
from random import randint
import re
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt


reg = Blueprint('reg', __name__, static_folder='static',
                template_folder='templates')

mysql = MySQL()
mail = Mail()
otp = randint(000000, 999999)


class degerler():
    name = str()
    surname = str()
    username = str()
    email = str()
    password = str()
    password_confirm = str()
    password_saved = str()


genel = degerler()


@reg.route('/register')
def register():

    return render_template('register.html')


@reg.route('/verify', methods=["GET", "POST"])
def ver():
    if request.method == 'POST':
        genel.name = request.form.get('name')
        genel.surname = request.form.get('surname')
        genel.username = request.form.get('username')
        genel.email = request.form.get('email')
        genel.password = request.form.get('password')
        genel.password_confirm = request.form.get('password_confirm')
        genel.password_saved = sha256_crypt.encrypt(
            request.form.get('password'))
        msg = Message(subject='OTP', sender='destek@tesannetwork.com',
                      recipients=[genel.email])
        msg.body = str(otp)

        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE username = % s', (genel.username, ))

        account = cursor.fetchone()

        if account:
            mesaj = 'kullanıcı zaten kayıtlı'
            return render_template('register.html', mesaj=mesaj)

        elif (len(genel.username) < 4 or len(genel.username) > 10):
            mesaj = "Kullanıcı adı 4'ten küçük, 10'dan büyük olamaz"
            return render_template('register.html', mesaj=mesaj)

        elif not re.search('[A-Z]', genel.username):
            mesaj = 'En az bir büyük harf olması gerekir!,Rakam içermez'
            return render_template('register.html', mesaj=mesaj)

        elif not re.search('[a-z]', genel.username):
            mesaj = 'En az bir küyük harf olması gerekir!,Rakam içermez !'
            return render_template('register.html', mesaj=mesaj)

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', genel.email):
            mesaj1 = 'Hatalı Mail Adresi !'
            return render_template('register.html', mesaj1=mesaj1)

        elif genel.password != genel.password_confirm:
            mesaj2 = 'Şifreler Uyuşmuyor'
            return render_template('register.html', mesaj2=mesaj2)

        else:
            mail.send(msg)
            flash('Mail gönderimi Başarılı', 'success')
            return render_template('verify.html')

    else:

        return render_template('verify.html')


@reg.route('/validate', methods=['POST'])
def val():
    user_otp = request.form['otp']

    if otp == int(user_otp):
        cursor = mysql.connection.cursor()
        sorgu = "Insert into users(name,surname,username,mail,password) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(sorgu, (genel.name, genel.surname,
                               genel.username, genel.email, genel.password_saved))
        mysql.connection.commit()
        flash('Kullanıcı Doğrulama Başarılı', 'success')
        return render_template('validate.html')
    flash('Kullanıcı Doğrulama Geçersiz', 'danger')
    return render_template('verify.html')
