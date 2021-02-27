"""

Scrape url - 
https://www1.arun.gov.uk/aplanning/OcellaWeb/planningSearch?action=Search&showall=showall&reference=&location=&OcellaPlanningSearch.postcode=&area=&applicant=&agent=&undecided=&receivedFrom=01-01-21&receivedTo=31-01-21&decidedFrom=&decidedTo=

author : Vlad Harutyunyan

"""

from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
import csv
import requests
import os
from calendar import monthrange

# import asyncio
# import aiohttp

requests_session = requests.Session()


csv_columns = ['Url','Address','ReferenceNumber','Validateddate','Status','Proposal']

csv_path = os.path.abspath(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'result.csv'))
    
csv_file = open(csv_path, 'w')
writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
writer.writeheader()

# async def get_site_content(SELECTED_URL):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(SELECTED_URL) as resp:
#             text = await resp.read()

#     return bs(text.decode('utf-8'), 'html5lib')

class Scraper :
    def __init__(self):
        pass
    
    def __get_html(self:object, fromm:str, to:str) -> list:
        r = requests_session.get(f'https://www1.arun.gov.uk/aplanning/OcellaWeb/planningSearch?action=Search&showall=showall&reference=&location=&OcellaPlanningSearch.postcode=&area=&applicant=&agent=&undecided=&receivedFrom={fromm}&receivedTo={to}&decidedFrom=&decidedTo=')
        strainter = ss('table')
        html = bs(r.text,'lxml',parse_only=strainter)

        '''
        Caught link for every item 
        '''

        infoblocks = html.findAll('a',href=True)
        return infoblocks

    def __parse_data(self:object,start_date:str,end_date:str) -> None:
        data = self.__get_html(start_date,end_date)
        print('Your request in progress please wait...')
        for x in data :
            link = f'https://www1.arun.gov.uk/aplanning/OcellaWeb/{x.get("href")}'
            item = {}
            r = requests_session.get(link)
            innerstrainter = ss('table')
            innerhtml = bs(r.text,'lxml',parse_only=innerstrainter)
            innerinfoblocks = innerhtml.findAll('tr')

            '''
            Parse data from html document
            '''
            item['Url'] = link
            item['Address'] = innerinfoblocks[4].findAll('td')[1].text
            item['ReferenceNumber'] = innerinfoblocks[1].findAll('td')[1].text
            item['Validateddate'] = innerinfoblocks[8].findAll('td')[1].text
            item['Status'] = innerinfoblocks[2].findAll('td')[1].text
            item['Proposal'] = innerinfoblocks[3].findAll('td')[1].text

            '''
            Write data to csv file 
            '''
        
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writerow(item)

    def get_full_data(self:object,startyear:int,endyear:int) -> None:
        month = 1

        while startyear != endyear-1 :
            

            num_days = monthrange(startyear, month)[1] # num_days = 28
            start_date = f"01-{month}-{startyear}"
            end_date = f"{num_days}-{month}-{startyear}"

            if month < 10 :
                start_date = f"01-0{month}-{startyear}"
                end_date = f"{num_days}-0{month}-{startyear}"

            print(f'Parsing data - {start_date},{end_date}')

            '''
            If retrieve more than 200 results , just skip
            '''
            try :
                self.__parse_data(start_date,end_date)
            except :
                print('To many results for this date , skiped')

            month -= 1
            if month < 1 :
                month = 12
                startyear -= 1
        csv_file.close()
        
if __name__ == '__main__':
    s = Scraper()
    '''
    Result for date from 2021,01,01 to 2020,01,01
    '''
    s.get_full_data(21,20)
