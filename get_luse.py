import requests


def get_luse(x_pos, y_pos):

    # chatgpt_api_keys = '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'
    url = f"https://lohas.taichung.gov.tw/arcgis/rest/services/Tiled3857/LandAdminNew3857/MapServer/2/query?f=json&geometry=%7B%22spatialReference%22%3A%7B%22wkid%22%3A4326%7D%2C%22x%22%3A{str(x_pos)}%2C%22y%22%3A{str(y_pos)}%7D&geometryPrecision=7&outFields=AA46%2CLUSE&geometryType=esriGeometryPoint&token=aVwX13YUhVcklKu0cfl565XRdT1XL5vJMmcNLfROJ07HG4NFdfLzwzAniYX3yJI_DSFp2a_LJ7GGygmmx4tO3g.."

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "lohas.taichung.gov.tw",
        "Origin": "https://mcgbm.taichung.gov.tw",
        "Referer": "https://mcgbm.taichung.gov.tw/",
        "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Access the response data in JSON format
        json_data = response.json()
        # Process the JSON data as needed
        # print(json_data)
    else:
        json_data = "None"
        print("Error: Request failed with status code", response.status_code)
    if json_data['features']:
        return json_data['features'][0]['attributes']['LUSE']
    else:
        print("如未登錄或地籍分割合併中會查無資料")
        return None


x = 120.679611
y = 24.188629
luse_result = get_luse(x, y)
print(f"the result is: {luse_result}")
