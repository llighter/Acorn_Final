'''
Created on 2017. 8. 29.

@author: acorn
'''
"""

"""

from pandas import Series, DataFrame
import numpy as np 
import pandas as pd
import sys, pymysql
from sqlalchemy import create_engine

## timeseries
from datetime import datetime
import pymysql as pms
import sys

def getIphone():
    try:
        con = pms.connect(host="35.190.226.198", port=3306, user="root", password="abc123", db="test", charset="UTF8")
        cursor = con.cursor()
        
        cursor.execute('select count(id) from past_iphone')
        count = cursor.fetchone()[0]
        blocks = np.ceil(count/1000)
        print(count, '// ',blocks)
        
        block = 0
        
        while block < blocks:    
#             cursor.execute('''
#                 select * from now_iphone
#                 where id = 11582864 or id = 11582872 or id = 11589685 or id = 11598018 or id = 11627517 or 
#                 id = 11629547 or id = 11695688 or id = 11704964
#             ''')
            
            
            cursor.execute('''
            SELECT
            A.*
            FROM
            (
                SELECT
                    @ROWNUM := @ROWNUM + 1 AS ROWNUM,
                    past_iphone.* 
                FROM
                    past_iphone,
                   (SELECT @ROWNUM := 0) R
            ) A
            WHERE
                A.ROWNUM between %s and %s
           
            '''%(block*1000, (block+1)*1000 - 1)
            ) ## 만약 utf8 charset이없을땐 한글대신 ?? 가뜬다.
            resultSet = cursor.fetchall() # 듀플로 모두 가져옴
#             num_fields = len(cursor.description)
            field_names = [i[0] for i in cursor.description]
            
            lists = []
            for item in resultSet:
        #         print(item)
                lists.append(item)
            print('######## block range ', block*1000, '~', (block+1)*1000 )
            
            pd.set_option('expand_frame_repr', False)
            df = DataFrame(lists)
            df.columns = field_names
            
            seperateModels(df)
            
            block+=1
            
    except:
        print('exception occured\n', sys.exc_info())
#         print(df)
        con.rollback()
        print('#####rollback done')
    finally:
        con.close()
        pass
    
def seperateModels(df):       
    model = []
    modelGB= []
    
    tempModels = list(df['MODEL'])  ## 리스트형태 컬럼명
    for tempModel in tempModels:
        tempModel = tempModel.strip().split(' ')
        temp = tempModel
#         agentLetter = tempModel[0][-1]
#         if agentLetter == 'L' or agentLetter == 'K' or agentLetter == 'S':
#             tempModel[0] = tempModel[0][0:-1]
#         
        if len(tempModel) == 2:
            if tempModel[0] == 'iPhone' and '6s' == tempModel[1]:
                model.append('iPhone_6s')
                modelGB.append('N/A')
            else:
                model.append(tempModel[0])
#                 print(tempModel[0])
                modelGB.append(tempModel[1])
    #             print(tempModel[1])

            
        elif len(tempModel) == 1:
            
            if '-8' in tempModel[0]:
                modelGB.append('8GB')
            elif '-16' in tempModel[0]:
                modelGB.append('16GB')
            elif '-32' in tempModel[0]:
                modelGB.append('32GB')
            elif '-64' in tempModel[0]:
                modelGB.append('64GB')
            elif '-128' in tempModel[0]:
                modelGB.append('128GB')
            else:
                modelGB.append('N/A')

            if tempModel[0][0] == 'A':
                model.append(tempModel[0][0:5]) ## past_iphone
            elif tempModel[0] == 'undefined':
                model.append('N/A')
            else:
                model.append(tempModel[0]) ## past_iphone
        else:
            if tempModel[0] == 'iPhone7' and  'Plus' == tempModel[1] :
                model.append('iPhone7_Plus')
                modelGB.append(tempModel[2])
            else:
                model.append('N/A')
                modelGB.append('N/A')
                print('no model')
#         print(temp, ' >:> ', model[-1],' :: ', modelGB[-1] )
    print(' >:> ', len(model),' :: ', len(modelGB) )
    df['MODEL'] = model
    df['GB'] = modelGB
    
#     condition = []
#     tempCond = list(df['conditions'])  ## 리스트형태 컬럼명
#     for tempModel in tempModels:
#         tempModel = tempModel.strip().split(' ')
    
    tempModels = list(df['MODEL'])  ## 리스트형태 컬럼명
    for tempModel in tempModels:
        tempModel = tempModel.strip().split(' ')
    
    
## SQL conditions --> 상중하
# UPDATE iphone4_copy SET conditions = 
# CASE 
#     WHEN conditions = '중 (생활흠집 외 양호)' 
#        THEN '중'
#     WHEN conditions = '상(새제품 수준/무흠집)' 
#        THEN '상'
#     WHEN conditions = '미사용' 
#        THEN '미사용'
#     WHEN conditions = '하(번인/잔상/파손)' 
#        THEN '하'
#  ELSE 'N/A'
# END;
    
    
    
    df = df[['ID', 'DATE', 'MODEL','GB', 'KRNAME','PRICE', 'CONTRANT', 'AGENCY', 'GUARANTEE', 'CHANGES', 'CONDITIONS', 'COMPONENT', 'SRC', 'SOLD' ]]
#     print(df)
#     print(df.describe())
    dfToMaria(df)


def dfToMaria(df):
    ###Anaconda prompt:: pip install mysql-connector
    ###Anaconda prompt:: pip install mysql-connector-python-rf
    
    try:
        engine = create_engine('mysql+mysqlconnector://root:abc123@35.190.226.198:3306/test', echo=False)
        df.to_sql(name='past_iphoneTEST01', con=engine, if_exists = 'append', index=False)
        
        print('-'*30, ' insert df in Maria :: Well done')
    
    except:
        print('-'*30, ' insert df in Maria :: went Wrong ::\n', sys.exc_info())


print('#' * 30 ,"")
s01 = datetime.now()
getIphone()
s02 = datetime.now()
print('#' * 15 ," time elapsed ::", s02- s01 )

