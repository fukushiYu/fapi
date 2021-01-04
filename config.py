oradb = {
    "connectstring" : "nrk/geefddcdefggg@w",
    "sqlstrings": {
	"stock_qty":"select customer_id,prod_id,prod_name,qty from stock where prod_id = :prod_id and freeze='N'",
	"15035_qty":"select prod_id,prod_name,qty from stock where prod_id = :prod_id and customer_id='15035' and freeze='N'",
	"code_detail":"select * from code_detail",
    }
}

ifs={"IN":"qin0",
    "OUT":"qout",
    "ERR":"qerr",
    "TITLE":r'''
  ______    __    __   __      ________     __       __   ___   __&    ___      ___   _______  
 /" _  "\  /" |  | "\ |" \    /"       )   /""\     |/"| /  ") |" \   |"  \    /"  | /"     "| 
(: ( \___)(:  (__)  :)||  |  (:   \___/   /    \    (: |/   /  ||  |   \   \  //   |(: ______) 
 \/ \      \/      \/ |:  |   \___  \    /' /\  \   |    __/   |:  |   /\\  \/.    | \/    |   
 //  \ _   //  __  \\ |.  |    __/  \\  //  __'  \  (// _  \   |.  |  |: \.        | // ___)_  
(:   _) \ (:  (  )  :)/\  |\  /" \   :)/   /  \\  \ |: | \  \  /\  |\ |.  \    /:  |(:      "| 
 \_______) \__|  |__/(__\_|_)(_______/(___/    \___)(__|  \__)(__\_|_)|___|\__/|___| \_______) 
''',
}


_redis = {
    "host":"localhost",
    "port":6379,
    "queue":"Chisaki",
    "timeout":60,
    "retry":10
}

_pg = {"dbs":"nrk",
    "usr":"nrk",
    "pwd":"geefddcdefggg",
    "hst":"127.0.0.1",
    "port":"5432" ,
    "sqlstrings":{
        "inscmd":"INSERT INTO public.cmdinfo(id,content,status,cnt,create_time,update_time) values (%s,%s,%s,%s,current_timestamp,current_timestamp)",
        "sel":"Select * from public.cmdinfo where create_time> %s",
        "cmdcnt":"Select status, count(*) cnt From cmdinfo Where create_time >=%s Group by status",
    }
}
