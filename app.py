from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from models.init_db import db
from views.book_view import book_blueprint
from views.customer_view import customer_blueprint
from views.loan_view import loan_blueprint




app = Flask(__name__, static_url_path='/library_project_updated/static')
CORS(app, origins="http://127.0.0.1:5501")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)
migrate = Migrate(app, db)  # Move Migrate creation here

with app.app_context():
    db.create_all()
# Register blueprints
app.register_blueprint(book_blueprint, url_prefix='/')
app.register_blueprint(customer_blueprint, url_prefix='/')
app.register_blueprint(loan_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True,port=7500)


