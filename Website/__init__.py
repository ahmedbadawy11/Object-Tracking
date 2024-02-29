from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
#-----------------------------------------------------------------------------------

import logging
from logging.handlers import RotatingFileHandler

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)

# Create a formatter and set the format for the logs
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(handler)

# Example usage:
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')




#----------------------------------------------------------------------------------------

db=SQLAlchemy()
DB_Name='database.db'
UPLOAD_FOLDER = 'Website/static/uploads' 
def create_app():
    app = Flask(__name__,static_folder='static')
    app.config["SECRET_KEY"]='kjhfdghjklfhjkl'
    app.config['SQLALCHEMY_DATABASE_URI']=  f'sqlite:///{DB_Name}'

     #Set the upload folder configuration option
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)

    from .auth import auth
    from .view import views


    app.register_blueprint(auth,Url_prefix='/')
    
    app.register_blueprint(views,Url_prefix='/')

    from  .models import user 

    
    with app.app_context():
        Create_DB()
    # Create_DB(app)
        
    login_manager=LoginManager()
    login_manager.login_view='auth.login'  # where we should go if we didn't login
    login_manager.init_app(app) # tell the login_manager which app we use

    @login_manager.user_loader
    def load_User(id):
        return user.query.get(int(id))


    return app


def Create_DB():

    if not path.exists('Website/' + DB_Name):
        db.create_all()
        print('Created Database!')


# with app.app_context():
#     create_db()