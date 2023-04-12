import requests
import json
import re
import time
import pandas as pd
import urllib.parse
import base64
import datetime
import numpy as np

now = datetime.datetime.now()
year_month_day_time = now.strftime("%Y_%m_%d")

# 設定 API 網址與 POST 資料

Lcdetypename = {
    "lcde_1": "本國人",
    "lcde_2": "外國人",
    "lcde_3": "國有",
    "lcde_4": "省市",
    "lcde_5": "縣市",
    "lcde_6": "鄉鎮市",
    "lcde_7": "本國私法人",
    "lcde_8": "外國法人",
    "lcde_9": "祭祀公業",
    "lcde_a": "其他",
    "lcde_b": "銀行法人",
    "lcde_c": "大陸地區自然人",
    "lcde_d": "大陸地區法人"
}

check_status_list = ['一般道路', '旱田', '道路相關設施', '未使用地']


def get_lcdetype_flag(json_dict):
    str_ = ""

    if not isinstance(json_dict, dict):
        str_ = "查無權利人資料"
    else:
        lcdetstr = ""
        s1 = 0
        for applier, a_val in json_dict.items():
            if "lcde_1" in applier:
                if isinstance(a_val, float) and a_val > 0:
                    s1 += a_val

        if s1 > 0:
            if s1 <= 1:
                str_ += Lcdetypename["lcde_1"] + ":" + str(round(s1 * 100, 2)) + "%"
            else:
                str_ += Lcdetypename["lcde_1"] + ":100%"

        for applier, a_val in json_dict.items():
            if "lcde_" in applier:
                if "lcde_1" not in applier:
                    if isinstance(a_val, float) and a_val > 0:
                        if a_val <= 1:
                            if str_:
                                str_ += "<br>"
                            str_ += Lcdetypename[applier] + ":" + str(round(a_val * 100, 2)) + "%"
                        else:
                            if str_:
                                str_ += "<br>"
                            str_ += Lcdetypename[applier] + ":100%"

    return str_


def location_query(l_payload):
    LocationQuery_url = 'https://api.nlsc.gov.tw/MapSearch/LocationQuery'
    LocationQuery_header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '29',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'api.nlsc.gov.tw',
        'Origin': 'https://maps.nlsc.gov.tw',
        'Referer': 'https://maps.nlsc.gov.tw/',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    LocationQuery_payload = l_payload
    # 發送 POST 請求
    LocationQuery_response = requests.post(LocationQuery_url, data=LocationQuery_payload, headers=LocationQuery_header)
    LocationQuery_result = LocationQuery_response.text
    LocationQuery_result = LocationQuery_result.split("@")
    # 找出行政區及使用現況
    print(LocationQuery_result[1])
    pattern = r'行政區:(.*?)\<br'
    l_own_area = re.search(pattern, LocationQuery_result[1])
    l_own_area = l_own_area.group(1)
    pattern = r'現況調查:(.*?)\(2'
    l_status = re.search(pattern, LocationQuery_result[1])
    l_status = l_status.group(1)
    return l_own_area.strip(), l_status.strip()


def get_land_info(get_payload):
    get_land_info_url = "https://api.nlsc.gov.tw/S09_Ralid/getLandInfo"
    get_land_info_payload = get_payload
    get_land_info_header = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "32",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "api.nlsc.gov.tw",
        "Origin": "https://maps.nlsc.gov.tw",
        "Referer": "https://maps.nlsc.gov.tw/",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    getLandInfo_response = requests.post(get_land_info_url, data=get_land_info_payload, headers=get_land_info_header)
    getLandInfo_result = json.loads(getLandInfo_response.text)
    l_area = getLandInfo_result['ralid']['AA10']
    l_price = getLandInfo_result['ralid']['AA16']
    l_owner = get_lcdetype_flag(getLandInfo_result['lcdetype'])
    t_value = getLandInfo_result['ralid']['AA16'] * getLandInfo_result['ralid']['AA10']
    return l_area, l_price, t_value, l_owner.strip()


def get_type(x_pos, y_pos):
    url = f"https://luz.tcd.gov.tw/tcdgm/ws_identify.ashx?token=U65yWjl1zDnIAUMdC3gzyjERU-RhDGj4zNqwXSHvDooEsmBdJpu5ENgQGb8WfB2Y-f940BPEYguPgPxNzLUzHQ..&LAYERS=5%2C3%2C6&X={str(x_pos)}&Y={str(y_pos)}&Z=TWW"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": f"ExtentJS={str(y_pos)},{str(x_pos)},19; ASP.NET_SessionId=nyymmbs0k4vphc0t51fdgqoy; _ga=GA1.3.1580569695.1680751244",
        "referer": "https://nsp.tcd.gov.tw/tcdgm/Default.aspx",
        "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            type_by_json = json.loads(response.text)
            print(type_by_json)
            if 'success' in type_by_json:
                time.sleep(10)
                response = requests.get(url, headers=headers)
                type_by_json = json.loads(response.text)

            result_head = type_by_json["5"]["features"]
            if result_head:
                result_body = type_by_json["5"]["features"][0]["properties"]
                # print(f'Result: {result_body}')
                type_use_area = result_body["使用分區"]
                type_plan_name = result_body["計畫區名稱"]
                print(f"使用分區: {type_use_area}")
                print(f"計畫區名稱: {type_plan_name}")
                return type_use_area, type_plan_name
            else:
                print("Empty type")
                type_use_area = '主要幹道/國有/未分類'
                type_plan_name = '臺中市都市計畫主要計畫'
                return type_use_area, type_plan_name
        else:
            type_use_area = '失敗:未取得資訊'
            type_plan_name = '失敗:未取得資訊'
            print(f"Fail code：{response.status_code}")
            return type_use_area, type_plan_name
    except Exception as e:
        raise e
        type_use_area = f"{str(e)}, {x_pos}, {y_pos}"
        type_plan_name = f"{str(e)}, {x_pos}, {y_pos}"
        return type_use_area, type_plan_name


