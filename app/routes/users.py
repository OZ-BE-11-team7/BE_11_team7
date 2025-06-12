# routes/users.py

from flask import Blueprint, request, jsonify
from models import db, User, AgeEnum, GenderEnum
from datetime import datetime

user_bp = Blueprint('users', __name__, url_prefix='/users')

# 사용자 전체 조회
@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            'id': u.id,
            'name': u.name,
            'age': u.age.value,
            'gender': u.gender.value,
            'email': u.email,
            'created_at': u.created_at
        } for u in users
    ])

# 단일 사용자 조회
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'age': user.age.value,
        'gender': user.gender.value,
        'email': user.email,
        'created_at': user.created_at
    })

# 사용자 등록
@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()

    try:
        user = User(
            name=data['name'],
            age=AgeEnum(data['age']),
            gender=GenderEnum(data['gender']),
            email=data['email'],
            created_at=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created', 'id': user.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
