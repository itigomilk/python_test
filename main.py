import twint
import json
import tkinter as tk
import tweepy
import csv
import datetime
from datetime import timezone, timedelta
from dateutil.parser import parse
import time
import os
import gspread
import glob
from concurrent.futures.thread import ThreadPoolExecutor
from settings import setting_load

AID="uKY-AZ9YXk"
use_library="twint"
this_file_path=os.getcwd()
(
env,USERNAME,
json_file,use_json,file_name,sheet_name,spread,wkb,wks,use_histry_wb,use_histry_ws,
worksheet,excel_csv,excel,
api,API_twitter_key,API_twitter_secretkey,API_twitter_AccessToken,API_twitter_AccessToken_secret,
output_contents,output_headers,created_at_flag,time_zone_flag,url_flag,
quote_tweet_flag,favorite_count_flag,retweet_count_flag,friends_count_flag,followers_count_flag,
message,error_flag
)=setting_load(this_file_path)

win_x=350
win_y=400
win=tk.Tk()
objs=[]

def callback(event):
    print(event.widget["textvariable"])
    if event.widget["textvariable"]=="__get":
        global objs
        print("OK")
        if objs[1].get():
            get_tweets((objs[1].get()).replace("@",""),(objs[6].get()),(objs[9].get()),(objs[12].get()),(objs[13].get()), )
        else:
            print("入力されていません。入力してください。")
    else:
        print("NG")

def gss_history(x,col):
    global use_histry_wb
    global use_histry_ws
    global AID
    use_histry_ws=use_histry_wb.worksheet("内容")
    x_column=use_histry_ws.find(col).col
    last_row=use_histry_ws.row_count
    if use_histry_ws.find(col).value=="AID":
        use_histry_ws.add_rows(1)
        use_histry_ws.update_cell(last_row+1,x_column,x)
    else:
        use_histry_ws.update_cell(last_row,x_column,x)

def settings():
    with ThreadPoolExecutor() as executor:
        # executor.submit(gss_history(AID,"AID"))
        # executor.submit(gss_history(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),"date"))
        # executor.submit(gss_history(USERNAME,"User"))

        global objs
        i=0
        objs.append(tk.Label(win,text="Twitter ID",font=("メイリオ", 12),anchor="center",width=20))
        objs[i].pack()
        i+=1
        objs.append(tk.Entry(win,text="",width=25,font=("メイリオ", 12),justify="center"))
        objs[i].pack()
        i+=1
        objs.append(tk.Label(win,text="",font=("メイリオ", 5),anchor="center",width=20))
        objs[i].pack()
        i+=1
        objs.append(tk.Button(win,text="ツイート取得開始",textvariable="__get",font=("メイリオ", 12),anchor="center"))
        objs[i].bind("<1>",callback)
        objs[i].pack()
        i+=1
             
        objs.append(tk.Label(win,text="",font=("メイリオ", 5),anchor="center",width=20))
        objs[i].pack()
        i+=1
        objs.append(tk.Label(win,text="条件指定：いいね数以上",font=("メイリオ", 12),anchor="center",width=20))
        objs[i].pack()
        i+=1
        objs.append(tk.Entry(win,text="",width=25,font=("メイリオ", 12),justify="center"))
        objs[i].pack()
        i+=1

        objs.append(tk.Label(win,text="",font=("メイリオ", 5),anchor="center",width=20))
        objs[i].pack()
        i+=1
        objs.append(tk.Label(win,text="この日から(例:2000-01-01)",font=("メイリオ", 12),anchor="center",width=22))
        objs[i].pack()
        i+=1
        objs.append(tk.Entry(win,text="",width=25,font=("メイリオ", 12),justify="center"))  #objs[9]
        objs[i].pack()
        i+=1
        objs.append(tk.Label(win,text="",font=("メイリオ", 5),anchor="center",width=20))
        objs[i].pack()
        i+=1
        objs.append(tk.Label(win,text="この日まで(例:2021-01-01)",font=("メイリオ", 12),anchor="center",width=22))
        objs[i].pack()
        i+=1
        objs.append(tk.Entry(win,text="",width=25,font=("メイリオ", 12),justify="center"))  #objs[12]
        objs[i].pack()
        i+=1

        
        objs.append(tk.BooleanVar(value = False))    #objs[13]
        i+=1
        objs.append(tk.Checkbutton(win, variable=objs[13],onvalue=False,offvalue=True ,text="返信、リプライを除く"))
        objs[i].pack()
        i+=1

        # objs.append(tk.BooleanVar(value = False))    #objs[15]
        # i+=1
        # objs.append(tk.Checkbutton(win, variable=objs[15],onvalue=False,offvalue=True ,text="RT、リツイートを除く"))
        # objs[i].pack()
        # i+=1
        
        print("end_settings")

