from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User

@app.route('/')
def home():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/<username>')
def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return f"Username: {user.username}, Email: {user.email}"

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        if not User.query.filter_by(username=username).first():
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            flash('User added successfully!', 'success')
        else:
            flash('User already exists!', 'danger')
        return redirect(url_for('home'))
    return render_template('add_user.html')
