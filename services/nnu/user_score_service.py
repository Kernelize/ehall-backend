import asyncio

import aiohttp
from aiohttp import CookieJar

from utils.nnu.cas_cache_utils import get_mod_auth_cas
from utils.common_utils import get_ehall_url, get_ehallapp_url
from utils.request_utils import default_header

from services.nnu.score_rank_service import get_score_rank


async def get_user_score(school_name: str, token: str, semester: str, amount: int, is_need_rank: bool) -> tuple[dict, int]:
    ehallapp_url = get_ehallapp_url(school_name)
    ehall_url = get_ehall_url(school_name)

    mod_auth_cas = get_mod_auth_cas(school_name, token)
    if mod_auth_cas is None:
        return {'status': 'error', 'message': 'Failed to get user score. authToken is probably invalid.'}, 401

    async with aiohttp.ClientSession(cookie_jar=CookieJar(unsafe=True)) as s:
        s.cookie_jar.update_cookies({'MOD_AUTH_CAS': mod_auth_cas})
        s.headers.update(default_header)
        if 'Referer' in s.headers:
            del s.headers['Referer']

        async with s.get(ehall_url + '/appShow?appId=4768574631264620') as response:
            if response.status != 200:
                return {'status': 'retry', 'message': 'Failed to get user score.Please try again'}, 402

        query_score_url = ehallapp_url + '/jwapp/sys/cjcx/modules/cjcx/xscjcx.do'
        query_score_data = get_query_score_data(semester, amount)
        async with s.post(query_score_url, data=query_score_data) as response:
            if response.status != 200:
                return {'status': 'retry', 'message': 'Failed to get user score.Please try again'}, 402
            original_json = await response.json()

        result_data = await transform_data_and_add_rankings(school_name, token, original_json, is_need_rank)

    return result_data, 200


def get_query_score_data(semester: str, amount: int):
    if semester == 'all':
        query_score_data = {
            'querySetting': '[{"name": "SFYX", "caption": "是否有效", "linkOpt": "AND", "builderList": "cbl_m_List","builder": "m_value_equal", "value": "1", "value_display": "是"},{"name": "SHOWMAXCJ", "caption": "显示最高成绩", "linkOpt": "AND", "builderList": "cbl_String","builder": "equal", "value": 0, "value_display": "否"}]',
            '*order': '-XNXQDM, -KCH, -KXH',
            'pageSize': amount,
            'pageNumber': 1
        }
        return query_score_data
    else:
        query_score_data = {
            'querySetting': '[{"name":"XNXQDM","value":"' + semester + '","linkOpt":"and","builder":"m_value_equal"},{"name":"SFYX","caption":"是否有效","linkOpt":"AND","builderList":"cbl_m_List","builder":"m_value_equal","value":"1","value_display":"是"}]',
            '*order': 'KCH,KXH',
            'pageSize': amount,
            'pageNumber': 1
        }
        return query_score_data


async def transform_data_and_add_rankings(school_name, token, original_json, isneedrank):
    result = {
        "status": "OK",
        "message": "User score retrieved successfully",
        "totalCount": original_json["datas"]["xscjcx"]["totalSize"],
        "data": []
    }

    for row in original_json.get("datas", {}).get("xscjcx", {}).get("rows", []):
        course_data = {
            "courseName": row.get("XSKCM", "Unknown Course"),
            "courseID": row.get("KCH", ""),
            "classID": row.get("JXBID", ""),
            "examTime": row.get("KSSJ", ""),
            "totalScore": row.get("ZCJ", 0),
            "gradePoint": str(round(row.get("XFJD", 0), 1)),
            "regularScore": row.get("PSCJ", ""),
            "midScore": row.get("QZCJ", ""),
            "finalScore": row.get("QMCJ", ""),
            "regularPercent": row.get("PSCJXS", ""),
            "midPercent": row.get("QZCJXS", ""),
            "finalPercent": row.get("QMCJXS", ""),
            "courseType": row.get("KCXZDM_DISPLAY", ""),
            "courseCate": row.get("KCLBDM_DISPLAY", ""),
            "isRetake": row.get("CXCKDM_DISPLAY", ""),
            "credits": row.get("XF", 0),
            "gradeType": row.get("DJCJLXDM_DISPLAY", ""),
            "semester": row.get("XNXQDM", ""),
            "department": row.get("KKDWDM_DISPLAY", "")
        }

        other_scores = {}
        for i in range(1, 9):
            qtcj_key = f"QTCJ{i}"
            qtcj_value = row.get(qtcj_key)
            if qtcj_value:
                other_scores[f"otherScore{i}"] = qtcj_value
        course_data.update(other_scores)

        result["data"].append(course_data)

    if isneedrank:
        ranking_tasks = [get_score_rank(school_name, token, course["courseID"], course["classID"], course["semester"]) for
                         course in
                         result["data"]]

        rankings = await asyncio.gather(*ranking_tasks)

        for i, (rank_info, _) in enumerate(rankings):
            result["data"][i]["courseRank"] = rank_info["data"]

    return result