def get_tweets(_ID,_like,start_since,end_since,RP_flag,):
    global spread
    global excel_csv
    global excel
    global api
    global wks
    global file_name
    tweets_list=[]

    if _like =="":
        _like=0
    if RP_flag:
        RP_flag=False
    else:
        RP_flag=True

    with ThreadPoolExecutor() as executor:
        executor.submit(gss_history(AID,"AID"))
        executor.submit(gss_history(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),"date"))
        executor.submit(gss_history(_ID +" & "+str(_like),"input"))
        executor.submit(gss_history(f"spread={spread},csv={excel_csv},excel={excel}","info"))
        executor.submit(gss_history(USERNAME,"User"))

    now_time=datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    # api.update_status(f"Twitterから指定IDのツイートを取得してExcelに出力するアプリケーションが使用されました。\nAID:{AID} {now_time}\n#Python\n#駆け出しエンジニアと繋がりたい\n#駆け出しエンジニア\n{_ID}")
    num=0
    if _ID:
        if use_library=="twint":
            json_dict=[]
            file_name=str(datetime.datetime.now().strftime("%Y%m%d %H %M %S"))
            path_json=f"出力ファイル/{file_name}.json"
            with open(path_json, 'w'):
                pass

            c = twint.Config()
            if start_since:#「この日から」の指定 "2015-01-01"
                c.Since=start_since
            if end_since:#「この日まで」の指定 "2020-01-01"
                c.Until = end_since

            c.Username = _ID
            c.Min_likes= _like
            c.Hide_output = True
            c.Store_json = True
            c.Output = path_json
            twint.run.Search(c)
            with open(path_json,"r",encoding="utf-8") as f:
                for line in f:
                    json_dict.append(json.loads(line))
            os.remove(path_json)

            tweet_user = api.user_timeline(_ID, count=1)
            out_headers=["日付","時間帯","ツイート","リプライ数","いいね数","リツイート数","引用RT","アカウントID","アカウント名","フォロワー数","フォロー数","リンク"]
            for tweet in json_dict:
                if tweet["likes_count"]>=int(_like):
                    if RP_flag==True:
                        if "@" in tweet["tweet"][:1]:        
                            continue
                    data_list=[]
                    # data_list["日付"]=tweet["date"]+" "+tweet["time"]
                    # time_zone=int(tweet["time"][:2])
                    # if 5<= time_zone <=10:
                    #     data_list["時間帯"]="朝"
                    # elif 11<=time_zone<=16:
                    #     data_list["時間帯"]="昼"
                    # else:
                    #     data_list["時間帯"]="夜"
                    # data_list["ツイート"]=tweet["tweet"]
                    # data_list["リプライ数"]=tweet["replies_count"]
                    # data_list["いいね数"]=tweet["likes_count"]
                    # data_list["リツイート数"]=tweet["retweets_count"]
                    # data_list["引用RT"]=tweet["quote_url"]
                    # data_list["アカウントID"]=tweet["username"]
                    # data_list["アカウント名"]=tweet["name"]
                    # data_list["フォロワー数"]=tweet_user[0].user.followers_count
                    # data_list["フォロー数"]=tweet_user[0].user.friends_count
                    # data_list["リンク"]=tweet["link"]
                    # tweet_data.append(data_list)

                    data_list.append(tweet["date"]+" "+tweet["time"])
                    time_zone=int(tweet["time"][:2])
                    if 5<= time_zone <=10:
                        data_list.append("朝")
                    elif 11<=time_zone<=16:
                        data_list.append("昼")
                    else:
                        data_list.append("夜")
                    data_list.append(tweet["tweet"])
                    data_list.append(tweet["replies_count"])
                    data_list.append(tweet["likes_count"])
                    data_list.append(tweet["retweets_count"])
                    data_list.append(tweet["quote_url"])
                    data_list.append(tweet["username"])
                    data_list.append(tweet["name"])
                    data_list.append(tweet_user[0].user.followers_count)
                    data_list.append(tweet_user[0].user.friends_count)
                    data_list.append(tweet["link"])
                    tweets_list.append(data_list)

            output_date=datetime.datetime.now().strftime("%Y%m%d %H %M %S")
            with open(f'出力ファイル/{output_date}.csv', 'w',newline='',errors='ignore') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(out_headers) # １行目に書く
                writer.writerows(tweets_list)
        return
        global output_headers
        out_headers=[]
        if spread=="True":
            try:
                tweets = tweepy.Cursor(api.user_timeline, id=_ID,exclude_replies = RP_flag,include_rts = RT_flag,count=10000).items(10000)
                for worksheet in wkb.worksheets():
                    if _ID ==worksheet.title:
                        add_skip=True
                        break
                    else:
                        add_skip=False
                        continue
                if add_skip==False:
                    pass
                    wkb.add_worksheet(title=_ID, rows="3500", cols="28")
                wks = wkb.worksheet(_ID)
                num=0
                y=2
                for tweet in tweets:
                    tweet_json=tweet._json
                    i,x=0,1
                    num+=1
                    tweet_str=str(tweet_json)
                    for key,value in output_contents.items():
                        if value=="True":
                            if num ==1:
                                out_headers.append(output_headers[str(i+1)])
                            val=tweet_str[tweet_str.find('\'' + key.lower()+'\''):]
                            val=val[val.find(" ")+1:val.find(",")].replace("'","").replace("\\n","\n")
                            tweets_list.append(val)
                            x+=1
                        i+=1
                    y+=1
                if not num==1:
                    header_cell_list=wks.range(1, 1, 1 , x-1)
                    for j,cell in enumerate(header_cell_list):
                        cell.value = out_headers[j]
                    cell_list=wks.range(2, 1,y-1, x-1)
                    for k,cell in enumerate(cell_list):
                        cell.value = tweets_list[k]
                    wks.update_cells(header_cell_list) and wks.update_cells(cell_list)
                    print("指定IDツイート出力完了")
                    gss_history("OK","normal")
                else:
                    print("ツイートが取得できませんでした。")
                    gss_history(tweet_json,"errorA")
                print("end")

                gss_history(num,"num")
                gss_history("OK","normal")

            except tweepy.TweepError as e:
                if e.reason == "[{'Twitter error response: status code = 404}]":
                        print("制限がかかりました。")
                        gss_history(e.reason ,"errorB")
                        print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                        time.sleep(60 * 15)
                else:
                    print("想定外の問題が発生しました。")
                    print(e.reason)
                    gss_history(e ,"errorC")

                gss_history("NG","normal")

            except gspread.exceptions.APIError as e:
                if 403 or 429 in e:
                    print("制限がかかりました。")
                    gss_history(e ,"errorB")
                else:
                    print("想定外の問題が発生しました。")
                    gss_history(e ,"errorC")

                gss_history("NG","normal")

        elif excel_csv=="True" or excel=="True":
            try:
                tweets = tweepy.Cursor(api.user_timeline, id=_ID,exclude_replies = RP_flag,include_rts = RT_flag,count=10000).items(10000) 
                #tweets = api.user_timeline(_ID, count=2000, page=10).items()
                num=0
                y=0
                for tweet in tweets:
                    i=0
                    num+=1
                    tweet_str=str(tweet)
                    x=1
                    tweet_list=[]
                    if not tweet.favorite_count>=int(_like):continue
                    for key,value in output_contents.items():
                        if value=="True":
                            if num ==1:
                                out_headers.append(output_headers[str(i+1)])
                            if key=="TEXT":
                                val=tweet.text
                            elif not created_at_flag and key in ("YEAR","MONTH","DAY","DAY_OF_WEEK","HOURS","MINUTES","SECONDS") :
                                val=tweet.created_at + timedelta(hours=9) 
                                # print(val.strftime('%Y %m %d %b %a %H:%M:%S'))
                                if key=="YEAR":
                                    val=val.strftime('%Y')
                                elif key=="MONTH":
                                    val=val.strftime('%m')
                                elif key=="DAY":
                                    val=val.strftime('%d')
                                elif key=="DAY_OF_WEEK":
                                    val=val.strftime('%a')
                                elif key=="HOURS":
                                    val=val.strftime('%H')
                                elif key=="MINUTES":
                                    val=val.strftime('%M')
                                elif key=="SECONDS":
                                    val=val.strftime('%S')
                            elif created_at_flag and key in ("YEAR","MONTH","DAY","DAY_OF_WEEK","HOURS","MINUTES","SECONDS"):
                                if num==1:
                                    del out_headers[len(out_headers)-1]
                                i+=1
                                continue
                            elif created_at_flag and key=="CREATED_AT":
                                val=tweet.created_at + timedelta(hours=9)
                                tweet_list.append(str(val))
                                time_zone=val.hour
                                if 5<= time_zone <=10:
                                    time_zone="朝"
                                elif 11<=time_zone<=16:
                                    time_zone="昼"
                                else:
                                    time_zone="夜"
                                x+=1
                                i+=1
                                continue
                            elif time_zone_flag and key=="TIME_ZONE":
                                tweet_list.append(time_zone)
                                x+=1
                                i+=1
                                continue
                            elif url_flag and key=="URL":
                                tweet_list.append("https://twitter.com/"+ _ID + "/status/"+tweet.id_str)
                                x+=1
                                i+=1
                                continue
                            elif quote_tweet_flag and key=="QUOTE_TWEET":
                                if "quoted_status_id_str" in tweet_str:
                                    tweet_list.append("https://twitter.com/"+ _ID + "/status/"+tweet.quoted_status_id_str)
                                    x+=1
                                    i+=1
                                else:
                                    tweet_list.append("")
                                    x+=1
                                    i+=1
                                continue
                            elif favorite_count_flag and key=="FAVORITE_COUNT":
                                tweet_list.append(tweet.favorite_count)
                                x+=1
                                i+=1
                                continue
                            elif retweet_count_flag and key=="RETWEET_COUNT":
                                tweet_list.append(tweet.retweet_count)
                                x+=1
                                i+=1
                                continue
                            elif friends_count_flag and key=="FRIENDS_COUNT":
                                tweet_list.append(tweet.user.friends_count)
                                x+=1
                                i+=1
                                continue
                            elif followers_count_flag and key=="FOLLOWERS_COUNT":
                                tweet_list.append(tweet.user.followers_count)
                                x+=1
                                i+=1
                                continue
                            else:
                                val=tweet_str[tweet_str.find('\'' + key.lower()+'\''):]
                                val=val[val.find(" ")+1:val.find(",")].replace("'","").replace("\\n","\n")
                            tweet_list.append("'"+val)
                            x+=1
                        i+=1
                    tweets_list.append(tweet_list)
                    y+=1

                if excel_csv=="True":
                    output_date=datetime.datetime.now().strftime("%Y%m%d %H %M %S")
                    with open(f'出力ファイル/{output_date}.csv', 'w',newline='',errors='ignore') as f:
                        writer = csv.writer(f, lineterminator='\n')
                        writer.writerow(out_headers) # １行目に書く
                        writer.writerows(tweets_list)
                elif excel=="True":
                    output_date=datetime.datetime.now().strftime("%Y%m%d %H %M %S")
                    with open(f'出力ファイル/{output_date}.csv', 'w',newline='',errors='ignore') as f:
                        writer = csv.writer(f, lineterminator='\n')
                        writer.writerow(out_headers) # １行目に書く
                        writer.writerows(tweets_list)

                gss_history(num,"num")
                gss_history("OK","normal")

            except tweepy.TweepError as e:
                if e.reason == "[{'Twitter error response: status code = 404}]":
                        print("制限がかかりました。")
                        gss_history(e.reason ,"errorB")
                        print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                        #time.sleep(60 * 15)
                        input("Enterを押すと処理が終了します。")
                else:
                    print("想定外の問題が発生しました。")
                    print(e.reason)
                    gss_history(e ,"errorC")

                gss_history("NG","normal")

settings()
win.minsize(win_x,win_y)
win.maxsize(win_x,win_y)
win.title("twitter_to_file")
files=glob.glob(r"./*")
for file in files:
    if ".ico" in file:
        iconfile = this_file_path + r"\icon.ico"
        win.iconbitmap(default=iconfile)
        break
    elif ".png" in file:
        win.iconphoto(False, tk.PhotoImage(file=this_file_path + r"\icon.png"))
        break
    else:
        continue
win.mainloop()