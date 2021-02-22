from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, InputRequired 
from wtforms import PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, ValidationError, Regexp
from blog.models import User
from flask import flash

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,8}$', message="your password should be between 6 and 8 charactor long")])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')
	#新加入
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			flash('Username already exist. Please choose a different one.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			flash('Email already exist. Please choose a different one.')
	#def validate_password(self, password):


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')
	'''
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if not user:
			raise ValidationError('username not exits')
	'''
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			flash("useless email")
			
class CommentForm(FlaskForm):
	comment = StringField('Comment', validators=[InputRequired()])
	submit = SubmitField('Post comment')
