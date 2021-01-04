#!/usr/bin/python3
import sys
from datetime import datetime
import cx_Oracle, redis, json
connectstring='nrk/geefddcdefggg@w'
sqls='''SELECT 
        customer_id||'-'||prod_id pid,
        qty 
    FROM stock 
    WHERE (customer_id = :customer_id or :customer_id is null) 
    AND (prod_id = :prod_id or :prod_id is null)
    AND freeze='N'
    '''
params={"customer_id":None, "prod_id":None}

# 如果有參數的話，，第二個表示customer_id,第三個表示prod_id
# 都沒有的話表示全部的 stock,如上面SQL所示
argc = len(sys.argv)
if argc >=2:
    params["customer_id"] = sys.argv[1]
if argc >=3:
    params["prod_id"] = sys.argv[2]
t1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
## 連接redis，並且使用0號DB當做是存放庫存的位置，沒有參數的話,db(0)全部清空
rd = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)  
if argc == 1:
    rd.flushdb()
dbconn = cx_Oracle.connect(connectstring)
cur = dbconn.cursor()
res=cur.execute(sqls,params)
n=0
# 循環設定至 redis
for r in res:
    print(r[0]+":"+str(r[1]))
    rd.set(r[0],r[1],86400*3)
    n += 1
cur.close()
dbconn.close()

# 看看要多久
t2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("\n"+t1+"~"+t2,n,"records")

