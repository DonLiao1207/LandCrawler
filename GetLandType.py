import requests

url = "https://nsp.tcd.gov.tw/tcdgm/ws_identify.ashx?token=U65yWjl1zDnIAUMdC3gzyqIcl1gyxVhhVcGbzWt1KM2KHtrIJ7ONPLz-bA3UJlHjAPuuQZyI5lJpWG0oR3vXpw..&LAYERS=5,3,6&X=120.68518944767705&Y=24.199912861334976&Z=TWW"
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cookie": "ExtentJS=24.20099910202824%2C120.67841955212346%2C16; _ga=GA1.3.1580569695.1680751244; ASP.NET_SessionId=csenmeazkz2mkx1cwa1qmjgc",
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

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("请求成功")
    print(response.text)
else:
    print(f"请求失败，错误代码：{response.status_code}")
'''
{
  "3": {
    "features": [],
    "type": "FeatureCollection"
  },
  "5": {
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "GeometryCollection",
          "geometries": []
        },
        "properties": {
          "OBJECTID": "89095",
          "使用分區": "廣場兼停車場",
          "分區簡稱": "廣兼停",
          "計畫區名稱": "臺中市都市計畫主要計畫",
          "資料日期": "",
          "計畫案名稱": "變更台中市都市計畫（己騰空眷村土地變更）細部計畫（公共設施變更部分）",
          "附帶條件": "",
          "資料品質": "",
          "參考面積": "4331.98",
          "變更前分區": "",
          "備註": ""
        }
      }
    ],
    "type": "FeatureCollection"
  },
  "6": {
    "features": [],
    "type": "FeatureCollection"
  }
}
'''
