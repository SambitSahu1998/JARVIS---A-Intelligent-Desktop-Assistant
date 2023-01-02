import pywhatkit
import datetime
import wikipedia
import os
import socket
import psutil, pyttsx3, math
import geocoder
from geopy.geocoders import Nominatim
import asyncio
import winsdk.windows.devices.geolocation as wdg
from Speak import Say
import time
import pyautogui
import pprint
import requests
import json
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import webbrowser
import subprocess
import pyautogui
from PIL import Image
import time
from Listen import Listen
from twilio.rest import Client

def Time():
    time = datetime.datetime.now().strftime("%H:%M")
    Say(time)

def Date():
    date=datetime.date.today()
    Say(date)

def Day():
    day=datetime.datetime.now().strftime("%A")
    Say(day)

def NonInputExecution(query):
    query=str(query)
    
    if "time" in query:
        Time()
    
    elif "date"in query:
        Date()

    elif "day"in query:
        Day()



def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))   
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


def system_stats():
    cpu_stats = str(psutil.cpu_percent())
    battery_percent = psutil.sensors_battery().percent
    memory_in_use = convert_size(psutil.virtual_memory().used)
    total_memory = convert_size(psutil.virtual_memory().total)
    final_res = f"Currently {cpu_stats} percent of CPU, {memory_in_use} of RAM out of total {total_memory}  is being used and battery level is at {battery_percent} percent"
    return final_res

async def getCoords():
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return [pos.coordinate.latitude, pos.coordinate.longitude]


def getLoc():
    try:
        return asyncio.run(getCoords())
    except PermissionError:
        print("ERROR: You need to allow applications to access you location in Windows settings")

def my_location():
    print(getLoc())
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse(getLoc())
    Say(locname.address)
    



def get_news():
    url = 'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=f8703d1081f54853b926df2a8d26ae8b'
    news = requests.get(url).text
    news_dict = json.loads(news)
    articles = news_dict['articles']
    try:
        return articles
    except:
        return False


def loc(place):
    webbrowser.open("http://www.google.com/maps/place/" + place + "")
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(place, addressdetails=True)
    target_latlng = location.latitude, location.longitude
    location = location.raw['address']
    target_loc = {'city': location.get('city', ''),
                   'state': location.get('state', ''),
                   'country': location.get('country', '')}

    geoLoc = Nominatim(user_agent="GetLoc")
    current_loc =  geoLoc.reverse(getLoc())
    current_latlng = getLoc()

    distance = str(great_circle(current_latlng, target_latlng))
    distance = str(distance.split(' ',1)[0])
    distance = round(float(distance), 2)

    return current_loc, target_loc, distance



def website_opener(domain):

    try:
        url = 'https://www.' + domain +'.com'
        webbrowser.open(url)
        return True
    except Exception as e:
        print(e)
        return False


def launch_app(path_of_app):
    try:
        subprocess.call([path_of_app])
        return True
    except Exception as e:
        print(e)
        return False

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    notepad = "C://Program Files//Notepad++//notepad++.exe"
    subprocess.Popen([notepad, file_name])


def weather():
    api_key = "c08c1b8094ff3eb234b2d9f95433fb01"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    Say("of which City?")
    city_name = Listen()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        print(city_name+":-\n")
        Say(" Temperature (in kelvin unit) = " +str(current_temperature) + "\n atmospheric pressure (in hPa unit) = " +str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidity) +"\n description = " +str(weather_description))
    else:
        Say(" City Not Found ")


def phonecall():
    account_sid='AC10a0b6b18279c555f2d0e8a7ee431e2b'
    auth_token='b2c1ecd49dcf0999bfda573c9516654d'
    client=Client(account_sid,auth_token)

    client.calls.create(twiml='<Response>Hello This is Sambit Kumar Sahu</Response/>',
                        to='+918763216294',
                        from_='+19498281238')



