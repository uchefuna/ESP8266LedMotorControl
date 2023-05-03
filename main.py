import gc
import uasyncio as asy # type: ignore
from time import sleep as slp
from wifiSTAConfig import startSystem
from wifiAPConn import *
from wifiSTAConn import *
from program import *

slp(0.1) # type: ignore


def startUP():
    startSystem()
    slp(0.5)
    getSTAWifi()

    staWifi = str(staWifiConnect)
    if staWifi == "on wifi sta conn":
        getAPWifi(1)
    else:
        getAPWifi(0)
        print("\nAt least one WiFi is present\n")
    return


startUP()
slp(0.1)

def eventMain():
    event_loop = asy.get_event_loop()
    event_loop.create_task(serverLoop())
    event_loop.create_task(testLoop())
    event_loop.run_forever()


async def main():
    tasks = [serverLoop(), testLoop()]
    await asy.sleep(1)
    await asy.gather(*tasks)


try:
    # asy.run(main())
    eventMain()
except KeyboardInterrupt:
    print("System interrupted by key input")
except OSError as err:
    print(f"error due to: {err}")
else:
    print("No exception occurred")
finally:
    print("Closing Loop")
    print(f"gabbage collected: {gc.collect()}")
