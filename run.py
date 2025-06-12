from app import create_app
from config import db

application = create_app()

if __name__ == '__main__':
    with application.app_context():  # DB 작업 위해 Flask 앱 컨텍스트 사용
        db.create_all()  # 테이블 자동 생성
    application.run(debug=True)  # 디버깅 모드로 실행