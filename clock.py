import sys
from tkinter import *
import time 
import datetime
import RPi.GPIO as GPIO
import dht11
import geocoder
from pprint import pprint
import requests 
from PIL import Image
import busio
import adafruit_sgp30
import board
import serial
import syslog
import time
port = "/dev/ttyACM0"
i2c_bus = busio.I2C(board.SCL, board.SDA, frequency = 1000000)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c_bus)

#Line 67, ifelse
color = "black"
size = 195
tcolor = "white"

#GPIO Settings to get the sensor working
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=17)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #setup switch
def getSwitch():
        reverse = False
        if (GPIO.input(21) == GPIO.HIGH): #button on the right is puhsed
                reverse = True
        return reverse
reverse = getSwitch()
startReverse = reverse
        
#GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #setup button
#Get Color and Size of Window
#color = input("Choose a color: ")
#size = int(input("Select a size: "))

#Get Current Location
g = geocoder.ip('me')
city = g.city
latlng = g.latlng

#get Weather
try:
    res = requests.get('https://api.darksky.net/forecast/12b7e3f7df4ecaef5997ffaa2fcb46b2/{0},{1}'.format(latlng[0],latlng[1]))
except:
    print("connection error at startup")
    time.sleep(3)
    sys.exit()
data = (res.json())
current_temp = round(data['currently']['temperature'])
mintemp = round(data['daily']['data'][0]["temperatureLow"])
maxtemp = round(data['daily']['data'][0]["temperatureHigh"])
#summary = str(data['daily']['summary'])
mintemp1 = round(data['daily']['data'][1]["temperatureLow"])
maxtemp1 = round(data['daily']['data'][1]["temperatureHigh"])
mintemp2 = round(data['daily']['data'][2]["temperatureLow"])
maxtemp2 = round(data['daily']['data'][2]["temperatureHigh"])
mintemp3 = round(data['daily']['data'][3]["temperatureLow"])
maxtemp3 = round(data['daily']['data'][3]["temperatureHigh"])
mintemp4 = round(data['daily']['data'][4]["temperatureLow"])
maxtemp4 = round(data['daily']['data'][4]["temperatureHigh"])
mintemp5 = round(data['daily']['data'][5]["temperatureLow"])
maxtemp5 = round(data['daily']['data'][5]["temperatureHigh"])
dailysummary = str(data['daily']['data'][0]["summary"])
icon0 = str(data['daily']['data'][0]["icon"])
icon1 = str(data['daily']['data'][1]["icon"])
icon2 = str(data['daily']['data'][2]["icon"])
icon3 = str(data['daily']['data'][3]["icon"])
icon4 = str(data['daily']['data'][4]["icon"])
icon5 = str(data['daily']['data'][5]["icon"])
summary = str(maxtemp1)+ "°/" + str(mintemp1) + "°  " + str(maxtemp2)+ "°/" + str(mintemp2) + "°  " + str(maxtemp3)+ "°/" + str(mintemp3) + "°  "+str(maxtemp4)+ "°/" + str(mintemp4) + "°  " + str(maxtemp5)+ "°/"     + str(mintemp5) + "°  "
sunrise = int(data['daily']['data'][0]["sunriseTime"])
sunset = int(data['daily']['data'][0]["sunsetTime"])

sunpassStart = False
currentime = int(time.time())
day = (currentime >= sunrise) and (currentime < sunset)
night = (currentime <  sunrise) or (currentime >= sunset)
if (currentime < sunset + 30 and currentime > sunset - 30) or (currentime < sunrise + 30 and currentime > sunrise -30):
        sunpassStart = True



def setcolors(sunset, sunrise):
        global reverse
        currentime = int(time.time())
        if reverse and (not sunpassStart): #switch is set to HIGH
                if (((currentime>= sunrise) and (currentime < sunset))):
                        color = "black"
                        tcolor = "#AFAFAF"
                else:
                        color = "white" 
                        tcolor = "black"
        else:
                #reverse = False
                if (((currentime>= sunrise) and (currentime < sunset))):
                        color = "white" 
                        tcolor = "black"
                else:
                        color = "black"
                        tcolor = "#AFAFAF"
        colist = [color, tcolor]
        return colist

color = setcolors(sunset, sunrise)[0]
tcolor = setcolors(sunset, sunrise)[1]

#create labels and Tk box
font = "times"
fontype = "bold"
root = Tk()
root.configure(background = color)
root.title("Clock")
right = -5
down = -40
root.geometry("+{}+{}".format(right,down))
root.geometry("1700x1700")

