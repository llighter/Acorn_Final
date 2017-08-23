'''
Created on 2017. 8. 9.

@author: acorn
'''
"""
-
http://market.cetizen.com/market.php?q=market&auc_sale=1&escrow_motion=3&sc=1&p=

@@@@@ 참고
@ 웹 크롤링
http://creativeworks.tistory.com/entry/PYTHON-3-Tutorials-24-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%9F%AClike-Google-%EB%A7%8C%EB%93%A4%EA%B8%B0-1-How-to-build-a-web-crawler
@ DataFrame -> mariaDB 방법.
http://creativeworks.tistory.com/entry/how-to-insert-dataframe-data-into-mysql-database-using-pymysqlpure-python3-library
@ DB배우기.
http://blog.naver.com/PostView.nhn?blogId=hmkuak&logNo=220583392375

######
Aug23, 2017. 19:43
JB

Work Done
------- Aug 21, 2017
2. 마지막4개. 분석하는 변수중 하나로 쓸만할듯.        
3. df form.
4. put in mariaDB.

-------- Aug 22, 2017
0. Gdrive - 5차산출 > 크롤링 > DB > cetizen0822_1352.sql   ## 13:52분 기점으로 200pg분량 정보출력 및  mysql문 저장.
1. auc_no따오기 - cf) 판매자정보는 프로젝트에 큰 영향없는 분석데이터라서 추후 크롤링.
6. soldLists로 df에 state_name,state_code 추가..


-------- Aug 23, 2017
2. last4 options>> 설명나누기!!  ex) span['onmouseover']
3. 분, 초 -> 오늘날짜.

 ## programming TODO:: 
-------- Aug 22, 2017
00. 가독성증가용 :: 함수/ 클래스화. 제발 ㅜㅜ
3. All listed prices 더 좋은방법 모색. <<< if, elif가 필요없다.
4. S(SK),K(KT),L(LG U+) 통신사 태크 제외시키고 저장..
5. 인기가 없거나 "데이터가 많은걸 저장"하고, 웹페이지에서 필터적용할수 있게끔.

4. 슬슬 데이터 -> matplot사용해서 그래프그리기.
5. word clouding

??. soldTitles의 경우, 한 페이지에 같은 제목 복수개중 첫번째 값만 가져온다. 모두 찾기 방법 모색.


 ## Project TODO:: 
0. 각기종의 첫 판매시기, 판매시기 전 가장 최근10개 기종 가격변동 확인.
1. 웹페이지 연동.
2. 해킹 - 페이지에 나타나지 않는 데이터 



"""
import requests
import pandas as pd
from pandas import DataFrame, Series
from bs4 import BeautifulSoup as BS
import mysql.connector
from sqlalchemy import create_engine
import pymysql, sys
from datetime import datetime
import re
from string import digits

def spider(startPage, endPage):
    page = startPage
    while page< endPage+1 :
        
        # board table.
        titles = []         # list_title
        soldTitles = []     # temp. soldLists추출용.
        soldLists = []      # temp. 판매중, 팔림.
        itemState = ['' for i in range(20)]    # list_state_code :: 판매중(''), 팔림(sold out).
        prices = []         # list_phone_price
        aucNos = []         # list_id        #http://market.cetizen.com/market.php?q=view&auc_no=aucNos    ## 상세게시글
        sellTimes = []      # list_uploadTime
        deliverFees = []    # 배달비용 0~
        sellerNames = []    # phone_seller
        
        options = []        # temp. phone_options ex) 만료선택확정중
                            # 선택: 선택약정(20% 요금할인 약정가입) 적용가능 , 불가: 선택약정할인 적용불가
        guarantee = []      # A/S: 무상 보증 미확인 ,보증: 무상 보증기간 잔여 , 만료:무상 보증기간 만료
        contrant = []       # 선택: 선택약정(20% 요금할인 약정가입) 적용가능 , 불가: 선택약정할인 적용불가
        changes = []        # 확정: 확정기변, 유심: 유심기변
        conditions = []     # 미사용, 상(무흠집), 중(생활흠집), 하(번인/잔상/파손)
        pInfoSet = []       # temp. aucNos.phoneId.phoneName 모음.
        agency = []         # 통신사 SK, KT, LG
        
        # phone table
        phoneId = []        # phone_id      # http://market.cetizen.com/market.php?q=info&pno=phoneId    ## 해당 폰 정보
        models = []         # phone_model    
        phoneName = []      # phone_name    
        
        date = datetime.now().strftime('%Y-%m-%d')
        print('#' * 30 )
        print('#' * 30 ,"   page ::", page)
        print('#' * 30 )
        
        # Web Scrap
        url = 'http://market.cetizen.com/market.php?q=market&auc_sale=1&escrow_motion=3&sc=1&p='+ str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BS(plain_text, 'lxml')  ## lxml은 html.parser보다 월등히빠름.
        
        ## 리스트 초기할당
        
        # 리스트의 기본 container.
        soupSel01 = soup.select('ul')  
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
                    deliverFees.append(sellInfo.text.replace('무료','0').replace('-','0'))
                elif idx ==2:
                    sellerNames.append(sellInfo.text)
            # selling time.  
            sTimes = uls.findAll('li', {'style': 'width:5%;float:left;overflow:hidden;text-align:center;padding-top:2px;'})
            for sTime in sTimes:
                if '-' in sTime.text:
                    time01 = datetime.strptime(sTime.text, '%m-%d')
                    time02 = time01.replace(year=2017).strftime('%Y-%m-%d')
                    sellTimes.append(time02)
                else:
                    sellTimes.append(date)
                    
        # four options
        soupSel04 = soup.select('li')
        for lis in soupSel04:
