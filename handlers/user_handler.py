import importlib


def user_info_handler(school_name: str, token: str) -> tuple[dict, int]:
    if token is None:
        return {'status': 'error', 'message': 'authToken not found'}, 400
    service = importlib.import_module(f'services.{school_name}.user_info_service')

    return service.get_user_info(school_name, token)


async def user_score_handler(school_name: str, token: str, requestdata: dict) -> tuple[dict, int]:
    if token is None:
        return {'status': 'error', 'message': 'authToken not found'}, 400
    semester = requestdata.get('semester', "2022-2023-2,2023-2024-1")
    amount = requestdata.get('amount', 10)
    isneedrank = requestdata.get('isNeedRank', False)
    if isneedrank == "true":
        isneedrank = True
    elif isneedrank == "false":
        isneedrank = False
    elif not isinstance(isneedrank, bool):
        return {'status': 'error', 'message': 'isNeedRank must be true or false'}, 400

    service = importlib.import_module(f'services.{school_name}.user_score_service')

    return await service.get_user_score(school_name, token, semester, amount, isneedrank)


async def score_rank_handler(school_name: str, token: str, requestdata: dict) -> tuple[dict, int]:
    if token is None:
        return {'status': 'error', 'message': 'authToken not found'}, 400
    course_id = requestdata.get('courseID', None)
    class_id = requestdata.get('classID', None)
    semester = requestdata.get('semester', None)
    if course_id is None or class_id is None or semester is None:
        return {'status': 'error', 'message': 'necessary args required'}, 400
    service = importlib.import_module(f'services.{school_name}.score_rank_service')

    return await service.get_score_rank(school_name, token, course_id, class_id, semester)


def course_table_handler(school_name: str, token: str, requestdata: dict) -> tuple[dict, int]:
    if token is None:
        return {'status': 'error', 'message': 'authToken not found'}, 400
    semester = requestdata.get('semester', "")
    service = importlib.import_module(f'services.{school_name}.course_table_service')

    return service.get_course_table(school_name, token, semester)
