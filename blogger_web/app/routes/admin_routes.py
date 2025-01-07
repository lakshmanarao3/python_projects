from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, Post, Notification
from app import db

admin = Blueprint("admin", __name__)

@admin.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("post.home"))

    users = User.get_all_users()
    posts = Post.get_all_posts()
    return render_template("admin_dashboard.html", users=users, posts=posts)

@admin.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("post.home"))

    if User.delete_user(user_id):
        Notification.create_notification(
            user_id=current_user.id, message="User deleted successfully."
        )
        flash("User deleted successfully.", "success")
    else:
        flash("Failed to delete user.", "danger")

    return redirect(url_for("admin.dashboard"))

@admin.route("/delete_post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("post.home"))

    if Post.delete_post(post_id):
        Notification.create_notification(
            user_id=current_user.id, message="Post deleted successfully."
        )
        flash("Post deleted successfully.", "success")
    else:
        flash("Failed to delete post.", "danger")

    return redirect(url_for("admin.dashboard"))
@admin.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("post.home"))

    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")

        if username and email:
            user.username = username
            user.email = email
            db.session.commit()
            flash("User updated successfully!", "success")
        else:
            flash("Username and Email are required.", "danger")
        return redirect(url_for("admin.dashboard"))

    return render_template("edit_user.html", user=user)
@admin.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("post.home"))
    
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        
        if not title or not content:
            flash("Title and content cannot be empty!", "danger")
            return redirect(url_for("admin.edit_post", post_id=post_id))
        
        post.title = title
        post.content = content
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("admin.dashboard"))
    
    return render_template("edit_post.html", post=post)

