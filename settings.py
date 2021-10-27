from dotenv import load_dotenv
import os
import inspect
import tweepy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
def setting_load(this_file_path):
    message=[]
    API_twitter_key,API_twitter_secretkey,API_twitter_AccessToken,API_twitter_AccessToken_secret,worksheet,spread,excel_csv,excel="","","","","","","",""
    output_contents={"CREATED_AT":"","TIME_ZONE":"","TEXT":"","FAVORITE_COUNT":"","RETWEET_COUNT":"","QUOTE_TWEET":"","NAME":"","SCREEN_NAME":"","FOLLOWERS_COUNT":"","FRIENDS_COUNT":"","URL":"","YEAR":"","MONTH":"","DAY":"","DAY_OF_WEEK":"","HOURS":"","MINUTES":"","SECONDS":"","ID":""}
    output_headers={"1":"","2":"","3":"","4":"","5":"","6":"","7":"","8":"","9":"","10":"","11":"","12":"","13":"","14":"","15":"","16":"","17":"","18":"","19":""}
    error_flag=False

    dotenv_path =f"{this_file_path}\.env"
    load_dotenv(dotenv_path)
    env=os.environ.get
    USERNAME=os.system.__self__.environ.get("USERNAME")
    json_file=os.environ.get("JSON_FILE");use_json=os.environ.get("USE_JSON")
    file_name=os.environ.get("FILE_NAME");sheet_name=os.environ.get("SHEET_NAME")
    spread=os.environ.get("spread");excel_csv=os.environ.get("csv");excel=os.environ.get("excel")
    API_twitter_key= os.environ.get("API_key")
    API_twitter_secretkey= os.environ.get("API_secretkey")
    API_twitter_AccessToken= os.environ.get("API_AccessToken")
    API_twitter_AccessToken_secret=os.environ.get("API_AccessToken_secret")

    def set_load():
        pass
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        if spread=="True" and not file_name=="" and not sheet_name=="":
            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
            gc = gspread.authorize(credentials)
            wkb = gc.open(file_name)
            wks = gc.open(file_name).worksheet(sheet_name)
        else:
            wkb,wks=None,None,
            message.append(f"envファイルのjsonの設定がありません。@setting_load:{inspect.currentframe().f_lineno}")

        if not use_json=="":
            use_GSS=ServiceAccountCredentials.from_json_keyfile_name(use_json, scope)
            use_wb = gspread.authorize(use_GSS)
            use_histry_wb=use_wb.open("使用履歴")
            use_histry_ws=use_histry_wb.worksheet("内容")
        else:
            use_histry_wb,use_histry_ws=None,None,
            message.append(f"envファイルのuse_jsonの設定がありません。@setting_load:{inspect.currentframe().f_lineno}")

        if API_twitter_key and API_twitter_secretkey and API_twitter_AccessToken and API_twitter_AccessToken_secret:
            auth = tweepy.OAuthHandler(API_twitter_key, API_twitter_secretkey)
            auth.set_access_token(API_twitter_AccessToken, API_twitter_AccessToken_secret)
            api = tweepy.API(auth)
            error_flag=False
        else:
            message.append(f"API_Twitter_Configファイルが見つかりませんでした。。@setting_load:{inspect.currentframe().f_lineno}")
            error_flag=True

        #output_settings#
        if "CONFIG" and "OUTPUT_CONTENTS" and "OUTPUT_HEADERS"  in str(env):
            for key in output_contents:
                try:
                    output_contents[key]=os.environ.get(key)
                    if key=="CREATED_AT":
                        if output_contents["CREATED_AT"]=="True":
                            created_at_flag=True
                        else:
                            created_at_flag=False
                    if key=="TIME_ZONE":
                        if output_contents["TIME_ZONE"]=="True":
                            time_zone_flag=True
                        else:
                            time_zone_flag=False
                    if key=="URL":
                        if output_contents["URL"]=="True":
                            url_flag=True
                        else:
                            url_flag=False
                    if key=="QUOTE_TWEET":
                        if output_contents["QUOTE_TWEET"]=="True":
                            quote_tweet_flag=True
                        else:
                            quote_tweet_flag=False
                    if key=="FAVORITE_COUNT":
                        if output_contents["FAVORITE_COUNT"]=="True":
                            favorite_count_flag=True
                        else:
                            favorite_count_flag=False
                    if key=="RETWEET_COUNT":
                        if output_contents["RETWEET_COUNT"]=="True":
                            retweet_count_flag=True
                        else:
                            retweet_count_flag=False
                    if key=="FRIENDS_COUNT":
                        if output_contents["FRIENDS_COUNT"]=="True":
                            friends_count_flag=True
                        else:
                            friends_count_flag=False
                    if key=="FOLLOWERS_COUNT":
                        if output_contents["FOLLOWERS_COUNT"]=="True":
                            followers_count_flag=True
                        else:
                            followers_count_flag=False
                except:
                    continue
            print("end_output_contents")
        else:
            print("初期化できませんでした。 @output_contents")
            
        if "1" and "2" and "3" and "4" and "5" and "6" and "7"  in str(env):
            for key in output_headers:
                try:
                    output_headers[key]=os.environ.get(key)
                except:
                    continue
            print("end_output_headers")
        else:
            print("初期化できませんでした。 @output_headers")

        if len(output_contents) == len(output_headers):
            print("end_output_contents=output_headers")
        else:
            print("初期化できませんでした。 @output_contents=output_headers")

        return wkb,wks,use_histry_wb,use_histry_ws,output_contents,output_headers,created_at_flag,time_zone_flag,url_flag,quote_tweet_flag,favorite_count_flag,retweet_count_flag,friends_count_flag,followers_count_flag,api,error_flag

    wkb,wks,use_histry_wb,use_histry_ws,output_contents,output_headers,created_at_flag,time_zone_flag,url_flag,quote_tweet_flag,favorite_count_flag,retweet_count_flag,friends_count_flag,followers_count_flag,api,error_flag,=set_load()

    return(
        env,USERNAME,
        json_file,use_json,file_name,sheet_name,spread,wkb,wks,use_histry_wb,use_histry_ws,
        worksheet,excel_csv,excel,
        api,API_twitter_key,API_twitter_secretkey,API_twitter_AccessToken,API_twitter_AccessToken_secret,
        output_contents,output_headers,created_at_flag,time_zone_flag,url_flag,
        quote_tweet_flag,favorite_count_flag,retweet_count_flag,friends_count_flag,followers_count_flag,
        message,error_flag
        )

if __name__ == "__main__":
    this_file_path=os.getcwd()
    setting_load(this_file_path)