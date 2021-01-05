
monitor rest request and push in to redis queue

$ ln -s fapi_0.service /etc/systemd/system/fapi_0.service

$ service fapi_0 start


python3 moni_redis.py
monitor redis queue and load request to do something

