from flask import Flask, render_template, request, Blueprint, flash, redirect, url_for, session
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

Login = Blueprint('Login', __name__, static_folder='static',
                  template_folder='templates')

mysql = MySQL()


@Login.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        sorgu = 'SELECT * FROM users WHERE username = %s'
        result = cursor.execute(sorgu, (username,))

        if result > 0:
            account = cursor.fetchone()
            reel_password = account['password']

            if sha256_crypt.verify(password, reel_password):

                session['logged_in'] = True
                session['username'] = account['username']
                flash('Kullanıcı Doğrulama Başarılı !', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Yanlış Kullanıcı Adı veya Şifresi', 'danger')
                return render_template('login.html')
        else:
            flash('Böyle Bir Kullanıcı Bulunamadı', 'danger')
            return render_template('login.html')

    else:

        return render_template('login.html')


@Login.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    flash('Yine Bekleriz', 'info')
    return redirect(url_for('main.index'))
