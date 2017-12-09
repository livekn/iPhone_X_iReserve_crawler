#coding: utf8
import requests
import json
import time
import datetime

import config as c
config = c.config()

headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"}

def main():
	# 以下以澳門版為例，如果要其他地方版，就讀 config 中不同的國家，例如 config.tw

	while True:
		response = requests.get(config.mo['source_url'], headers=headers)

		# 如果 Apple 不是 return 200，30 秒後重試，常在晚上 Apple 維護網站時發生
		while response.status_code != 200:
			print("Apple response: {}".format(response.status_code))
			print(response.text)
			time.sleep(30)

		data_mo = response.json()
		# data_mo = {"isToday":True,"launchDate":{"zh_MO":"2017 年 11 月 23 日星期四"},"updated":1512796380119,"stores":{"R672":{"MQA82ZA/A":{"availability":{"contract":False,"unlocked":False}},"MQA52ZA/A":{"availability":{"contract":False,"unlocked":True}},"MQA92ZA/A":{"availability":{"contract":False,"unlocked":True}},"MQA62ZA/A":{"availability":{"contract":False,"unlocked":False}}}}}

		available = False

		for store, store_data in data_mo['stores'].items():
			for part_name, part_data in store_data.items():
				if part_data['availability']['contract'] or part_data['availability']['unlocked']:
					available = True
					print("{}: {} available: {}".format(datetime.datetime.now().isoformat(), config.mo['part_name'][part_name], config.mo['store_name'][store]))
					# 也可以在這裏加上你喜歡的通知方法，我個人愛用 Telegram 去接收，再簡單點用 IFTTT 的 Webhooks 也可以

		# 沒有貨
		if not(available):
			print("{}: Not available".format(datetime.datetime.now().isoformat()))

		# 20 秒後再試
		time.sleep(20)

if __name__ == "__main__":
	main()
