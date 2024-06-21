import snap7
from snap7.util.getters import get_real, get_bool
import json

regs = {}

with open("S7_registers.json") as f:
    regs = json.load(f)

client = snap7.client.Client()
client.connect("127.0.0.1", 0, 0, 1102)

def read_reg(r):
    if(r["id"].startswith("M")):
        # TODO
        return 0
    db = r["id"].split(".")[0]
    db = int(db[2:])

    print(r["id"])

    if r["type"] == "FLOAT":
        dbd = int(r["id"].split(".")[1][3:])
        val = client.db_read(db, dbd, 4)
        return get_real(val, 0)
    if r["type"] == "BOOL":
        dbx, dbxi = r["id"].split(".")[1:3]
        dbx = int(dbx[3:])
        dbxi = int(dbxi)
        print(f"{db} {dbx} {r['id']}")
        val = client.db_read(db, dbx, 1)
        return get_bool(val, 0, dbxi)

while True:
    res = {r["name"]: read_reg(r) for r in regs}
    print(res)
data = client.db_read(1, 0, 4)
print(data)
client.db_write(1, 0, data)
