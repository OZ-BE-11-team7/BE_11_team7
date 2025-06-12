# routes/images.py

from flask import Blueprint, request, jsonify
from models import db, Image, ImageTypeEnum
from datetime import datetime

image_bp = Blueprint('images', __name__, url_prefix='/images')

# 이미지 목록 조회
@image_bp.route('/', methods=['GET'])
def get_images():
    images = Image.query.all()
    return jsonify([
        {
            'id': i.id,
            'url': i.url,
            'type': i.type.value,
            'created_at': i.created_at
        } for i in images
    ])

# 이미지 단건 조회
@image_bp.route('/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.get_or_404(image_id)
    return jsonify({
        'id': image.id,
        'url': image.url,
        'type': image.type.value,
        'created_at': image.created_at
    })

# 이미지 등록 (파일 업로드 없이 URL만 받는 구조)
@image_bp.route('/', methods=['POST'])
def create_image():
    data = request.get_json()

    try:
        image = Image(
            url=data['url'],
            type=ImageTypeEnum(data['type']),
            created_at=datetime.utcnow()
        )
        db.session.add(image)
        db.session.commit()
        return jsonify({'message': 'Image created', 'id': image.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
