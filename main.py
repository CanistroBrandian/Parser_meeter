import requests
import random
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import fake_useragent
import numpy as np
import pandas as pd
from pandas import ExcelWriter

def to_excel(dataFrame):
    data = pd.DataFrame(dataFrame,columns=['Data','Place','Link_place','Event','Link_event','Ganre','Time_start','Price'])
    with pd.ExcelWriter('output.xlsx') as writer:
        data.to_excel(writer)

user = fake_useragent.UserAgent().random
header = {'user-agent': user}
store_data =[]
local_variable=[]

link = ['https://afisha.relax.by/kino/minsk/',
        'https://afisha.relax.by/theatre/minsk/',
        'https://afisha.relax.by/ny/minsk/',
        'https://afisha.relax.by/event/minsk/',
        'https://afisha.relax.by/conserts/minsk/',
        'https://afisha.relax.by/expo/minsk/',
        'https://afisha.relax.by/kids/minsk/',
        'https://afisha.relax.by/clubs/minsk/',
        'https://afisha.relax.by/stand-up/minsk/',
        'https://afisha.relax.by/education/minsk/',
        'https://afisha.relax.by/sport/minsk/',
        'https://afisha.relax.by/quest/minsk/',
        'https://afisha.relax.by/entertainment/minsk/',
        
        ]
responce = requests.get(link,headers= header).text
res = 'asd'

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
        
        name_place = place.find('a', class_='schedule__place-link link')#   
        name_event = place.find('a', class_='schedule__event-link link')# название события
        link_event = name_event.get('href')       #ссылка на событие
        name_ganre = place.find('a', class_='schedule__event-dscr text-black-light')#жанр события
        time_start_arr = place.findAll('a', \
                                       class_='schedule__seance-time schedule__seance--buy js-buy-ticket')#массив время начала
        price_event_arr = place.findAll('span', \
                                        class_='seance-price')#массив цен на билеты
        
        if name_place or name_ganre or price_event_arr:#проверка значение на None
            link_place = name_place.get('href')
            name_place = name_place.text
            name_ganre = name_ganre.text
            
            prev_name_place = name_place
        else:
            name_place = prev_name_place
               
        #форматирование строк
        time_start = ', '.join([time.text.strip() \
                                for time in time_start_arr])#
        price_event = ', '.join([price.text \
                                for price in price_event_arr])#
        data_event=' '.join(data_event.split())\
                      .split(',')[0]
        name_event_format = name_event.text
        name_event_format = ' '.join(name_event_format.split()).split(',')[0]
        
        #Добавление значений в массив 
        local_variable.append([data_event,\
                        name_place.strip() ,link_place,\
                        name_event_format,link_event,\
                        name_ganre,time_start,\
                        price_event])
    store_data += local_variable
    
    local_variable = []
df = pd.DataFrame(store_data,columns=['Data','Place','Link_place','Event','Link_event','Ganre','Time_start','Price'])


to_excel(store_data)

