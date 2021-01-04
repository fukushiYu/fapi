#!/usr/bin/python3
import redis, time,sys
import json, signal
import mypg
import config

def myexit(a,b):
    # 處理一半的
    sys.exit('程序終止')

class mredis():
    def __init__(self,cfg=config._redis):
        self.cfg = cfg
        self.pool = redis.ConnectionPool(host=cfg["host"], port=cfg["port"], decode_responses=True)
    def loop(self):
        r = redis.Redis(connection_pool=self.pool)
        pg, dbopen, isql = mypg.pgo(config._pg), True, config._pg["sqlstrings"]["inscmd"]
        while True:  
            entry=r.blpop(self.cfg["queue"], self.cfg["timeout"])  # timeout=0 block永久 second
            timestring, result = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()), ""
            if entry is None:
                entry, dbopen ="", False
                del pg
            else:
                if not dbopen:
                    pg, dbopen = mypg.pgo(config._pg), True
                # entry(queue,json) : "Chisaki","{"type": "redis", "id": "c9d3b8c6-39d0-11eb-ab09-256cd4854ed0", "count": 0, "data": {"cmd": 123}}"
                eobj = json.loads(entry[1]) 
                # 應該根據json的內容,將資料移入Destination DB,此處先作假動作Insert 到 PG,retry的機制? re-push entry[1]
                ret = action()      # insert into destination DB or do some actions
                # 若成功
                pg.exe(isql,[eobj["id"], json.dumps(eobj['data'],ensure_ascii=False),"成功",eobj["count"]]) 
                # else:
                #     eobj["count"] +=1
                #     estr = json.dumps(eobj,ensure_ascii=False)
                #     if eobj["count"](重試次數) < self.cfg["retry"](max retry) ，重新 queue
                #         r.rpush(self.cfg["queue"],estr )
                #         logging.info("(R) %s"%(estr,))
                #         pg.exe(isql,[eobj["id"], json.dumps(eobj['data'],ensure_ascii=False),"重試",eobj["count"]]) 
                #     else:
                #         logging.info("(X) %s"%(estr,))
                #         pg.exe(isql,[eobj["id"], json.dumps(eobj['data'],ensure_ascii=False),"失敗",eobj["count"]]) 

            print(timestring, entry)
        r.close()
    def action(self,params=[]):
        return True


# main()

signal.signal(signal.SIGINT, myexit)
signal.signal(signal.SIGTERM, myexit)
print(config.ifs['TITLE'])

m = mredis()
m.loop()