#             print(lis)
            fourOps = lis.findAll('span', {'style': re.compile('float:left;display:block;overflow:hidden;width:.*.margin-left:5px.*')})
#             liss = uls.findAll('li', {'style':  'width:16%;float:right;overflow:hidden;padding-right:0px;text-align:right;'})
            for fourOp in fourOps:
                if fourOp.has_attr('onmouseover') :
#                     print(fourOp['onmouseover'].strip('OnIconShow(').strip(');').replace("'","").lstrip(digits).replace(",","") )    
                    options.append(fourOp['onmouseover'].strip('OnIconShow(').strip(');').replace("'","").lstrip(digits).replace(",","") )    
                elif fourOp.has_attr('title') :
#                     print(fourOp['title'])
                    options.append(fourOp['title'])
                else:
                    options.extend( ['(미등록)','(미등록)'] )
#         print(' ::: ', len(options),' ::: ', (options))
        for op, idx in zip(options, range(len(options)) ):
#             print(idx, ' :: ', op)
            if idx%4 ==0 :
                guarantee.append(op)
            elif idx%4 ==1 :
                contrant.append(op)
            elif idx%4 ==2 :
                changes.append(op.replace('유심기변 확정기변','모름'))
            elif idx%4 ==3 :
                conditions.append(op)

        # 팔린물품 in 전체물품 -> 비교해서 index번호 따기.
        if len(soldTitles) != 0:
            soldLists = [titles.index(x) for x in soldTitles] # index number(0 ~) in the list.
            for soldItemNo in soldLists:
                itemState[soldItemNo] = 'sold out'
        # Model id.
        soupSel02 = soup.select('ul > li > div > a > span' )  ## 이거 .map function 해도 먹힐거같다?
        for allModel in soupSel02:
            tempModel = allModel.text
            agentLetter = tempModel.split(' ')[0][-1]
            if agentLetter == 'L' or agentLetter == 'K' or agentLetter == 'S':
                tempList = tempModel.split(' ')
                tempList[0] = tempList[0][0:-1]
                tempModel = " ".join(str(s) for s in tempList) 
                if agentLetter == 'L':
                    agency.append('LG U+')
                elif agentLetter == 'S':
                    agency.append('SKT')
                elif agentLetter == 'K':
                    agency.append('KT')
            else:
                agency.append('All')
                        
            models.append(tempModel)
          
        soupSel03 = soup.select('li')
        for lis in soupSel03:
            divs = lis.findAll('div', {'style': 'overflow:hidden;cursor:hand;cursor:pointer;margin-top:2px;margin-left:5px;'})
            for div in divs:
                div = div['onmouseover'].strip('OnUserMenuShow(').strip(');').replace("'","") 
                pInfoSet.append(div)
        
        # Checking num of elements in list is 20.    
        lenList = [models, titles, prices, deliverFees, sellerNames, sellTimes, aucNos, phoneId, phoneName ]
        for check in lenList:
            if len(check) % 20 != 0:
                print('length not multiple of 20 . :: len:', len(check),'   list:: ', check )
        # 팔린물건 존재할경우 print.   
        if len(soldTitles) != 0:
#             print('soldList :: ',soldLists )    
#             print('soldTitle :: ',soldTitles)    
#             print('titles[soldLists] :: ',[titles[x] for x in soldLists])   ## 지우지말것.  ## 원래 리스트와의 비교 
            pass
        
        for (pInfo,p) in zip(pInfoSet, range(len(pInfoSet))):
            aucNos.append(pInfo.split(',')[0]) 
            phoneId.append(pInfo.split(',')[1]) 
            phoneName.append(pInfo.split(',')[2])
        
        df = DataFrame(data = {
                        'aucNos': aucNos,#1
                        'models':models,#1
                        'agency': agency,
                        'phoneName': phoneName,#1
                        'prices': prices,#1
                        'itemState': itemState,#
                        
                        'sellTimes': sellTimes, #1
                        'sellerNames': sellerNames,#1
                        'guarantee': guarantee,#1
                        'contrant': contrant,#1
                        'changes': changes,#1
                        
                        'conditions': conditions,#1
                        'titles': titles,#
                        'deliverFees': deliverFees,#1
                        'phoneId': phoneId })#1
        
        df = df[['aucNos','models','agency','phoneName','prices','itemState',
                 'sellTimes','sellerNames','guarantee','contrant','changes',
                 'conditions','titles','deliverFees','phoneId']]
        
        # 페이지 넓게 보여줌.
        pd.set_option('expand_frame_repr', False)
#         print(df)
        
#         print(df.describe())   
            
        dfToMaria(df)
        
        page+=1
    ### while loop END
        
    


def dfToMaria(df):
    ###Anaconda prompt:: pip install mysql-connector
    ###Anaconda prompt:: pip install mysql-connector-python-rf
    
    try:
        con = pymysql.connect(host = 'localhost', port = 3306, 
                              user = 'root', passwd = '11111', 
                              db = 'crawl', charset = 'utf8')
        engine = create_engine('mysql+mysqlconnector://root:11111@localhost:3306/crawl', echo=False)
        df.to_sql(name='table0823_test002', con=engine, if_exists = 'append', index=False)
        
        con.commit()
        print('-'*30, ' insert df in Maria :: Well done')
    
    except:
        print('-'*30, ' insert df in Maria :: went Wrong ::\n', sys.exc_info())
        
        con.rollback()
    finally:
        print('='*30, ' insert df in Maria :: finally')
        con.close()



s1 = datetime.now()
spider(1,10) ## page start, end.
s2 = datetime.now()
print('$'*50, 'time elapsed :: ', s2-s1)

