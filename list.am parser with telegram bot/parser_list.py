import requests
from bs4 import BeautifulSoup as bs


#getting inputs
inp = input('search : ')
pr = input('price `from-to` in dollars : ')


#price from to 
pr_pars = pr.split(' ')
 
pr_from = int(pr_pars[0])

pr_to = int(pr_pars[1])

inp = inp.split(' ')
inp_pars = ''
for x in range(len(inp)):
    if x == len(inp)-1 :
        inp_pars += inp[x]
    else : 
        inp_pars += inp[x] + '+'



max_page = 3  
pages = []
for x in range(1,max_page + 1):
    pages.append( requests.get('https://www.list.am/category/23/{}?q={}'.format(str(x),inp_pars)  ))



cnt = 0
for r in pages : 
     
    html = bs(r.content,'html.parser') 
  
    for el in html.select('a'):

        try :
            #for products with dollar price
            title = el.select('.l')
            price = el.select('.p')
            price_parse =  price[0].text
            price_parse = price_parse.split('$')[1]
            price_parse = price_parse.split(',')
            price_parse = price_parse[0] + price_parse[1]
            price_parse = int(price_parse) 



            if pr_from < price_parse < pr_to : 
                cnt += 1
                print(cnt,":",title[0].text," price = ", price_parse)
        except:   
            pass 