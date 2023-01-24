import datetime
import time
import requests
import random
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import fake_useragent
import numpy as np
import pandas as pd
from pandas import ExcelWriter

def to_excel(dataFrame,name):
    data = pd.DataFrame(dataFrame,columns=['Category','Data','Place','Link_place','Event','Link_event','Ganre','Time_start','Price'])
    with pd.ExcelWriter(f'{name}-{datetime.date.today()}.xlsx') as writer:
        data.to_excel(writer)
    print(f'Файл {name} записан за {(time.perf_counter() - timer_start):.02f}')

user = fake_useragent.UserAgent().random
header = {'user-agent': user}
store_data =[]
local_variable=[]
i=0
timer_start = time.perf_counter()

links = ['https://afisha.relax.by/kino/minsk/',
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

def connection_to_link(local_link): 
    document_responces = []
    document_responces_text = ''
    for responce in local_link:
       document_responces_text =  requests.get(responce, headers = header).text
       document_responces.append(document_responces_text)
    return document_responces

def category(local_link):
    category_name_list = [name.split('/')[-3] for name in local_link]
    return category_name_list

responces = connection_to_link(links)

for responce in responces: 
    
    category_name= category(links)                
    soup = BeautifulSoup(responce,'html.parser')
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
            
            if name_place  :#проверка значение на None
                link_place = name_place.get('href')
                name_place = name_place.text
                
                prev_name_place = name_place
            else:
                name_place = prev_name_place
               
            if name_ganre: name_ganre = name_ganre.text
            if price_event_arr: price_event_arr
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
            local_variable.append([category_name[i],data_event,\
                            name_place.strip() ,link_place,\
                            name_event_format,link_event,\
                            name_ganre,time_start,\
                            price_event])
        store_data += local_variable
        
        local_variable = []
    i=i+1
to_excel(store_data, 'afishaby')
print(f'Парсинг закончен: {time.perf_counter() - timer_start:.02f}')
