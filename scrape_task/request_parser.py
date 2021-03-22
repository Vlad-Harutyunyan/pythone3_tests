import requests
import json 
import re



def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def parse_request(link):
    r = requests.get(link)
    json_data = json.loads(r.text)
    obj = {}

    #parse overview
    overview = json_data['infoGroups'][0]['list']
    cnt1 = 0
    for x in overview:
        cnt1 += 1
        obj[f'overview_{cnt1}'] = x['label']

    #parse FURNISHING
    furnish = json_data['infoGroups'][1]['list']
    cnt2 = 0
    for x in furnish:
        cnt2 += 1
        obj[f'FURNISHING_{cnt2}'] = x['label']

    #parse SURROUNDINGS
    surrounding = json_data['infoGroups'][2]['list']
    cnt3 = 0
    for x in surrounding:
        cnt3 += 1
        obj[f'SURROUNDINGS_{cnt3}'] = x['label']

    #parse rules
    rules = json_data['policies']
    cnt4 = 0
    for x in rules:
        cnt4 += 1
        obj[f'HOUSERULES_{cnt4}'] = x['label']

    obj['description'] = cleanhtml(json_data['description']['unit']['content'])

    return obj


if __name__== '__main__':
    # Testing
    testlinks = [
        'https://www.casamundo.com/rental/offer/6e3db915e7c8f0c6373632bc74e83b35',
        'https://www.casamundo.com/rental/offer/ad23c52fce800626'
        ]
    
    for link in testlinks:
        print(parse_request(link))