from flask import render_template, url_for, flash
from blog import app
from blog.models import User, Post, Comment
from blog import db
from flask import request, redirect
from blog.forms import RegistrationForm, CommentForm
from blog.forms import LoginForm
from flask_login import login_user, login_required, current_user, logout_user
from blog.views import AdminView

@app.route("/")
def hello():
	return 'hello world'

@app.route("/home")
def home():
	posts = Post.query.all()
	return render_template('home.html', posts=posts)

@app.route("/about")
def about():
	return render_template('about.html', title='about')

@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	comments = Comment.query.filter(Comment.post_id == post.id)
	form = CommentForm()
	return render_template('post.html', post=post, comments=comments, form=form)

@app.route('/post/<int:post_id>/comment', methods=['GET', 'POST'])
@login_required
def post_comment(post_id):
	post = Post.query.get_or_404(post_id)
	form = CommentForm()
	if form.validate_on_submit():
		db.session.add(Comment(content=form.comment.data, post_id=post.id, author_id=current_user.id))
		db.session.commit()
		flash("Your comment has been added to the post", "success")
		return redirect(f'/post/{post.id}')
	comments = Comment.query.filter(Comment.post_id == post.id)
	return render_template('post.html', post=post, comments=comments, form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	
	if current_user.is_authenticated:
		flash('you have loged in your account')
		return redirect(url_for('home'))

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(url_for('home'))
		else:
			flash('Invalid email address or password.')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/index")
def index():
	#admin = AdminView(User, current_user)
	return render_template('admin/index.html')











