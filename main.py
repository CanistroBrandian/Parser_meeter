import requests
import random
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import fake_useragent
import numpy as np
import pandas as pd
from pandas import ExcelWriter

user = fake_useragent.UserAgent().random
header = {'user-agent': user}

store_data =[]
local_variable=[]

link = 'https://afisha.relax.by/kino/minsk/'
responce = requests.get(link,headers= header).text
soup = BeautifulSoup(responce,'html')
block_scedule = soup.find('div', id = 'append-shcedule')

# event info
all_event_list = [event for event in block_scedule.findAll('div', class_='schedule__list')]
date_event = block_scedule.find('h5')
place = block_scedule.findAll('div', id='schedule__place_wrap')

for event in all_event_list:
    data_event = event.find('h5').text #дата
    table_events = event.find('div', id='theatre-table') #Таблица событий за день
    rows_events = table_events.findAll('div', class_='schedule__table--movie__item')#строки события 
    
    for place in rows_events:
        
        name_place = place.find('a', class_='schedule__place-link link') 
        
        if name_place:
            link_place = name_place.get('href')
            name_place = name_place.text
            prev_name_place = name_place
        else:
            name_place = prev_name_place

        
        name_event = place.find('a', class_='schedule__event-link link')
        link_event = name_event.get('href')       
        name_ganre = place.find('a', class_='schedule__event-dscr text-black-light')
        
        if name_ganre:
            name_ganre = name_ganre.text
            
        time_start_arr = place.findAll('a', \
                                       class_='schedule__seance-time schedule__seance--buy js-buy-ticket')
        price_event_arr = place.findAll('span', \
                                        class_='seance-price')
        time_start = ', '.join([time.text \
                                for time in time_start_arr])
        price_event = ', '.join([price.text \
                                for price in price_event_arr])
        
        local_variable.append([data_event,\
                        name_place,link_place,\
                        name_event.text,link_event,\
                        name_ganre,time_start,\
                        price_event])
    store_data += local_variable
    local_variable = []
df = pd.DataFrame(store_data,columns=['Data','Place','Link_place','Event','Link_event','Ganre','Time_start','Price'])

