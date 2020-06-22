import slackweb
import requests
from bs4 import BeautifulSoup
import csv
import os
import datetime
import schedule
import time

def job():
        slack = slackweb.Slack(url="https://hooks.slack.com/services/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")

        headers = {
        'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'en-US,en;q=0.9,ja;q=0.8,fr-FR;q=0.7,fr;q=0.6',
        'Authorization'   : 'Basic Y3JpdGVvY3BwZjpaJkRYc2xzdyVE',
        'Cache-Control'   : 'no-cache',
        'Connection'      : 'keep-alive',
        'Host'            : 'datafeed.ias.rakuten.co.jp',
        'Pragma'          : 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }

        reqSession = requests.Session()
        res        = reqSession.get('http://datafeed.ias.rakuten.co.jp/datafeed/criteocppf/rakuten_feed_file_list.dat', headers=headers)
        l          = res.text.split('\n')
        del l[-1]

        a = []
        for line in open('rakuten_feed_file_list_yesterday.dat.txt','r').readlines():
                choped_line = line.rstrip('\n')
                a.append(choped_line)

        for i in l:
                if i not in a:
                        slack.notify(text="今日のリストから追加もしくは変更になっているファイル名: " + i)
                        print("今日のリストから追加もしくは変更になっているファイル名: " + i)

        for j in a:
                if j not in l:
                        slack.notify(text="今日のリストから消えているファイル名： " + j)
                        print("今日のリストから消えているファイル名： " + j)

        today = datetime.date.today()
        os.remove("rakuten_feed_file_list_yesterday.dat.txt")

        for i in l:
                with open("rakuten_feed_file_list_yesterday.dat.txt", mode="a") as k:
                        k.writelines(i + "\n")

                with open("rakuten_feed_file_list_" + today.strftime('%Y%m%d') + ".dat.txt", mode="a") as k:
                        k.writelines(i + "\n")

schedule.every().day.at("11:50").do(job)

while True:
  schedule.run_pending()
  time.sleep(300)