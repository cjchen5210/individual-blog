from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



app = Flask(__name__)
app.config['SECRET_KEY'] = '3c400ddfd0555aa13e340e5ac481042c68e43f20e9b9ced1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c2015203:Cwj619404244@csmysql.cs.cf.ac.uk:3306/c2015203_Flask'

db = SQLAlchemy(app)

#login
login_manager = LoginManager()
#login_manager.session_protection = 'strong'
#slogin_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return User.get(user_id)



from blog import routes
from blog.models import User, Post, Comment
from blog.views import AdminView

#admin
admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))