import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://afisha.relax.by/kino/minsk/')
        soup = BeautifulSoup(html, 'html.parser')
        events = soup.find_all(class_='h5 h5--compact h5--bolder u-mt-6x')
        for event in events:
            title = event.find('a').text
            place_link = event.find(class_='schedule__place-link link').text
            event_link = event.find(class_='schedule__event-link link').text
            seance_time = event.find(class_='schedule__seance-time schedule__seance--buy js-buy-ticket').text
            price = event.find(class_='seance-price').text
            print(f'Title: {title}\nPlace: {place_link}\nEvent link: {event_link}\nSeance time: {seance_time}\nPrice: {price}\n---')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

