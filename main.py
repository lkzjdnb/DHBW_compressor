from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import re
import snap7
from snap7.util.getters import get_real, get_bool
import json

url = "http://141.72.13.23:9091"

regs = {}

with open("S7_registers.json") as f:
    regs = json.load(f)

client = snap7.client.Client()
client.connect("192.168.1.16", 0, 0, 102)

def read_reg(r):

    if(r["id"].startswith("M")):
        # TODO
        return 0
    db = r["id"].split(".")[0]
    db = int(db[2:])

   # print(r["id"])

    if r["type"] == "FLOAT":
        dbd = int(r["id"].split(".")[1][3:])
        val = client.db_read(db, dbd, 4)
        return get_real(val, 0)
    if r["type"] == "BOOL":
        dbx, dbxi = r["id"].split(".")[1:3]
        dbx = int(dbx[3:])
        dbxi = int(dbxi)
       # print(f"{db} {dbx} {r['id']}")
        val = client.db_read(db, dbx, 1)
        return get_bool(val, 0, dbxi)
    
while True:
    registry = CollectorRegistry()
    res = {r["name"]: read_reg(r) for r in regs}
    for i in res:
        g = Gauge(re.sub(r'[\W_]+','_',i), i, registry=registry)
        if(res[i]==None):
            g.set(-1)
        else :
            g.set(res[i])
    push_to_gateway(url, job='compressor', registry=registry)

    