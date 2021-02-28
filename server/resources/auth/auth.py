import os
from flask import jsonify, request, Blueprint, session
from flask_restful import abort
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from database.models.user import User
from database.models.profile import Profile
from database.db import db

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    email, password, fullname = dict(request.get_json(force=True)).values()
    # print(email, password, fullname)
    if email == "" or password == "" or fullname == "":
        abort(400, msg="이메일, 패스워드, 이름은 NULL일 수 없습니다.")
    elif User.query.filter_by(email=email).first():
        return jsonify(status="fail", msg=f"{email}는 이미 등록된 계정입니다."), 400

    user = User(email, password, fullname)
    db.session.add(user)
    db.session.commit()

    profile = Profile(user.id, user.fullname)
    db.session.add(profile)
    db.session.commit()
    return jsonify(status="success", message=f"Successfully Registered: {email}")


@auth.route("/login", methods=["POST"])
def login():
    email, password = dict(request.get_json(force=True)).values()
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return (
            jsonify(status="fail", msg="아이디 또는 비밀번호를 확인하세요."),
            400,
        )
    # 세션 방식
    # user_id = session.get("user_id")
    # # 기존에 로그인한 계정이 있다면
    # if user_id:
    #     return (
    #         jsonify(
    #             status="fail",
    #             message="Invalid access: already logined",
    #         ),
    #         401,
    #     )
    # session["user_id"] = email
    # return jsonify(status="success", session=session.get("user_id"))
    response = jsonify(
        status="success", user={"id": user.id, "fullname": user.fullname}
    )
    access_token = create_access_token(identity=user.id)
    set_access_cookies(response, access_token)
    return response


@auth.route("/logout", methods=["POST"])
def logout():
    response = jsonify(status="success")
    # accessToken Cookie를 삭제한다.
    unset_jwt_cookies(response)
    return response


@auth.route("/user", methods=["POST"])
@jwt_required()
def get_user():
    identity = get_jwt_identity()
    if not identity:
        abort(401, status="fail", msg="로그인이 필요합니다.")
    user = db.session.query(User).filter_by(id=identity).first()
    return jsonify(status="success", user={"id": identity, "fullname": user.fullname})


# 세션 방식
# @auth.route("/logout")
# def logout():
#     user_id = session.get("user_id")
#     print(user_id)
#     # 기존에 로그인한 계정이 없다면
#     if not user_id:
#         return (
#             jsonify(
#                 status="fail",
#                 message="Invalid access: there is no account to log out.",
#             ),
#             401,
#         )
#     session.pop("user_id", None)
#     return jsonify(status="success")

# 세션 방식
# @auth.before_request
# def set_session_permanent():
#     session.permanent = True
#     auth.permanent_session_lifetime = timedelta(minutes=5)