clock  = Label(root, font = (font, size, fontype), bg = color, fg = tcolor)
clock.grid(row = 0,  column = 0)
date  = Label(root, font = (font, int(size/3), fontype), bg = color, fg = tcolor)
date.grid(row = 1,  column = 0)
outemp  = Label(root, font = (font, int(size/2.2), fontype), bg = color, fg = tcolor)
outemp.grid(row = 2,  column = 0)
dsum  = Label(root, font = (font, int(size/5), fontype), bg = color, fg = tcolor)
dsum.grid(row = 3,  column = 0)
temp  = Label(root, font = (font, int(size/5), fontype), bg = color, fg = tcolor)
temp.grid(row = 4 ,  column = 0)
humid  = Label(root, font = (font, int(size/5), fontype), bg = color, fg = tcolor)
humid.grid(row = 5,  column = 0)
location  = Label(root, font = (font, int(size/5), fontype), bg = color, fg = tcolor)
location.grid(row = 6,  column = 0)
weekday = Label(root, font = (font, int(size/5), fontype), bg = color, fg = tcolor)
weekday.grid(row = 7, column = 0)
weeksum  = Label(root, font = (font, int(size/4), fontype), bg = color, fg = tcolor)
weeksum.grid(row = 8,  column = 0)
iconrow  = Label(root, font = (font, int(size/5), fontype), bg = color, fg = tcolor)
iconrow.grid(row = 9,  column = 0)
#photo = Image.open("Desktop/icons/cloudy.gif")
ypos = 910
xpos = 170
xspace = 230
bicons = 4
sicons = 4
iconfile = "/home/pi/icons/"
photo0 = PhotoImage(file = str(iconfile +"{0}.gif".format(icon0)))
photo0 = photo0.subsample(bicons)
Licon0 = Label(root, image = photo0,bd = 0, highlightthickness = 0, bg = color)
Licon0.place(x = 540, y = 405)
photo1 = PhotoImage(file = str(iconfile +"{0}.gif".format(icon1)))
photo1 = photo1.subsample(sicons)
Licon1 = Label(root, image = photo1,bd = 0, highlightthickness = 0, bg = color)
Licon1.place(x = xpos, y = ypos)
photo2 = PhotoImage(file = str(iconfile +"{0}.gif".format(icon2)))
photo2 = photo2.subsample(sicons)
Licon2 = Label(root, image = photo2,bd = 0, highlightthickness = 0, bg = color)
Licon2.place(x = xpos + xspace, y = ypos)
photo3 = PhotoImage(file = str(iconfile +"{0}.gif".format(icon3)))
photo3 = photo3.subsample(sicons)
Licon3 = Label(root, image = photo3,bd = 0, highlightthickness = 0, bg = color)
Licon3.place(x = xpos + (2*xspace), y = ypos)
photo4 = PhotoImage(file = str(iconfile +"{0}.gif".format(icon4)))
photo4 = photo4.subsample(sicons)
Licon4 = Label(root, image = photo4,bd = 0, highlightthickness = 0, bg = color)
Licon4.place(x = xpos + (3*xspace), y = ypos)
photo5 = PhotoImage(file = str(iconfile +"{0}.gif".format(icon5)))
photo5 = photo5.subsample(sicons)
Licon5 = Label(root, image = photo5,bd = 0, highlightthickness = 0, bg = color)
Licon5.place(x = xpos + (4*xspace), y = ypos)

ygap = 140
xpos = xpos + 35
xspace = xspace - 3
day1ob  = Label(root, font = (font, int(size/4), fontype), bg = color, fg = tcolor)
day1ob.place(x = xpos + (0*xspace), y = ypos - ygap)
day2ob  = Label(root, font = (font, int(size/4), fontype), bg = color, fg = tcolor)
day2ob.place(x = xpos + (1*xspace), y = ypos - ygap)
day3ob  = Label(root, font = (font, int(size/4), fontype), bg = color, fg = tcolor)
day3ob.place(x = xpos + (2*xspace), y = ypos - ygap)
day4ob  = Label(root, font = (font, int(size/4), fontype), bg = color, fg = tcolor)
day4ob.place(x = xpos + (3*xspace), y = ypos - ygap)
day5ob  = Label(root, font = (font, int(size/4), fontype), bg = color, fg = tcolor)
day5ob.place(x = xpos + (4*xspace), y = ypos - ygap)
               
 
#get current weekday as Su M T W Th F S Su
def getweekday(date):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    dow = int(datetime.date(year,month,day).weekday())
    return dow

