# import必要的模組
from fastapi import FastAPI
import uuid,logging,json,os,sys,traceback
from datetime import datetime
import model,config,mypg
#import cx_Oracle
import redis

INIT = { "CUSTOMER_ID":"15035",
    "O":"正確",
    "X":"錯誤"
    }
#--------------------------------------------------------------------------------------
# 將執行的過程記錄
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p',level=logging.INFO)
now = datetime.now()
datestr = now.strftime("%Y%m%d%H%M%S_")
env = os.getenv('ENVIRONMENT')
ticket = 0
logging.info(config.ifs['TITLE'])
##
redispool = redis.ConnectionPool(host=config._redis["host"], port=config._redis["port"], decode_responses=True)
# 如果設定環境參數 ENVIRONMENT = develop,則可在網頁上面執行fastapi的doc,作debug
if env == 'PRODUCTION':
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI()
#dbconn.close()
#--------------------------------------------------------------------------------------
## 只是回應
@app.get("/")
def root():
    retval={"status":INIT["O"],"detail":"alive"}
    return retval

# 查詢REDIS庫存 (ex:APT20-000145), http://nrk/fapi/qty/{prod_id}
@app.get("/qty/{prod_id}")
def get_rdqty(prod_id:str):
    global redispool
    try:
        r = redis.Redis(connection_pool=redispool)
        v = r.get("%s-%s"%(INIT['CUSTOMER_ID'],prod_id,))
        r.close()
        if v is None:
            logging.info("(X) %s is not found"%(prod_id,))
            return {"status":INIT['X'],"detail": []}
        else:
            logging.info("(O) %s = %s"%(prod_id,v))
            return {"status":INIT['O'],"detail": [int(v)]}
    except Exception as e:
        msg = show_error(e)
        logging.info("(X) %s error message:%s"%(prod_id,msg))
        return {"status":INIT['X'],"detail": msg}

# postgres
## 任意的查詢,SQL在config裡面設定
# http://nrk/fapi/qry/{sqlnames}?params=[%s,%s...]
@app.get("/pgqry/{sqlname}")
def pgqry(sqlname:str, params:str =''):
    try:
        paro = json.loads(params) if len(params)>2 else []
    except Exception as e:
        return {"status":INIT['X'],"detail":show_error(e)}
    pg = mypg.pgo(config._pg)
    try:
        sqlstring = config._pg["sqlstrings"][sqlname]
        rows = pg.query(sqlstring,paro)
        total = pg.rowcount
        retval={"status":"正確","detail": {"total":total, "rows": rows} }
        del pg
    except Exception as e:
        retval={"status":"誤訛","detail": show_error(e)}
    return retval

''' 201225
# curl -X GET "http://localhost:8000/ent?params=%7B%22data%22%3A123%7D" -H  "accept: application/json"
@app.get("/ent")
async def _ing(params:str = ''):
    id=str(uuid.uuid1())    #datestr+f"{ticket:08}"
    fname = config.ifs["IN"] + "/" +id
    try:
        p=json.loads(params)
        pload={"type":"file","id":id,"count":0,"data":p} 
        fin=open(fname,"w")
        plstr = json.dumps(pload,ensure_ascii=False)
        fin.write(plstr)
        fin.close()
        logging.info("(O) %s"%(plstr,))
        return {"status":INIT['O'],"detail":pload}
    except Exception as e:
        msg = show_error(e)
        logging.info("(X) %s error message:%s"%(id,msg))
        return {"status":INIT['X'],"detail":show_error(e)}
# redis
# 201224
@app.get("/qin")
async def _qin(params:str = ''):
    id=str(uuid.uuid1())    #datestr+f"{ticket:08}"
    try:
        p=json.loads(params)
        pload={"type":"redis","id":id,"count":0,"data":p} 
        logging.info("(O) %s"%(params,))
        r = redis.Redis(connection_pool=redispool)
        pstr = json.dumps(pload,ensure_ascii=False)
        r.rpush(config._redis["queue"], pstr)
        r.close()
        logging.info("(O) %s"%(pstr,))
        return {"status":INIT['O'],"detail":pload}
    except Exception as e:
        msg = show_error(e)
        logging.info("(X) %s error message:%s"%(id,msg))
        return {"status":INIT['X'],"detail": msg}
'''
@app.post("/qin")
async def _qin(soline:model.SOLINE):
    id=str(uuid.uuid1())
    try:
        solinestr=soline.json()
        pload={"type":"redis","id":id,"count":0,"data":json.loads(solinestr)} 
        logging.info("(O) %s"%(solinestr,))
        r = redis.Redis(connection_pool=redispool)
        pstr = json.dumps(pload,ensure_ascii=False)
        r.rpush(config._redis["queue"], pstr)
        r.close()
        logging.info("(O) %s"%(pstr,))
        return {"status":INIT['O'],"detail":pload}
    except Exception as e:
        msg = show_error(e)
        logging.info("(X) %s error message:%s"%(id,msg))
        return {"status":INIT['X'],"detail": msg}

@app.post("/qso")
async def _qso(s:model.Shipment):
    id=str(uuid.uuid1())
    try:
        pload={"type":"redis","id":id,"count":0,"data":json.loads(s.json())} 
        r = redis.Redis(connection_pool=redispool)
        pstr = json.dumps(pload,ensure_ascii=False)
        logging.info("(O) %s"%(pstr,))
        r.rpush(config._redis["queue"], pstr)
        r.close()
        return {"status":INIT['O'],"detail":pload}
    except Exception as e:
        msg = show_error(e)
        logging.info("(X) %s error message:%s"%(id,msg))
        return {"status":INIT['X'],"detail": msg}

#--------------------------------------------------------------------------------------
def show_error(e):
        error_class   = e.__class__.__name__
        detail        = e.args[0]
        cl, exc, tb   = sys.exc_info()
        lastCallStack = traceback.extract_tb(tb)[-1]
        fileName = lastCallStack[0]
        lineNum  = lastCallStack[1]
        funcName = lastCallStack[2]
        errMsg   = ":File \"{}\", line {}, in {}: [{}] {}.".format(fileName, lineNum, funcName, error_class, detail)
        return errMsg
