#!/usr/bin/python3
import psycopg2
import json
from datetime import datetime

def myconverter(o):
    if isinstance(o, datetime):
        return datetime.strftime(o,"%Y-%m-%d %H:%M:%S")

class pgo:
    conn = None
    status = None
    def __init__(self,c):
        try:
            self.conn = psycopg2.connect(database=c['dbs'], user=c['usr'], password=c['pwd'], host=c['hst'], port=c['port'])
            self.status = "正確"
        except:
            self.status = "無法連接PG DB"
    def exe(self, sql, params):
        try:
            cursor = self.conn.cursor()
            # %s, %s...
            cursor.execute(sql,params)
            self.conn.commit()
            self.status = "正確"
        except:
            self.status = "執行錯誤"
        cursor.close()
        return self.status
    def query(self, sql , params=[]):
        try:
            cur = self.conn.cursor()
            cur.execute(sql,params)
            self.rowcount = cur.rowcount
            cols=[c.name for c in cur.description]
            res=[]
            for row in cur:
                res.append(dict(zip(cols,row)))
            self.status = "正確"
            cur.close()
            return res
        except:
            self.status = "查詢錯誤"
            cur.close()
            return None
    def __del__(self):
        self.conn.close()


if __name__=='__main__':
    import config
    pg = pgo(config._pg)
    r = pg.query(config._pg["sqlstrings"]["sel"],["2020-01-01 00:00:00"])
    print(pg.rowcount)
    print(json.dumps(r,ensure_ascii=False,indent=1,default=myconverter))
