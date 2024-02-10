import requests

from utils.common_utils import get_ehall_url
from utils.request_utils import default_header


def get_user_info(school_name: str, mod_auth_cas: str) -> tuple[dict, int]:
    # check if school is supported
    ehall_url = get_ehall_url(school_name)
    if ehall_url is None:
        return {'status': 'error', 'message': f'{school_name} is not supported'}, 400

    # get user info
    s = requests.Session()
    s.cookies.set('MOD_AUTH_CAS', mod_auth_cas)
    s.headers.update(default_header)

    query_url = ehall_url + '//jsonp/ywtb/info/getUserInfoAndSchoolInfo.json'
    response = s.get(query_url, verify=False)

    # check if the response is valid, and get 'username', 'userid', 'userType', 'userDepartment',  'userSex'
    if response.status_code != 200:
        return {'status': 'error', 'message': 'Failed to get user info.MOD_AUTH_CAS is probably invalid.'}, 400
    try:
        user_info_orig = response.json()['data']
    except KeyError:
        return {'status': 'error', 'message': 'Failed to get user info.MOD_AUTH_CAS is probably invalid.'}, 400
    except Exception as e:
        return {'status': 'error', 'message': f'Unknown: {str(e)}'}, 400
    user_info: dict = {'status': 'OK', 'message': 'User info retrieved successfully',
                       'data': {
                           'username': user_info_orig['userName'], 'userid': user_info_orig['userId'],
                           'userType': user_info_orig['userTypeName'],
                           'userDepartment': user_info_orig['userDepartment'],
                           'userSex': user_info_orig['userSex']
                       }
                       }
    return user_info, 200