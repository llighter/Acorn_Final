'''
Created on 2017. 8. 9.

@author: acorn
'''
"""
http://creativeworks.tistory.com/entry/PYTHON-3-Tutorials-24-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%9F%AClike-Google-%EB%A7%8C%EB%93%A4%EA%B8%B0-1-How-to-build-a-web-crawler

http://market.cetizen.com/market.php?q=market&auc_sale=1&escrow_motion=3&sc=1&qs=&auc_wireless=&auc_uid=&stype=&akeyword=&just_one=&just_one_name=&just_one_pcat=&view_type=&m%5B1%5D=1&auc_price1=&auc_price2=&keyword_p=&pno=&pw=&p=1


######
거의완성본@@ 
Aug21, 2017
12:48 workDone upto debug #2

JB

 ## TODO:: 
1. soldTitles의 경우, 한 페이지에 같은 제목 복수개중 첫번째 값만 가져온다. 모두 찾기 방법 모색.
2. 마지막4개. 분석하는 변수중 하나로 쓸만할듯.        
>>3. df form.
4. put in mariaDB.
   


"""
import requests
import pandas as pd
from pandas import DataFrame, Series
from bs4 import BeautifulSoup as BS

def spider(startPage, endPage):
    page = startPage
    while page< endPage+1 :
        print('#' * 30 )
        print('#' * 30 ,"   page ::", page)
        print('#' * 30 )
        
        # Web Scrap
        url = 'http://market.cetizen.com/market.php?q=market&auc_sale=1&escrow_motion=3&sc=1&qs=&auc_wireless=&auc_uid=&stype=&akeyword=&just_one=&just_one_name=&just_one_pcat=&view_type=&m%5B1%5D=1&auc_price1=&auc_price2=&keyword_p=&pno=&pw=&p='+ str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BS(plain_text, 'lxml')  ## lxml은 html.parser보다 월등히빠름.
        
        ## 리스트 초기할당
        soldTitles = []
        titles = []
        models = []
        soldLists = []
        prices = []
        deliverFees = []
        sellerNames = []
        sellTimes = []
        options = []
        
        # 리스트의 기본 container.
        soupSel01 = soup.select('ul')  ## Note: 이거 .map function 해도 먹힐거같다?
        for uls in soupSel01:
            # find sold items
            sTitles = uls.findAll('span', {'class': 'clr02', 'style': 'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block;'})
            for soldTitle in sTitles:
                soldTitles.append(soldTitle.text)
            # All listed titles
            allTitles = uls.findAll('span', {'style': 'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block;'})
            for allTitle in allTitles:
                titles.append(allTitle.text) 
            # All listed prices
            sellInfos = uls.findAll('span', {'class': 'ls-0'})
            for (sellInfo,idx) in zip(sellInfos,range(len(sellInfos)) ):
                if idx ==0:
                    prices.append(sellInfo.text)
                elif idx ==1:
                    deliverFees.append(sellInfo.text)
                elif idx ==2:
                    sellerNames.append(sellInfo.text)
            # selling time.  - '~~분전' 'class': 'p11 clr02 '  // '@@시:##분' 'class': 'ls-0'
            sTimes = uls.findAll('li', {'style': 'width:5%;float:left;overflow:hidden;text-align:center;padding-top:2px;'})
            for sTime in sTimes:
                sellTimes.append(sTime.text)
            fourOps = uls.findAll('li', {'style': 'width:16%;float:right;overflow:hidden;padding-right:0px;text-align:right;'})
            for fourOp in fourOps:
                options.append(fourOp.text.replace('\n', '').strip() )

        # 팔린물품 in 전체물품 -> 비교해서 index번호 따기.
        if len(soldTitles) != 0:
            soldLists = [titles.index(x) for x in soldTitles] # index number(0 ~) in the list.
           
        # Model id.
        soupSel02 = soup.select('ul > li > div > a > span' )  ## 이거 .map function 해도 먹힐거같다?
        for allModel in soupSel02:
            models.append(allModel.text)
          
        # Checking num of elements in list is 20.    
        lenList = [models, titles, prices, deliverFees, sellerNames, sellTimes ]
        for check in lenList:
            if len(check) != 20:
                print('length not 20. :: len:', len(check),'   list:: ', check )
        # show result
#         print('models :: ',models)    
#         print('titles :: ',titles)    
#         print('prices :: ',prices)    
#         print('deliverFees :: ',deliverFees)    
#         print('sellerNames :: ',sellerNames)    
#         print('sellTimes :: ',sellTimes)    
        
        # 팔린물건 존재할경우 print.   
        if len(soldTitles) != 0:
            print('soldList :: ',soldLists )    
            print('soldTitle :: ',soldTitles)    
#             print('titles[soldLists] :: ',[titles[x] for x in soldLists])   ## 지우지말것.  ## 원래 리스트와의 비교 
        
        
        df = DataFrame(data = {'models':models,
                        'titles': titles,
                        'prices': prices,
                        'deliverFees': deliverFees,
                        'sellerNames': sellerNames,
                        'sellTimes': sellTimes,
                        'options': options })
        # 페이지 넓게 보여줌.
        pd.set_option('expand_frame_repr', False)
        print(df)
        
        print('#' * 30 ,"  df.describe()  ::")
        print(df.describe())
        
        
        
        
        
        
        
        
        
        
        
        
        
        # 리스트 초기화
        soldTitles = []
        titles = []
        models = []
        soldLists = []
        prices = []
        deliverFees = []
        sellerNames = []
        sellTimes = []
        options = []
        
        
        
        page+=1



spider(18, 25) ## page start, end.


