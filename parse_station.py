# # coding: utf-8
#
# import re
# import requests
# from pprint import pprint
# import time
# headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
#          , 'Connection':'keep-alive'}
#
# url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9050'
#
# response = requests.get(url=url, verify=False, headers = headers)
#
# stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
#
# pprint(dict(stations),indent=4)
