from pydantic import BaseModel
from typing import List, Set, Tuple,Optional
#--------------------------------------------------------------------------------------
class SOLINE(BaseModel):
    itemid  : str
    qty : int
    unit_price : int =0
    sell_price : int =0
    cost : int =0
class SO(BaseModel):
    ticket : str ="so"
    ordid : int =0
    member_id : int =0
    rcvname : str =""
    phoone : str =""
    address: str =""
    deltail : List[SOLINE]

class TEST(BaseModel):
    id : str
    name : str
    mobile : str = "yyy"
    address : str = "xxx"

class Shipment(BaseModel):
    shpno : str
    type  : Tuple[str, str]				# dtype, ecid
    store : Optional[ Tuple[str, str, str, str ]]	# type, id, name, srv
    comm  : Optional[str]
    cmps  : Optional[int]
    ord   : Tuple[str, str, str, str ] 			# cid, name, tel, email
    rcv   : Tuple[str, str, str, str, str] 		# name, tel, post, addr, email
    sum   : int
    line  : List[ Tuple[str,str,int,int]	]	# orderid, item, qty, unitprice

if __name__ == '__main__':
    soline = SOLINE(itemid="123",qty=10)

    print(soline.json())