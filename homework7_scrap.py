from bs4 import BeautifulSoup as bs
import requests
import json


# a_tags = soup.find_all('a')

class Parser :
    def __init__(self:object) -> None :
        pass
    
    def get_html(self:object,path:str) -> object : 
        r = requests.get(path).text
        soup = bs(r,'html.parser')
        return soup

    def get_a_tags(self:object,path:str) -> list :
        a_tags = self.get_html(path).find_all('a',href=True)
        return a_tags
    
    def filter_a_tags(self:object,path:str) -> list :
        a_tags = self.get_a_tags(path)
        result = []
        for a in a_tags:
            if 'https://' in a['href'] or 'www.' in a['href'] or a['href'][0] == '#':
                pass
            else:
                result.append(a)
        return list(set(result))

    

    def parse_by_depth(self:object,depth:int,start_path:str,result=dict()) -> dict :
        filtered_a_tags = self.filter_a_tags(start_path)
        result['title'] = self.get_html(start_path).find('title').text
        result['links'] = []
        page_name = start_path.split('//')[1].split('/')[0]
        page_name = f'https://{page_name}'
        limit = 0
        for a in filtered_a_tags :
            new_link = f'{page_name}{a["href"]}'
            new_d = {}
            print( f'Working on this link - {new_link} , please wait . . .')
            new_d[a["href"]] = {}
            new_d[a['href']]['title'] = self.get_html(new_link).find('title').text
            # new_d['links'] = [] #[x['href'] for x in self.filter_a_tags(new_link)]
            new_d[a['href']]['links'] = []
            filtered_a1_tags = self.filter_a_tags(new_link)
            limit1 = 0
            for a1 in filtered_a1_tags :
                new_link1 = f'{page_name}{a1["href"]}'
                new_d1 = {}
                # print( f'Working on this link - {new_link} , please wait . . .')
                new_d1[a1["href"]] = {}
                new_d1[a1['href']]['title'] = self.get_html(new_link1).find('title').text
                # new_d['links'] = [] #[x['href'] for x in self.filter_a_tags(new_link)]
                new_d1[a1['href']]['links'] = []
                new_d[a['href']]['links'].append(new_d1)
                limit1+=1
                if limit1 == 3:
                    break




     
            result['links'].append(new_d)
            
            # if depth != 0 :
            #     self.parse_by_depth(depth-1,new_link,result)
            limit += 1
            if limit == 3:
                break
        return result


    def to_json(self:object,dct:dict) :
        return json.dumps(dct, indent = 4 )
    # def to_depth(self,path,page_name,depth):
        # new_d = {}
        # if depth > 0:
        #     new_d['title'] = self.get_html(path).find('title').text

               

if __name__ == "__main__":
    p = Parser()
    # print(p.get_a_tags())
    print( p.to_json(p.parse_by_depth(3,'https://en.wikipedia.org/wiki/Main_Page') ) )   