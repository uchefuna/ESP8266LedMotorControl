

import machine as mhn  # type: ignore
import network as net  # type: ignore
from wifiAPConfig import *


# As Access Point
def getAPWifi(apV):
    apConfig = apLoadConfig()

    print(f"\nAP config: {apConfig}")

    if apConfig["Configuration"]["WiFiMode"] == "Access Point":
        wifiAP = net.WLAN(net.AP_IF)
        wifiAP.active(apV)

        if apV == 1:
            # wifiAP.config(essid='RoutTable', password='uGRA9500')
            wifiAP.config(
                essid=apConfig["Configuration"]["WiFiClientSSID"],
                authmode=net.AUTH_WPA_WPA2_PSK,
                password=apConfig["Configuration"]["WiFiAPPassword"],
            )
            wifiAP.config(channel=apConfig["Configuration"]["WiFiCHANNEL"])

            wifiAP.ifconfig(
                (
                    apConfig["Configuration"]["WiFiAPIP"],
                    apConfig["Configuration"]["WiFiAPMask"],
                    apConfig["Configuration"]["WiFiGATEWAY"],
                    apConfig["Configuration"]["WiFiNET"],
                )
            )

            print("\nAP SERVER: Access Point Configured")

        else:
            print("\nAP SERVER: Access Point not Configured")

        print(f"\nAP ifconfig: {wifiAP.ifconfig()}")

    # As Wi-Fi client
    elif apConfig["Configuration"]["WiFiMode"] == "Client":
        print(
            f"SERVER: Setup as client {apConfig['Configuration']['WiFiClientSSID']} with password {apConfig['Configuration']['WiFiClientPassword']}")
    else:
        mhn.reset()
