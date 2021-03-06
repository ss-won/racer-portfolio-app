import os
import config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import (
    JWTManager,
    get_jwt_identity,
    get_jwt,
    create_access_token,
    set_access_cookies,
)
from datetime import datetime, timedelta, timezone
from database.db import db

migrate = Migrate()

# auth blueprint 객체
from resources.auth.auth import auth
from resources.auth.auth import jwt
from resources.portfolio.education import EducationApi
from resources.portfolio.awards import AwardsApi
from resources.portfolio.project import ProjectApi
from resources.portfolio.certificate import CertificateApi
from resources.portfolio.profile import ProfileApi


def set_api_resources(api):
    api.add_resource(EducationApi, "/education/<user_id>", "/education/<user_id>/<id>")
    api.add_resource(AwardsApi, "/awards/<user_id>", "/awards/<user_id>/<id>")
    api.add_resource(ProjectApi, "/project/<user_id>", "/project/<user_id>/<id>")
    api.add_resource(
        CertificateApi, "/certificate/<user_id>", "/certificate/<user_id>/<id>"
    )
    api.add_resource(ProfileApi, "/profile", "/profile/<user_id>")


def create_app():
    # Flask 객체 app 생성 및 config 변수 적용
    app = Flask(__name__, static_url_path="/static")
    CORS(app, supports_credentials=True)
    # app object에 config 적용
    app.config.from_object(config)
    # jwt 적용을 위한 JMTManager 적용
    jwt.init_app(app)
    # auth 객체 blueprint 등록
    app.register_blueprint(auth, url_prefix="/auth")
    # api 설정 및 적용
    api = Api(app)
    set_api_resources(api)
    # db 적용 및 migrate
    db.init_app(app)
    db.create_all(app=app)
    migrate.init_app(app, db)

    # JWT 암시적 로그인 연장을 위한 코드
    # app에 대한 모든 HTTP request 요청 실행 후 refresh
    # 여부를 확인하고 refresh 한다.
    @app.after_request
    def add_header(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            # 현재 accessToken의 expire time이 30분 미만 남았을 때
            # accessToken을 refresh 시켜준다.
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            # 유효한 Access Token이 아닐 때는 기존 response를 그대로 보낸다.
            print("error")
            return response

    return app
