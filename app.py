import logging
import asyncio

from waitress import serve
from flask import Flask, request
from handlers.login_handler import cas_login_handler
from handlers.user_handler import user_info_handler, user_score_handler, score_rank_handler, course_table_handler

app = Flask(__name__)


@app.route('/<school_name>/cas_login', methods=['POST'])
def cas_login(school_name):
    login_data = request.json
    return cas_login_handler(school_name, login_data)


@app.route('/<school_name>/user/info', methods=['GET'])
def user_info(school_name):
    auth_token = request.headers.get('Authorization')
    return user_info_handler(school_name, auth_token)


@app.route('/<school_name>/user/score', methods=['GET', 'POST'])
def user_score(school_name):
    auth_token = request.headers.get('Authorization')
    if request.method == 'GET':
        return user_score_handler(school_name, auth_token, {})
    score_request_data = request.json
    result, status_code = asyncio.run(user_score_handler(school_name, auth_token, score_request_data))
    return result, status_code


@app.route('/<school_name>/user/score_rank', methods=['POST'])
def score_rank(school_name):
    auth_token = request.headers.get('Authorization')
    score_rank_request_data = request.json
    result, status_code = asyncio.run(score_rank_handler(school_name, auth_token, score_rank_request_data))
    return result, status_code


@app.route('/<school_name>/user/course_table', methods=['GET', 'POST'])
def course_table(school_name):
    auth_token = request.headers.get('Authorization')
    if request.method == 'GET':
        return course_table_handler(school_name, auth_token, {})
    course_table_request_data = request.json
    return course_table_handler(school_name, auth_token, course_table_request_data)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8080
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)
    serve(app, host=host, port=port)