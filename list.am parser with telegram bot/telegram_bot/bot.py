import config
import telebot
import requests
from bs4 import BeautifulSoup as bs


# #getting inputs
# inp = input('search : ')
# pr = input('price `from-to` in dollars : ')


# #price from to 
# pr_pars = pr.split(' ')
 
# pr_from = int(pr_pars[0])

# pr_to = int(pr_pars[1])

# inp = inp.split(' ')
# inp_pars = ''
# for x in range(len(inp)):
#     if x == len(inp)-1 :
#         inp_pars += inp[x]
#     else : 
#         inp_pars += inp[x] + '+'

  

max_page = 3  
pages = [] 
for x in range(1,max_page + 1):
    pages.append( requests.get('https://www.list.am/category/23/camry?q={}'.format(max_page)  ))







bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message): 
	bot.send_message(message.chat.id, "Hello {0.first_name} \n I`m <b> best bot in the world </b>".format(message.from_user,bot.get_me()),parse_mode='html')
  
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)
 
@bot.message_handler(commands=['search'])
def send_welcome(message): 

    cnt = 0
    for r in pages : 
     
        html = bs(r.content,'html.parser') 
    
        for el in html.select('a'):

            try :
                #for products with dollar price
                title = el.select('.l')
                price = el.select('.p')
                img = el.select('img')
                price_parse =  price[0].text
                price_parse = price_parse.split('$')[1]
                price_parse = price_parse.split(',')
                price_parse = price_parse[0] + price_parse[1]
                price_parse = int(price_parse) 
                
                tmp = str(img[0])
                tmp = tmp.split('//')
                s = tmp[1].split('"')
                s = str(s[0])
                if 1500 < price_parse < 7000 : 
                    cnt += 1  
                    bot.send_message(message.chat.id, "{} : <b> {} </b> : {} ".format(cnt,title[0].text,price_parse,bot.get_me()),parse_mode='html')
                    bot.send_photo(message.chat.id,s)  
            except:      
                pass     
    
bot.polling()    #EGS  