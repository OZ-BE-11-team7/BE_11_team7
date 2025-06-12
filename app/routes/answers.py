# routes/answers.py

from flask import Blueprint, request, jsonify
from models import db, Answer, User, Choice
from datetime import datetime
from sqlalchemy.sql import func

answer_bp = Blueprint('answers', __name__, url_prefix='/answers')

@answer_bp.route('/', methods=['POST'])
def submit_answer():
    data = request.get_json()
    user_id = data.get('user_id')
    choice_id = data.get('choice_id')

    if not user_id or not choice_id:
        return jsonify({'error': 'user_id and choice_id are required'}), 400

    answer = Answer(
        user_id=user_id,
        choice_id=choice_id,
        created_at=func.now()
    )
    db.session.add(answer)
    db.session.commit()

    return jsonify({'message': 'Answer submitted', 'id': answer.id}), 201

@answer_bp.route('/user/<int:user_id>', methods=['GET'])
def get_answers_by_user(user_id):
    answers = Answer.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'answer_id': a.id,
            'choice_id': a.choice_id,
            'question_id': a.choice.question_id,
            'choice_content': a.choice.content
        }
        for a in answers
    ])

@answer_bp.route('/stats', methods=['GET'])
def get_answer_stats():
    from sqlalchemy import func
    stats = db.session.query(
        Answer.choice_id,
        func.count(Answer.id)
    ).group_by(Answer.choice_id).all()

    return jsonify([
        {'choice_id': choice_id, 'count': count}
        for choice_id, count in stats
    ])

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'), nullable=False)
    created_at = db.Column(db.DateTime)

    user = db.relationship('User', backref='answers')
    choice = db.relationship('Choice', backref='answers')
