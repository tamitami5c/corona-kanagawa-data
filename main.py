import json
import csv
import io
import datetime

import requests


def main():
    url="https://www.pref.kanagawa.jp/osirase/1369/data/csv/patient.csv"
    r=requests.get(url)
    r.encoding=r.apparent_encoding
    if r.status_code!=requests.codes.ok:
        raise Exception("status_code != ok")

    date2count={}
    reader=csv.DictReader(io.StringIO(r.text))

    for row in reader:
        date_text=row["発表日"]
        if date_text in date2count:
            date2count[date_text]+=1
        else:
            date2count[date_text]=1

    #感染者がいる日付にその感染者数を入れる
    dates=list(map(lambda k:datetime.date.fromisoformat(k),date2count.keys()))

    #抜けている日付に0を入れていく。
    start_date=min(dates)
    end_date=max(dates)
    i=0
    print(dates)
    while True:
        date=start_date+datetime.timedelta(days=i)
        print([date.isoformat()])
        print(date not in dates)
        if date not in dates:
            date2count[date.isoformat()]=0


        i+=1

        if date==end_date:
            break

    #{'date':'2020-01-01','count':0}のようなものの配列を作る
    data=sorted(list(map(lambda key:{"date":key,"count":date2count[key]},date2count.keys())),key=lambda k:datetime.date.fromisoformat(k["date"]))
    json_data={
        "data":data
    }
    #保存する
    with open("kanagawa_data.json","w") as f:
        json.dump(json_data,f,ensure_ascii=False,indent=4)


if __name__ == "__main__":
    main()