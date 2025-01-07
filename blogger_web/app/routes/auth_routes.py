from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app.forms import ProfileUpdateForm, LoginForm, RegistrationForm
from app.models import User
from app import db, bcrypt
import os, secrets
from PIL import Image

auth = Blueprint('auth', __name__)

def save_picture(form_picture):
    """Save the uploaded picture to the file system and return the filename."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('post.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Assign admin role to the first registered user
        is_admin = User.query.count() == 0
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_admin=is_admin)
        
        db.session.add(user)
        db.session.commit()

        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)



@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('post.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('post.home'))
        flash('Login unsuccessful. Check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        # Update username and email
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Update password if provided
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password

        # Update profile picture if provided
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.profile'))
    
    elif request.method == 'GET':
        # Populate form with current user data
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Profile', form=form, image_file=image_file)


@auth.route("/notifications", methods=["GET", "POST"])
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    if request.method == "POST":
        for notification in notifications:
            notification.is_read = True
        db.session.commit()
        flash("All notifications marked as read", "success")
    return render_template("notifications.html", notifications=notifications)

@auth.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("post.home"))

    # Fetch all users and posts without pagination
    users = User.query.order_by(User.username).all()
    posts = Post.query.order_by(Post.date_posted.desc()).all()

    return render_template("admin_dashboard.html", users=users, posts=posts)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
