#!/usr/bin/env python3
import datetime
import time
import requests
import json
import tweepy
from PIL import Image, ImageDraw, ImageFont

# authentication of access token and secret
consumer_key = 'consumer key'
consumer_secret = 'consumer secrets'
access_token = 'access token'
access_token_secret = 'access token secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# create font object with the font file and specify
# desired size
font = ImageFont.truetype('font/Roboto-Bold.ttf', size=80)
avail_date_font = ImageFont.truetype('font/Roboto-Bold.ttf', size=40)
count_font = ImageFont.truetype('font/Roboto-Bold.ttf', size=60)
vaccine_font= ImageFont.truetype('font/Roboto-Bold.ttf', size=60)
dist_font =ImageFont.truetype('font/Roboto-Bold.ttf', size=40)

# get current date


def getDate():
    current_time = datetime.datetime.now()
    day = current_time.day
    month = current_time.month
    year = current_time.year
    date = "{dd}-{mm}-{yyyy}".format(dd=day, mm=month, yyyy=year)
    # set time interval for checking vaccine availability, default time : 15 minutes
    time.sleep(900)
    return date
# get name of district


def getDistrictID(st_id, lookout_district):
    district_name = ''
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{st}".format(
        st=st_id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        parsed_response = json.loads(response.text)
        district_length = len(parsed_response['districts'])
        for idx in range(district_length):
            if((parsed_response['districts'][idx]['district_id']) == lookout_district):
                district_name = parsed_response['districts'][idx]['district_name']
        return (district_name)
    except Exception as e:
        print(e)


# get vaccine slot details
def getCOWIN(date, district_id):
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}".format(
        district_id=district_id, date=date)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

# check slot availability


def checkAvailability(payload):
    if('centers' in payload.keys()):
        length = len(payload['centers'])
        output = []
        if(length > 1):
            for i in range(length):
                sessions_len = len(payload['centers'][i]['sessions'])
                for j in range(sessions_len):
                    if((payload['centers'][i]['sessions'][j]['available_capacity'] > 0)):
                        res = {'available_center': payload['centers'][i]['name'],
                               'capacity': payload['centers'][i]['sessions'][j]['available_capacity'],
                               'vaccine': payload['centers'][i]['sessions'][j]['vaccine'],
                               'date_avail': payload['centers'][i]['sessions'][j]['date']}
                        output.append(res)

    return output

while True:
    st_id = 17
    lookout_district = 296 # distict id which you want to keep an eye on vaccine availability
    date = getDate()
    district_id = lookout_district
    dist_name = getDistrictID(st_id, lookout_district)
    payload = getCOWIN(date, district_id)
    responses = checkAvailability(payload)
    for key in responses:
        status = "Cowin Vaccine slot available at #" + dist_name + " ("+key['date_avail']+") \n #getvaccinated #cowin  #CrushTheCurve \n posted by:#cowintrackerbot"
        image = Image.open('images/cowin.jpg') 
        draw = ImageDraw.Draw(image)
        (x, y) = (122,170)
        center_name = key['available_center']
        color = 'rgb(255, 255, 255)' # white
        draw.text((x, y), center_name, fill=color, font=font)

        (x, y) = (1184,65)
        avail_date = key['date_avail']
        color = 'rgb(0, 0, 0)' # black color
        draw.text((x, y), avail_date, fill=color, font=avail_date_font)

        (x,y) = (203,363)
        dose = str(key['capacity'])
        color = 'rgb(0, 0, 0)' # black color
        draw.text((x, y), dose, fill=color, font=count_font)

        (x,y) = (197,492)
        age_lim = "45"
        color = 'rgb(0, 0, 0)' # black color
        draw.text((x, y), age_lim, fill=color, font=count_font)
        

        (x,y) = (382,609)
        vaccine_name = key['vaccine']
        color = 'rgb(139,0,0)' # maroon color
        draw.text((x, y), vaccine_name, fill=color, font=vaccine_font)

        (x,y) = (1054,134)
        dist_names = dist_name
        color = 'rgb(48,8,8)' # black color
        draw.text((x, y), dist_names, fill=color, font=dist_font)

        image.save('images/optimized.png', optimize=True, quality=20)
        img_path = 'images/optimized.png'
        api.update_with_media(img_path,status)
