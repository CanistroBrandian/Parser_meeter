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
    
    data = pd.DataFrame(dataFrame,columns=['City','Category','Data','Place','Link_place','Event','Link_event','Description','Image','Ganre','Time_start','Price'])
    data = preprocessing_write_df_to_excel(data)
    with pd.ExcelWriter(f'{name}-{datetime.date.today()}.xlsx') as writer:
        data.to_excel(writer)
    print(f'Файл {name} записан за {(time.perf_counter() - timer_start):.02f}')

def preprocessing_write_df_to_excel(data_frame):
    grouped = data_frame.groupby('Link_event')
    for name, group in grouped:
        description_and_image = group[['Description','Image']].iloc[0].to_list()
        group['Description'] = description_and_image[0]
        group['Image'] = description_and_image[1]
        data_frame.update(group)
    return data_frame

def check_existence_link(link):
    for local_link in existence_links:
        if(local_link != link):
            continue           
        else: return None
    existence_links.append(link)
    return link
            
def connection_to_link(local_links): 
    document_responces_arr = []
    if(isinstance(local_links, str)):       
         document_responces_text =  requests.get(local_links, headers = header).text
         soup = BeautifulSoup(document_responces_text,'html.parser')
         return soup
    else: 
        for link in local_links:
            document_responces_arr.append(requests.get(link, headers = header).text)
        return document_responces_arr


def get_links_with_city(links,cities):
    list_links_cities=[]
    for city in cities:
        for link in links:
            list_links_cities.append(link+city)
    return list_links_cities

def parsing_single_page(link):
    if(link == check_existence_link(link)):
        local_doc = connection_to_link(link)
        block_single_page= local_doc.find('div', class_= 'b-page js-afisha')
        description_block = block_single_page.find('div', class_= 'b-afisha_cinema_description_text')
        
        #добавить исключение на пустой блок 
        if description_block != None: description_single_page = ' '.join([desc.text for desc in description_block.findAll('p')])
        image_sibgle_page = block_single_page.find('img', class_='b-afisha-event__image')
        
        return description_single_page, ''.join(image_sibgle_page['src'])
    else: return '',''

user = fake_useragent.UserAgent().random
header = {'user-agent': user}

store_data =[]
local_variable=[]
existence_links = [] #хранит в себе ссылки, которые помещены в датафрейм

i=0
timer_start = time.perf_counter()

cities = ['minsk', 'brest', 'gomel','mogilev','vitebsk','grodno']
links = ['https://afisha.relax.by/kino/',
        'https://afisha.relax.by/theatre/',
        'https://afisha.relax.by/ny/',
        'https://afisha.relax.by/event/',
        'https://afisha.relax.by/conserts/',
        'https://afisha.relax.by/expo/',
        'https://afisha.relax.by/kids/',
        'https://afisha.relax.by/clubs/',
        'https://afisha.relax.by/stand-up/',
        'https://afisha.relax.by/education/',
        'https://afisha.relax.by/sport/',
        'https://afisha.relax.by/quest/',
        'https://afisha.relax.by/entertainment/',        
        ]

links_list_with_cities =get_links_with_city(links,cities)
responces = connection_to_link(links_list_with_cities)

for responce in responces:         
    soup = BeautifulSoup(responce,'html.parser')
    block_scedule = soup.find('div', id = 'append-shcedule')

    city_name = links_list_with_cities[i].split('/')[-1] 
    category_name = links_list_with_cities[i].split('/')[-2] 
      
    # event info
    all_event_list = [event for event in block_scedule.findAll('div', class_='schedule__list')]
    date_event = block_scedule.find('h5')
    place = block_scedule.findAll('div', id='schedule__place_wrap')
    
    for event in all_event_list:       
        data_event = event.find('h5').text #дата
        table_events = event.find('div', id='theatre-table') #Таблица событий за день
        rows_events = table_events.findAll('div', class_='schedule__table--movie__item')#строки события 
        
        for place in rows_events:   
            #определение элементов парсинга        
            name_place = place.find('a', class_='schedule__place-link link')#навание места проведения   
            name_event = place.find('a', class_='schedule__event-link link')# название события
            link_event = name_event.get('href')       #ссылка на событие
            name_ganre = place.find('a', class_='schedule__event-dscr text-black-light')#жанр события
            time_start_arr = place.findAll('a', \
                                        class_='schedule__seance-time schedule__seance--buy js-buy-ticket')#массив время начала
            price_event_arr = place.findAll('span', \
                                            class_='seance-price')#массив цен на билеты
            
            #парсинг каждой страницы 
            
            description_event, image_event = parsing_single_page(link_event)
            
            #проверка значение на None
            if name_place  :
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
            local_variable.append([
                            city_name, category_name,data_event,\
                            name_place.strip() ,link_place, name_event_format, \
                            link_event, description_event,\
                            image_event, name_ganre, \
                            time_start, price_event])
        store_data += local_variable      
        local_variable = []
    i=i+1
to_excel(store_data, 'afishaby')
print(f'Парсинг закончен: {time.perf_counter() - timer_start:.02f}')
