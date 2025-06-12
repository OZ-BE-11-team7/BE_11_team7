import enum
from sqlalchemy import Enum
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy


# SQLAlchemy 인스턴스
db = SQLAlchemy()

# ----------------------
# ENUM 정의
# ----------------------
class AgeEnum(enum.Enum):
    teen = 'teen'
    twenty = 'twenty'
    thirty = 'thirty'
    forty = 'forty'
    fifty = 'fifty'

class GenderEnum(enum.Enum):
    male = 'male'
    female = 'female'

class ImageTypeEnum(enum.Enum):
    main = 'main'
    sub = 'sub'

# ----------------------
# 사용자 테이블
# ----------------------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    age = db.Column(Enum(AgeEnum), nullable=False)
    gender = db.Column(Enum(GenderEnum), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    answers = db.relationship('Answer', backref='user', cascade='all, delete-orphan')

# ----------------------
# 이미지 테이블
# ----------------------
class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    type = db.Column(Enum(ImageTypeEnum), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    questions = db.relationship('Question', backref='image', cascade='all, delete-orphan')

# ----------------------
# 질문 테이블
# ----------------------
class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    choices = db.relationship('Choice', backref='question', cascade='all, delete-orphan')

# ----------------------
# 선택지 테이블
# ----------------------
class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    answers = db.relationship('Answer', backref='choice', cascade='all, delete-orphan')

# ----------------------
# 응답 테이블
# ----------------------
class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    choice_id = db.Column(db.Integer, db.ForeignKey('choices.id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
