from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import sys
import os
sys.path.append("..")

app = Flask(__name__, template_folder='templates')
app.config.from_object('your_config_module')  # or set config directly
db = SQLAlchemy(app)
migrate = Migrate(app, db)

migrate = Migrate(app, db)
handler = Manager(app)
handler.add_command('db', MigrateCommand)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
class Transfers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender_account = db.Column(db.String(100), nullable=False)
    receiver_bank = db.Column(db.String(100), nullable=False)
    receiver_account = db.Column(db.String(100), nullable=False)
    receiver_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text)
    frequency = db.Column(db.Enum('monthly', 'daily', 'weekly', name='frequency_types'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
 
if __name__ == '__main__':
    handler.run()