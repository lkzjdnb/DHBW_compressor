from snap7.server import Server
from ctypes import (
    c_char,
    byref,
    sizeof,
    c_int,
    c_int32,
    c_uint32,
    c_void_p,
    CFUNCTYPE,
    POINTER,
    Array,
    _SimpleCData,
)
from _ctypes import CFuncPtr
from snap7.types import longword, wordlen_to_ctypes, WordLen, S7Object
from snap7.types import srvAreaDB, srvAreaPA, srvAreaTM, srvAreaCT

import logging

logger = logging.getLogger(__name__)

import time

def mainloop(tcpport: int = 1102, init_standard_values: bool = False) -> None:
    """Init a fake Snap7 server with some default values.

    Args:
        tcpport: port that the server will listen.
        init_standard_values: if `True` will init some defaults values to be read on DB0.
    """

    server = Server()
    size = 10000
    DBdata: "Array[_SimpleCData[int]]" = (wordlen_to_ctypes[WordLen.Byte.value] * size)()
    PAdata: "Array[_SimpleCData[int]]" = (wordlen_to_ctypes[WordLen.Byte.value] * size)()
    TMdata: "Array[_SimpleCData[int]]" = (wordlen_to_ctypes[WordLen.Byte.value] * size)()
    CTdata: "Array[_SimpleCData[int]]" = (wordlen_to_ctypes[WordLen.Byte.value] * size)()
    # server.register_area(srvAreaDB, 0, DBdata)
    for i in range(512):
        server.register_area(srvAreaDB, i, DBdata)
    server.register_area(srvAreaPA, 1, PAdata)
    server.register_area(srvAreaTM, 1, TMdata)
    server.register_area(srvAreaCT, 1, CTdata)

    if init_standard_values:
        ba = _init_standard_values()
        userdata = wordlen_to_ctypes[WordLen.Byte.value] * len(ba)
        server.register_area(srvAreaDB, 0, userdata.from_buffer(ba))

    server.start(tcpport=tcpport)
    while True:
        while True:
            event = server.pick_event()
            if event:
                print(server.event_text(event))
                logger.info(server.event_text(event))
            else:
                break
        time.sleep(1)

mainloop()
