# routes/questions.py

from flask import Blueprint, request, jsonify
from models import db, Question, Image
from datetime import datetime
from sqlalchemy.sql import func

question_bp = Blueprint('questions', __name__, url_prefix='/questions')

# 질문 목록 조회
@question_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.filter_by(is_active=True).order_by(Question.sqe).all()
    return jsonify([
        {
            'id': q.id,
            'title': q.title,
            'sqe': q.sqe,
            'image_url': q.image.url if q.image else None
        }
        for q in questions
    ])

# 질문 단건 조회
@question_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get_or_404(question_id)
    return jsonify({
        'id': question.id,
        'title': question.title,
        'sqe': question.sqe,
        'image_url': question.image.url if question.image else None,
        'is_active': question.is_active
    })

# 질문 생성
@question_bp.route('/', methods=['POST'])
def create_question():
    data = request.get_json()
    question = Question(
        title=data['title'],
        sqe=data.get('sqe', 0),
        image_id=data.get('image_id'),  # optional
        is_active=True,
        created_at=func.now(),
        updated_at=func.now()
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({'message': 'Question created', 'id': question.id}), 201

# 질문 수정
@question_bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    data = request.get_json()
    question = Question.query.get_or_404(question_id)

    question.title = data.get('title', question.title)
    question.sqe = data.get('sqe', question.sqe)
    question.image_id = data.get('image_id', question.image_id)
    question.updated_at = func.now()

    db.session.commit()
    return jsonify({'message': 'Question updated'})

# 질문 삭제
@question_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    question.is_active = False
    question.updated_at = func.now()
    db.session.commit()
    return jsonify({'message': 'Question soft-deleted'})
