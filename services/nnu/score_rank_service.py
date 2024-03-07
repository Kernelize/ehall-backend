import aiohttp
import asyncio

from aiohttp import CookieJar

from utils.common_utils import get_ehallapp_url, get_ehall_url
from utils.nnu.cas_cache_utils import get_mod_auth_cas
from utils.request_utils import default_header


async def get_score_rank(school_name: str, token: str, course_id: str, class_id: str, semester: str) -> tuple[
    dict, int]:
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

        # First, get user id
        query_user_info_url = ehall_url + '/jsonp/ywtb/info/getUserInfoAndSchoolInfo'
        async with s.get(query_user_info_url) as response:
            user_info = await response.json()
            user_id = user_info['data']['userId']
        async with s.get(ehall_url + '/appShow?appId=4768574631264620') as response:
            if response.status != 200:
                return {'status': 'retry', 'message': 'Failed to get score rank.Please try again'}, 402

        # Define tasks for simultaneous requests
        tasks = [
            s.post(ehallapp_url + '/jwapp/sys/cjcx/modules/cjcx/jxbcjtjcx.do',
                   data={'JXBID': class_id, 'XNXQDM': semester, 'TJLX': '01'}),
            s.post(ehallapp_url + '/jwapp/sys/cjcx/modules/cjcx/jxbcjtjcx.do',
                   data={'JXBID': '*', 'XNXQDM': semester, 'KCH': course_id, 'TJLX': '02'}),
            s.post(ehallapp_url + '/jwapp/sys/cjcx/modules/cjcx/jxbcjfbcx.do',
                   data={'JXBID': class_id, 'XNXQDM': semester, 'TJLX': '01', '*order': '+DJDM'}),
            s.post(ehallapp_url + '/jwapp/sys/cjcx/modules/cjcx/jxbcjfbcx.do',
                   data={'JXBID': '*', 'XNXQDM': semester, 'KCH': course_id, 'TJLX': '02', '*order': '+DJDM'}),
            s.post(ehallapp_url + '/jwapp/sys/cjcx/modules/cjcx/jxbxspmcx.do',
                   data={'XH': user_id, 'JXBID': class_id, 'XNXQDM': semester, 'TJLX': '01'}),
            s.post(ehallapp_url + '/jwapp/sys/cjcx/modules/cjcx/jxbxspmcx.do',
                   data={'XH': user_id, 'JXBID': '*', 'XNXQDM': semester, 'KCH': course_id, 'TJLX': '02'})
        ]
        responses = await asyncio.gather(*tasks)

        # Parsing responses
        class_score_response = await responses[0].json()
        school_score_response = await responses[1].json()
        class_people_response = await responses[2].json()
        school_people_response = await responses[3].json()
        class_rank_response = await responses[4].json()
        school_rank_response = await responses[5].json()

        # Structure the response data
        res_data = {"status": "OK", "message": "Score rank retrieved successfully", "data": {
            "class": {
                "highScore": class_score_response['datas']['jxbcjtjcx']['rows'][0]['ZGF'],
                "lowScore": class_score_response['datas']['jxbcjtjcx']['rows'][0]['ZDF'],
                "averageScore": class_score_response['datas']['jxbcjtjcx']['rows'][0]['PJF'],
                "numAbove90": class_people_response['datas']['jxbcjfbcx']['rows'][0].get('DJSL', 0),
                "rank": class_rank_response['datas']['jxbxspmcx']['rows'][0]['PM'],
                "totalPeopleNum": class_rank_response['datas']['jxbxspmcx']['rows'][0]['ZRS']
            },
            "school": {
                "highScore": school_score_response['datas']['jxbcjtjcx']['rows'][0]['ZGF'],
                "lowScore": school_score_response['datas']['jxbcjtjcx']['rows'][0]['ZDF'],
                "averageScore": school_score_response['datas']['jxbcjtjcx']['rows'][0]['PJF'],
                "numAbove90": school_people_response['datas']['jxbcjfbcx']['rows'][0].get('DJSL', 0),
                "rank": school_rank_response['datas']['jxbxspmcx']['rows'][0]['PM'],
                "totalPeopleNum": school_rank_response['datas']['jxbxspmcx']['rows'][0]['ZRS']
            }
        }}

        # Process class and school in one loop for additional grade distribution details
        for i in range(len(class_people_response['datas']['jxbcjfbcx']['rows'])):
            grade_key = f'numAbove{90 - i * 10}' if i != 4 else 'numBelow60'
            res_data['data']['class'][grade_key] = class_people_response['datas']['jxbcjfbcx']['rows'][i].get('DJSL', 0)
            res_data['data']['school'][grade_key] = school_people_response['datas']['jxbcjfbcx']['rows'][i].get('DJSL',
                                                                                                                0)

        return res_data, 200
