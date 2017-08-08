'''
Created on 2017. 8. 7.

@author: acorn
'''
"""
Aug 8, 2017 19:42.
첫 4페이지 crawling -> console 완료.


// TODO:
0. 중요!! 5페이지에서부터 price, deliveryFee, seller length가 불일치!!! -> 다른 crawling방법 모색.
1. csv파일에 누적저장.
2. title -> keyword작업.
3. model -> phone기종 변환.


"""

from pandas import Series, DataFrame
import numpy as np 
import pandas as pd
import sys, pymysql

## visualization
#import matplotlib.pyplot as plt
#from matplotlib import font_manager, rc
#font_name= font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
#rc('font', family = font_name)

## timeseries
from datetime import datetime

from bs4 import BeautifulSoup as BeautifulSoup
import urllib.request



model = []
title = []
price = []
deliveryFee = []
seller = []
pkg = "com.mavdev.focusoutfacebook"
opener = urllib.request.build_opener()


def crawling(pg):
    url = "http://market.cetizen.com/market.php?q=market&auc_sale=1&escrow_motion=3&sc=1&qs=&auc_wireless=&auc_uid=&stype=&akeyword=&just_one=&just_one_name=&just_one_pcat=&view_type=&m%5B1%5D=1&auc_price1=&auc_price2=&keyword_p=&pno=&pw=&p="+str(pg) + pkg
    data = opener.open(url).read()
    soup=BeautifulSoup(data, "html.parser")
    
    # print(soup)
    # ul = soup.findAll('ul', {'style': 'clear:both;width:100%;overflow:hidden;margin:0px auto;padding-top:15px;padding-bottom:15px;border-bottom:1px solid #DBDBDB;'})
    # for k in ul:
    #     print(k.text)
    # print('#'*30, li)
    
    
    a = soup.findAll('a', {'href': lambda L: L and L.startswith('/market.php?')})
    for (i,p) in zip(a,range(len(a)) ):
        if p>5:
#             print(p,' :: ' ,i.text)
            if p%2 ==0:
                model.append(i.text)
            else:
                title.append(i.text)
        
    # print(model)
    # print(title)
    print('### now working in page', pg)
    print('len(model): ', len(model))
    print('len(title): ', len(title))
    print('#'*50)
    b = soup.findAll('span', {'class': 'ls-0'})
    for (j,q) in zip(b,range(len(b)) ):
        if q>5:
#             print(q,' :: ' ,j.text)
            if q%3 ==0:
                price.append(j.text)
            elif q%3 ==1:
                deliveryFee.append(j.text)
            else:
                seller.append(j.text)
        
    # print(price)
    # print(deliveryFee)
    # print(seller)
    print('### now working in page', pg)
    print('len(price): ', len(price))
    print('len(deliveryFee): ', len(deliveryFee))
    print('len(seller): ', len(seller))
    print('#'*50)
    
    
    # t=soup.find('span',{'class':'clr04'})
    # print(t.text)
#################### function crawling(pg) END  
   



s1 = datetime.now()
for pg in range(1,5):
    crawling(pg)
# //TODO: page5에서 price, defee, seller갯수가 틀어져서 다른 전처리방법을 몰색해야함.
# 4페이지까지는 데이터가 잘나옴. 
s2 = datetime.now()


data = DataFrame({
    'model':model,
    'title':title,
    'price':price,
    'deliveryFee':deliveryFee,
    'seller':seller })
data = data[['model', 'title', 'price', 'deliveryFee','seller']]
pd.set_option('expand_frame_repr', False)  ## 넓게 볼수잇게처리.
print(data)  ## 콘솔에서는 깔끔하게보이는건 아쉽지만 무리.. ㅜㅜ
print('#'*30, '\t\t runtime::', s2-s1)







