from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.forms import PostForm
from app.models import Post, likes
from app import db, cache
from sqlalchemy import and_

post = Blueprint('post', __name__)

@post.route("/")
@post.route("/home")
@cache.cached(timeout=60)

def home():
    page = request.args.get('page', 1, type=int)
    paginated_posts = Post.query.paginate(page=page, per_page=5)
    
    # Build the list of posts with like counts
    posts_with_likes = [
        {"post": post, "like_count": db.session.query(likes).filter(likes.c.post_id == post.id).count()}
        for post in paginated_posts.items
    ]
    
    # Pass the pagination object and the processed posts
    return render_template(
        "index.html",
        posts=posts_with_likes,
        pagination=paginated_posts,
    )

@post.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Validate content directly from the form
        if not form.content.data.strip():
            flash("Post content cannot be empty!", "danger")
            return render_template("new_post.html", form=form)

        # Create a new post instance
        post = Post(title=form.title.data, content=form.content.data.strip(), author=current_user)
        db.session.add(post)
        db.session.commit()


        flash("Your post has been created!", "success")
        return redirect(url_for("post.home"))

    return render_template("new_post.html", form=form)



@post.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Check if the user already liked the post
    already_liked = db.session.query(likes).filter(
        and_(likes.c.user_id == current_user.id, likes.c.post_id == post.id)
    ).first()
    
    if already_liked:
        # Unlike the post if already liked
        db.session.execute(
            likes.delete().where(
                and_(likes.c.user_id == current_user.id, likes.c.post_id == post.id)
            )
        )
    else:
        # Add a like for the post
        db.session.execute(
            likes.insert().values(user_id=current_user.id, post_id=post.id)
        )
    
    db.session.commit()
    flash("Post liked/unliked successfully", "success")
    return redirect(url_for("post.home"))

@post.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    results = Post.query.filter(Post.title.contains(query) | Post.content.contains(query)).all()
    return render_template("search_results.html", query=query, results=results)


@post.route("/post/<int:post_id>/comment", methods=["POST"])
@login_required
def add_comment(post_id):
    content = request.form.get("content")
    parent_id = request.form.get("parent_id")  # For threaded replies
    new_comment = Comment(content=content, post_id=post_id, user_id=current_user.id, parent_id=parent_id)
    db.session.add(new_comment)
    db.session.commit()
    flash("Comment added!", "success")
    return redirect(url_for("post.view_post", post_id=post_id))


@post.route("/post/<int:post_id>")
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id, parent_id=None).all()
    return render_template("view_post.html", post=post, comments=comments)


