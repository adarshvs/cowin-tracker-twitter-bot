#!/usr/bin/env python3
import datetime,time
import os
import requests 
import json
import tweepy

# authentication of access token and secret
consumer_key = 'consumer key'
consumer_secret = 'consumer secrets'
access_token = 'access token'
access_token_secret = 'access token secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#get current date
def getDate(): 
    current_time = datetime.datetime.now()
    day = current_time.day
    month = current_time.month
    year = current_time.year
    date = "{dd}-{mm}-{yyyy}".format(dd=day,mm=month,yyyy=year)
    time.sleep(900) # set time interval for checking vaccine availability, default time : 15 minutes
    return date
#get name of district
def getDistrictID(st_id, lookout_district): 
    district_name = ''
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{st}".format(st = st_id)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36' }
    try:
        response = requests.get(url,headers=headers)
        parsed_response = json.loads(response.text)
        district_length = len(parsed_response['districts'])
        for idx in range(district_length):
            if((parsed_response['districts'][idx]['district_id']) == lookout_district):
                district_name = parsed_response['districts'][idx]['district_name']
        return (district_name)
    except Exception as e:
        print(e)
        
        
#get vaccine slot details 
def getCOWIN(date,district_id):
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}".format(district_id = district_id, date = date)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36' }
    response = requests.get(url,headers=headers)
    return json.loads(response.text)

#check slot availability
def checkAvailability(payload):    
    if('centers' in payload.keys()):
        length = len(payload['centers'])
        output = []
        if(length>1):
            for i in range(length):
                sessions_len = len(payload['centers'][i]['sessions'])
                for j in range(sessions_len):
                    if((payload['centers'][i]['sessions'][j]['available_capacity']>0)): 
                        res = {'available_center' : payload['centers'][i]['name'],\
                        'capacity' : payload['centers'][i]['sessions'][j]['available_capacity'],\
                        'vaccine': payload['centers'][i]['sessions'][j]['vaccine'] ,\
                        'date_avail' : payload['centers'][i]['sessions'][j]['date'] }
                        output.append(res)
            
    return output
while True:
    st_id = 17
    lookout_district = 301
    date = getDate()
    district_id = lookout_district
    dist_name = getDistrictID(st_id, lookout_district)
    payload = getCOWIN(date,district_id)
    responses =checkAvailability(payload)
    for key in responses:    
        status =  "Cowin Vaccine available at "+ dist_name +" ("+key['date_avail']+"):\n "+ str(key['capacity'])+" doses of "+ key['vaccine']+" vaccine available at "+ key['available_center'] +"\n #getvaccinated #cowin \n posted by:#covintrackerbot"
        api.update_status(status)