def InputExecution(tag,query):

    if "wikipedia" in tag:
        name = str(query).replace("who is","").replace("about","").replace("what is","").replace("wikipedia","").replace("what's","")
        result = wikipedia.summary(name,sentences=2)
        Say(result)

    elif "hide" in tag:
        os.system("attrib +h /s /d")
        Say("Sir, all the files in this folder are now hidden")

    elif "visible" in tag:
        os.system("attrib -h /s /d")
        Say("Sir, all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace")

    elif "ip" in tag:
        hostname=socket.gethostname()
        IPAddr = socket.gethostbyname(hostname) 
        Say(f"Your ip address is {IPAddr}")

    elif "system" in tag:
        sys_info = system_stats()
        Say(sys_info)

    elif "locationc" in tag:
        my_location()

    elif "swindow" in tag:
        Say("Okay sir, Switching the window")
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.keyUp("alt")

    elif "news" in tag:
                x=1
                news_res = get_news()
                Say('Source: The Times Of India')
                Say('Todays Headlines are..')
                for index,articles in enumerate(news_res):
                        pprint.pprint(articles['title'])
                        Say(articles['title'])
                        x+=1
                        if index == len(news_res)-2:
                            break
                        if x==5:
                            break
                Say('These were the top headlines, Have a nice day Sir!!..')

    elif "findplace" in tag:
                place = query.split('where is ', 1)[1]
                current_loc, target_loc, distance = loc(place)
                city = target_loc.get('city', '')
                state = target_loc.get('state', '')
                country = target_loc.get('country', '')
                time.sleep(1)
                try:

                    if city:
                        res = f"{place} is in {state} state and country {country}. It is {distance} km away from your current location"
                        Say(res)

                    else:
                        res = f"{state} is a state in {country}. It is {distance} km away from your current location"
                        Say(res)

                except:
                    res = "Sorry sir, I couldn't get the co-ordinates of the location you requested. Please try again"
                    Say(res)


    elif "open" in tag:
                domain = query.split(' ')[-1]
                open_result = website_opener(domain)
                Say(f'Alright sir !! Opening {domain}')

    elif "video" in tag:
                video = query.split(' ')[1]
                Say(f"Okay sir, playing {video} on youtube")
                pywhatkit.playonyt(video)


    elif "apps" in tag:
                dict_app = {

                    'chrome' : 'C:/Program Files/Google/Chrome/Application/chrome',
                    'brave'  : 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe',
                    'kmplayer' : 'C:/Program Files/KMPlayer 64X/KMPlayer64.exe',
                    'notepad' : 'C:/Program Files/Notepad++/notepad++.exe',
                    'uml' : 'C:/Program Files/StarUML/StarUML.exe'
                }

                app = query.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    Say('Application path not found')

                else:
                    Say('Launching: ' + app + ' for you sir!')
                    launch_app(path_of_app=path)


    elif "tscreenshot" in tag:
                Say("By what name do you want to save the screenshot?")
                na = Listen()
                Say("Alright sir, taking the screenshot")
                img = pyautogui.screenshot()
                na = f"{na}.jpeg"
                img.save(na)
                Say("The screenshot has been succesfully captured")
                img = Image.open('D://ProjectCode//'+na)
                img.show(img)
                Say("Here it is sir")
                time.sleep(2)

    elif "cscreenshot" in tag:
                 Say("Closing Screenshot")
                 os.system("Taskkill /IM PhotosApp.exe /F")

    elif "cnotepad" in tag:
                 Say("Closing Notepad")
                 os.system("taskkill /f /im notepad++.exe")

    elif "mnotepad" in tag:
                Say("What would you like me to write down?")
                note_text = Listen()
                note(note_text)
                Say("I've made a note of that")
    
    elif "weather" in tag:
                weather()
    
    elif "volup" in tag:
            pyautogui.press("volumeup")
            Say("I've increased yout volume by 2")
    
    elif "voldn" in tag:
            pyautogui.press("volumedown")
            Say("I've decreased yout volume by 2")

    elif "volmt" in tag:
            pyautogui.press("volumemute")
            Say("Muted Successfully!")

    elif "phonecall" in tag:
            phonecall()
            Say("A trail call being generated!")


        



    

    
        