def get_info(input_array, x_pos, y_pos):
    # '120.711271,24.160243' ;120.702043,24.170301
    # qryTile
    score = {}
    qryTile_url = f'https://landmaps.nlsc.gov.tw/S_Maps/qryTileMapIndex?callback=jQuery&type=2&flag=1&city=B&x={str(x_pos)}&y={str(y_pos)}'
    qryTile_headers = {
        'Referer': 'https://maps.nlsc.gov.tw/',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    response = requests.get(qryTile_url, headers=qryTile_headers)
    res_json = response.content.decode('utf-8')
    pattern = r'\[\[(.*?)\]\]'
    match = re.search(pattern, res_json).group(1)
    match = json.loads(match)
    try:
        sect = match['sect'].strip()
        landno = match['landno'].strip()
        landstr = match['sectStr'].strip()
        decoded_str = base64.b64decode(landstr).decode("utf-8").strip()
        # getLandInfo
    except Exception as E:
        print(E.args)
        return input_array
    print(f'地段為:{sect}')
    print(f'地號為:{landno}')
    sect_landno = sect + '-' + landno
    try:
        landno_array = np.array(input_array).T[1]
    except:
        pass

    query_pos = {'center': str(x_pos) + ',' + str(y_pos)}
    land_payload = {'city': 'B', 'sect': sect, 'landno': landno}

    # 確認是否真實為一般道路/旱田/道路相關設施
    if not input_array or (sect_landno not in landno_array):
        # LocationQuery
        own_area, land_status = location_query(query_pos)
        # 土地調查
        land_area, land_price, total_value, land_owner = get_land_info(land_payload)
        score[land_status] = 1
        use_area, plan_name = get_type(x_pos, y_pos)
        input_array.append(
            [decoded_str, sect_landno, own_area, land_status, land_area, land_price, total_value, land_owner,
             np.round(x_pos, 6), np.round(y_pos, 6), score, use_area, plan_name])

        print(f"面積為:{land_area} 平方公尺")
        print(f"單價為:{land_price} 元/平方公尺")
        print(f"擁有者:{land_owner}")
        print(f"總值:{total_value}元")
        print(f"土地調查為:{land_status}")
        print("------***新增***------")

        return input_array
    elif sect_landno in landno_array:
        # print(f"{sect}在{input_array['地號']}")
        print(f'------***重複地號，確認中***------')
        print(np.where(landno_array == sect_landno))
        idx_check = np.where(landno_array == sect_landno)[0][0]
        own_area, land_status = location_query(query_pos)
        if land_status not in input_array[idx_check][-3]:
            input_array[idx_check][-3][land_status] = 1
        else:
            input_array[idx_check][-3][land_status] += 1
        max_score_land_status = max(input_array[idx_check][-3], key=input_array[idx_check][-3].get)
        print(f'本次:{land_status}->最高分:{max_score_land_status}')
        input_array[idx_check][3] = max_score_land_status
        return input_array


# data_set = {'地段名':[], '地段':[], '地號':[],'行政區':[], '狀態':[], '面積':[], '估值':[], '總值':[], '使用者':[]}
col_names = ['地段名', '地段-地號', '行政區', '狀態', '面積', '估值', '總值', '使用者', '座標x', '座標y', 'score', '使用分區', '計畫區']
# debug:120.721069	24.174339
# x_min, x_max = 120.685709, 120.721948
# y_min, y_max = 24.172339, 24.200506
# x, y = 120.685709, 24.172339
x_min, x_max = 120.685709, 120.721948
y_min, y_max = 24.172339, 24.200506
x, y = 120.685709, 24.172339
result_array = []

while True:
    try:
        if x_min < x_max:
            print(f"座標為{x_min, y_min}")
            result_array = get_info(result_array, x_min, y_min)
            print(pd.DataFrame(result_array, columns=col_names))
            # 小數第5位的值約為1.02公尺
            x_min += 0.00004
            time.sleep(0.2)
            # print(f'結果為{result_set}')
            data_len = len(np.array(result_array).T[0])
            if data_len % 10 == 0:
                result_df = pd.DataFrame(result_array, columns=col_names)
                print(result_df)
                print("-----------------------------------------------")
                result_df.to_excel(f'result_{year_month_day_time}.xlsx', index=False, encoding='utf-8')

        elif y_min < y_max:
            y_min += 0.0004
            x_min = x
        else:
            break
    except Exception as E:
        result_df = pd.DataFrame(result_array, columns=col_names)
        print(result_df)
        print("===============================================")
        result_df.to_excel(f'result_{year_month_day_time}.xlsx', index=False, encoding='utf-8')
        print(E.args)
        time.sleep(360)

result_df = pd.DataFrame(result_array, columns=col_names)
print(result_df)
result_df.to_excel(f'result_{year_month_day_time}.xlsx', index=False, encoding='utf-8')