#converting 24 hour time to 12 hour AMPM time
def to12(time):
    time = str(time)[0:8]
    hour = int(time[0:2])
    AMPM = "AM"
    if hour == 12:
        AMPM = "PM" #noon
    if hour == 0:
        AMPM = "AM" #midnight
        hour = 12
    elif hour > 12:
        hour = hour-12
        AMPM = "PM"
    if hour < 10:
        hour = str("  " + str(hour))
    time = str(str(hour) +  time[2:8]  +" "+AMPM)
    return time


#converting yyyy-mm-dd to Weekday, Month Year
def date2weekday(date):
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    rdth = "th"
    year = int(date[0:4])
    month = int(date[5:7])
    monthprint = months[month-1]
    day = int(date[8:10])
    if (day == 1 or day == 21 or day == 31):
        rdth = "st"
    if (day == 2 or day == 22):
        rdth = "nd"
    if (day == 3 or day == 23):
        rdth = "rd"
    dow = int(datetime.date(year,month,day).weekday())
    dow = week[dow]
    newdatetime = str(dow+" "+str(monthprint)+" "+str(day)+ rdth+", "+ str(year))
    # newdatetime = "Wednesday, September 30th, 2019"
    return newdatetime
#connect to ardunio 
#ard = (serial.Serial(port,9600))
mscount = 0
#Update Clock
def tick():
        global reverse
        global xspace
        global xpos
        global ypos
        global ygap
        global Licon0
        global Licon1
        global Licon2
        global Licon3
        global Licon4
        global Licon5
        global color
        global tcolor
        global clock
        global date
        global outemp
        global dsum
        global temp
        global humid
        global location
        global weekday
        global weeksum
        global iconrow
        global day1ob
        global day2ob
        global day3ob
        global day4ob
        global day5ob
        global mscount
        global mintemp
        global maxtemp
        global mintemp1
        global maxtemp1
        global mintemp2
        global maxtemp2
        global mintemp3
        global maxtemp3
        global mintemp4
        global maxtemp4
        global mintemp5
        global maxtemp5
        global current_temp
        global dailysummary
        global summary
        global sunrise
        global sunset
        global icon0
        global icon1
        global icon2
        global icon3
        global icon4
        global icon5
        global photo0
        global photo1
        global photo2
        global photo3
        global photo4
        global photo5
        global iconfile
        mscount += 200
        currentime = int(time.time())
        day = (currentime >= sunrise) and (currentime < sunset)
        night = (currentime <  sunrise) or (currentime >= sunset)

        reverse = getSwitch()
        if (currentime < sunset + 30 and currentime > sunset - 30) or (currentime < sunrise + 30 and currentime > sunrise -30):
                reverse = False
        if ((((color == "white") and (night)) or ((color == "black") and (day))) and (not reverse)):
                sys.exit()
        if reverse != startReverse:
                sys.exit()
        time_string = datetime.datetime.now().time()
        # 120000 ms = 2 minutes.
        #Ensure when the counter is reset, the weather isn't updated again
        if mscount % 120000 == 0:
                try:
                    res = requests.get('https://api.darksky.net/forecast/12b7e3f7df4ecaef5997ffaa2fcb46b2/{0},{1}'.format(latlng[0],latlng[1]))
                except:
                    print("connection error")
                    sys.exit()
                data = (res.json())
                mintemp = round(data['daily']['data'][0]["temperatureLow"])
                maxtemp = round(data['daily']['data'][0]["temperatureHigh"])
                #summary = str(data['daily']['summary'])
                mintemp1 = round(data['daily']['data'][1]["temperatureLow"])
                maxtemp1 = round(data['daily']['data'][1]["temperatureHigh"])
                mintemp2 = round(data['daily']['data'][2]["temperatureLow"])
                maxtemp2 = round(data['daily']['data'][2]["temperatureHigh"])
                mintemp3 = round(data['daily']['data'][3]["temperatureLow"])
                maxtemp3 = round(data['daily']['data'][3]["temperatureHigh"])
                mintemp4 = round(data['daily']['data'][4]["temperatureLow"])
                maxtemp4 = round(data['daily']['data'][4]["temperatureHigh"])
                mintemp5 = round(data['daily']['data'][5]["temperatureLow"])
                maxtemp5 = round(data['daily']['data'][5]["temperatureHigh"])
                current_temp = round(data['currently']['temperature'])
                dailysummary = str(data['daily']['data'][0]["summary"])
                sunrise = int(data['daily']['data'][0]["sunriseTime"])
                sunset = int(data['daily']['data'][0]["sunsetTime"])
                icon0 = str(data['daily']['data'][0]["icon"])
                photo0 = PhotoImage(file = str(iconfile+"{0}.gif".format(icon0)))
                photo0 = photo0.subsample(bicons)
                icon1 = str(data['daily']['data'][1]["icon"])
                photo1 = PhotoImage(file = str(iconfile+"{0}.gif".format(icon1)))
                photo1 = photo1.subsample(sicons)
                icon2 = str(data['daily']['data'][2]["icon"])
                photo2 = PhotoImage(file = str(iconfile+"{0}.gif".format(icon2)))
                photo2 = photo2.subsample(sicons)
                icon3 = str(data['daily']['data'][3]["icon"])
                photo3 = PhotoImage(file = str(iconfile+"{0}.gif".format(icon3)))
                photo3 = photo3.subsample(sicons)
                icon4 = str(data['daily']['data'][4]["icon"])
                photo4 = PhotoImage(file = str(iconfile+"{0}.gif".format(icon4)))
                photo4 = photo4.subsample(sicons)
                icon5 = str(data['daily']['data'][5]["icon"])
                photo5 = PhotoImage(file = str(iconfile+"{0}.gif".format(icon5)))
                photo5 = photo5.subsample(sicons)
                summary =  str(maxtemp1)+ "°/" + str(mintemp1) + "°  " + str(maxtemp2)+ "°/" + str(mintemp2) + "°  " + str(maxtemp3)+ "°/" + str(mintemp3) + "°  "+str(maxtemp4)+ "°/" + str(mintemp4) + "°  " + str(maxtemp5)+ "°/"     + str(mintemp5) + "°  "
                mscount = 0
                #Update the weather, otherwise the weather is not updated.
        time_string = to12(time_string)
        date_string = datetime.datetime.now().date()
        week = [" M", " T", "W", "Th", " F", " S", "Su"]
        today = int(getweekday(str(date_string)))
        day1 = str(week[(today+1) % 7])
        day2 = str(week[(today+2) % 7])
        day3 = str(week[(today+3) % 7])
        day4 = str(week[(today+4) % 7])
        day5 = str(week[(today+5) % 7])
        date_string = date2weekday(str(date_string))
        outemp_string = str(current_temp) + "°     " + str(maxtemp)+ "°/" + str(mintemp) + "°"
        dsum_string = dailysummary
        #Grab sensor data for interior temp and humidity. Only if valid reading from sensor
        #ardln = str(ard.readline())
        #leng = len(ardln)
        #ardln = ardln[2:(leng-5)]
        result = instance.read()
        if result.is_valid():
            AH = ((6.112*(2.71828**((17.67*result.temperature)/(result.temperature + 243.5)))*result.humidity*2.1674)/(273.15+result.temperature)) 
            sgp30.set_iaq_humidity(AH)
            #print(AH)
            eCO2, TVOC = sgp30.iaq_measure()
            #ard = "4.83"
            #humid_string = ("Room Humidity: "+ str(result.humidity)+ "%" +"\t\tCO = {0} ppm".format(ardln))
            humid_string = ("Room Humidity: "+ str(result.humidity)+ "%" +"\t\tTVOC = {0} ppb".format(TVOC))
            humid_string = str(humid_string)
            F = (float(result.temperature *(9/5) + 32))
            F = str(F)[0:5]
            if len(F) == 2:
                F = F + "."
            while len(F) < 5:
                F = F +"0"
            temp_string = str("Room Temperature: " + F +" F"+ "\tCO2 = %d ppm" % (eCO2))
            temp.config(text=temp_string)
            humid.config(text=humid_string) 
        #display the labels as text
        clock.config(text=time_string)
        date.config(text= date_string)
        outemp.config(text= outemp_string)
        location.config(text = city)
        weeksum.config(text = summary)
        day1ob.config(text = day1)
        day2ob.config(text = day2)
        day3ob.config(text = day3)
        day4ob.config(text = day4)
        day5ob.config(text = day5)
        dsum.config(text = dsum_string)
        Licon0.config(image = photo0)
        Licon1.config(image = photo1)
        Licon2.config(image = photo2)
        Licon3.config(image = photo3)
        Licon4.config(image = photo4)
        Licon5.config(image = photo5)
        #Run this function every 200 msi
        root.after(200, tick)
try:
        tick()
        root.mainloop()
except:
        print("restarting !")
        sys.exit()
