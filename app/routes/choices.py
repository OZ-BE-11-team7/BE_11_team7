# routes/choices.py

from flask import Blueprint, request, jsonify
from models import db, Choice
from datetime import datetime
from sqlalchemy.sql import func

choice_bp = Blueprint('choices', __name__, url_prefix='/choices')

@choice_bp.route('/<int:question_id>', methods=['GET'])
def get_choices(question_id):
    choices = Choice.query.filter_by(question_id=question_id, is_active=True).order_by(Choice.sqe).all()
    return jsonify([
        {
            'id': c.id,
            'content': c.content,
            'sqe': c.sqe
        } for c in choices
    ])

@choice_bp.route('/', methods=['POST'])
def create_choice():
    data = request.get_json()
    choice = Choice(
        question_id=data['question_id'],
        content=data['content'],
        sqe=data.get('sqe', 0),
        is_active=True,
        created_at=func.now(),
        updated_at=func.now()
    )
    db.session.add(choice)
    db.session.commit()
    return jsonify({'message': 'Choice created', 'id': choice.id}), 201


@choice_bp.route('/<int:choice_id>', methods=['PUT'])
def update_choice(choice_id):
    data = request.get_json()
    choice = Choice.query.get_or_404(choice_id)
    choice.content = data.get('content', choice.content)
    choice.sqe = data.get('sqe', choice.sqe)
    choice.updated_at = func.now()
    db.session.commit()
    return jsonify({'message': 'Choice updated'})

@choice_bp.route('/<int:choice_id>', methods=['DELETE'])
def delete_choice(choice_id):
    choice = Choice.query.get_or_404(choice_id)
    choice.is_active = False
    choice.updated_at = func.now()
    db.session.commit()
    return jsonify({'message': 'Choice soft-deleted'})

