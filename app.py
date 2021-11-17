from flask import Flask, render_template, request,redirect, url_for, flash, session
import db_function as bf
from forms import RegistrForm

app = Flask(__name__)
app.secret_key = 'my_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def lets_play():
    if 'user_id' in session:
        session['user_scores'] = bf.get_score(session['user_id'])
    else:
        session['user_scores'] = 0
    return render_template('game.html', counter = session['user_scores'])

@app.route('/<int:counter>', methods=["POST"])
def get_count(counter):
    if 'user_id' in session:
        session['user_scores'] = counter
        bf.update_score(session['user_scores'], session['user_id'])
        return redirect(url_for('lets_play'))
    session['user_scores'] = counter
    return redirect(url_for('registration'))
    
@app.route('/rigistr', methods=["GET", "POST"])
def registration():
    form = RegistrForm()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = request.form.get("remember_me")        
        #обрабатываем галку "запомни меня"
        if remember_me:
            session.permanent = True
        else:
            session.permanent = False

        #записываем пользователя в базу если его почту ещё не регистрировались
        if bf.write_in_base(name, email, password, 0):
            flash("Пользователь с такой почтой уже зарегистрирован!")
            return redirect(url_for('registration'))

        #записываем пользователя в сессию, чтобы после регистрации он остался залогиненым
        session['user_name'] = name
        session['user_scores'] = 0
        session['user_id'] = bf.get_user(name, email, password)[0][0]
        flash("Вы зарегистрировались!")
        return redirect(url_for('registration'))
    return render_template('sign_in.html', form=form, adr=url_for('registration'))

@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    #если пользователь уже вошел, перенаправляем на игру
    if 'user_id' in session:
        return redirect(url_for('lets_play'))
        
    form = RegistrForm()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = request.form.get("remember_me")
        #получаем данные пользователя из базы данных
        user_data = bf.get_user(name, email, password)[0]
        #обрабатываем галку "запомни меня"
        if remember_me:
            session.permanent = True
        else:
            session.permanent = False
        
        if user_data:
            #сохраняем данные пользователя в сессии
            session['user_id'] = user_data[0]
            session['user_name'] = user_data[1]
            session['user_scores'] = user_data[4]
            return redirect(url_for('lets_play'))
    return render_template('sign_in.html', form=form, adr=url_for('sign_in'))

@app.route('/logout')
def logout():
    # удаляет пользователя из сессии
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_scores', None)
    return redirect(url_for('index'))

@app.route('/score_board')
def score_board():
    return render_template('top_ten.html', top_ten = bf.get_top())
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
