#!/bin/bash
cd /opt/fapi/0/script
python3 stock_qty.py > sync.log 2>&1
at now + 24 hours -f /opt/fapi/0/script/sync.sh



