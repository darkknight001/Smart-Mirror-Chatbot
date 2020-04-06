import datetime
import json
import feedparser
import requests

class Knowledge:
    
    def __init__(self,weather_api_key,country_code='in',city = 'Delhi'):
        self.weather_api_key = weather_api_key
        self.country_code = country_code
        self.city =city
        
    def get_date(self):
      x = datetime.datetime.now()
      month_list = ["January","February","March","April","May","June","July","August","September","October","November","December"]
      str_month = "It is "+ x.strftime("%A")+", "+ str(x.day)+ " " + month_list[x.month-1] +", "+ str(x.year)
      return str_month

    def get_time(self):
      x = datetime.datetime.now()
      period = "am"
      hour = x.hour
      minute = lambda x : str(x) if int(x>9) else("0"+str(x))
      if hour>12 and hour!=24:
        hour = x.hour-12
        period = "pm"
      elif hour == 24:
        hour = 12
      str_time = "It is "+ str(hour) + " : "+ str(minute(x.minute)) + " "+ period.upper() 
      return str_time
    
    def get_day(self):
        x = datetime.datetime.now()
        day = "It's" + x.strftime("%A")
        return day
    
    def get_news(self):
        ret_headlines = []
        feed = feedparser.parse("https://news.google.com/news?ned=%s&output=rss" % self.country_code)
        for post in feed.entries[0:5]:
            ret_headlines.append(post.title)
            
        return ret_headlines
        
    
    def find_weather(self,city = 'Delhi'):
        weather_req_url = "https://api.openweathermap.org/data/2.5/weather?APPID=%s&q=%s" % (self.weather_api_key, city)
        r = requests.get(weather_req_url)
        x = r.json()
        
        if x["cod"] != "404":
            y = x["main"]
            temperature = y["temp"]
            t_max = y["temp_max"]
            t_min = y["temp_min"]
            weather = x["weather"][0]["description"]
            return {'city' : city, 'temperature': str(int(temperature-273.15)),'temp_max':t_max,'temp_min':t_min,'forcast':weather.title()}
        else:
            return "Failed"
