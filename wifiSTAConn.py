

import network as net  # type: ignore
from wifiSTAConfig import staLoadConfig
from time import sleep as slp


def staWifiConnect(SSID: str, pwd: str, attempts: int, delay_in_msec: int) -> net.WLAN:
    wifi = net.WLAN(net.STA_IF)

    if wifi.isconnected():
        print(f"\nConnected to {SSID} at start.")
        print(f"STA ifconfig: {wifi.ifconfig()}\n")

        return "wifi sta conn"
    else:
        print("\nWifi not configured. Trying to configure...")

    wifi.active(0)
    print("\nDisconnect STA Wifi.")
    wifi.active(1)
    print("\nReconnect STA Wifi.\n")

    count = 0

    while not wifi.isconnected() and count <= attempts:
        print(f"WiFi connecting to {SSID}. Attempt: {count}.")
        if wifi.status() != net.STAT_CONNECTING:
            wifi.connect(SSID, pwd)
        slp(delay_in_msec)
        count += 1

    if wifi.isconnected():
        print(f"\nConnected to {SSID}")
        print(f"STA ifconfig: {wifi.ifconfig()}\n")

        return "wifi sta conn"
    else:
        print("\nWifi not connected.\n")
        return "no wifi sta conn"

    # return wifi


def getSTAWifi():
    staConfig = staLoadConfig()
    print(staWifiConnect(staConfig["wifi"]["SSID"],
                         staConfig["wifi"]["password"], staConfig["wifi"]["attempts"],
                         staConfig["wifi"]["delay_in_msec"]))
