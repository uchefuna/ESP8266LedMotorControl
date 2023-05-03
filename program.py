# .......................................................

import uasyncio as asy  # type: ignore

from ws_run import *
from bd_access import *

# .......................................................


# Main Loop
# .......................................................


async def serverLoop():
    # define Wifi port number
    PRTNUM = const(5000)  # type: ignore

    # server start
    server = TestServer('websock.html')
    server.start(PRTNUM)  # set port number 5000
    print("\nWaiting for client connection...\n")

    # loop process
    try:
        while True:
            server.process_all()
            await asy.sleep_ms(1)
    except KeyboardInterrupt:
        server.stop()


async def testLoop():
    while True:
        await asy.sleep(5)
        print("Continuing 1")
        await asy.sleep(5)
        print("Continuing 2")

# .......................................................
