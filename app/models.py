from app import login_manager
import datetime
from app import db
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin,login_required,current_user

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),index=True,unique=True)
    email=db.Column(db.String(120),index=True,unique=True)
    password_hash=db.Column(db.String(128))
    created_at=db.Column(db.DateTime,default=datetime.datetime.utcnow)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    

    
    @classmethod
    def create_user(cls,username,email,password):
        user=cls(username=username,email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    


class UserInput(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(255),nullable=False)
    created_at=db.Column(db.DateTime,default= datetime.datetime.utcnow)

    def __repr__(self):
        return '{}'.format(self.text)
class ChatResponse(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(255),nullable=False)
    created_at=db.Column(db.DateTime,default= datetime.datetime.utcnow)
    
    def __repr__(self):
        return '<ChatResponse {}'.format(self.text)
class ImageRequest(db.Model):
    __tablename__='image_requests'
    id=db.Column(db.Integer,primary_key=True)
    prompt=db.Column(db.Text)
    image_url=db.Column(db.String(255))
    created_at=db.Column(db.DateTime,default= datetime.datetime.utcnow)
    __table_args__ = (
        db.UniqueConstraint('prompt', name='unique_prompt'),
    )

    