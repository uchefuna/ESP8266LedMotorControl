import gc
import json as jsn
import machine as mhn  # type: ignore


def apLoadConfig():

    apConfig = {}

    # Load and check the apConfig file
    print("\nLoading AP config json file...")

    try:
        with open("wifiAP.json", "r") as fd:
            apConfig = jsn.load(fd)

    except OSError:
        # failed to open file (maybe it didn't exist)
        apConfig = {}

        # apConfig is corrupted
        if (apConfig.get("Device", {}).get("Manufacture") != "ESP8266"
                or apConfig.get("Checksum") != "18caE"):

            print("BOOT: wifiAP.json is corrupted! Uploading from backup.")

            # Copy clean from backup
            with open('wifiAP-backup.json', 'r') as fd:
                configBackup = jsn.load(fd)

            with open('wifiAP.json', 'w') as fd:
                jsn.dump(configBackup, fd)

            print("BOOT: Uploading from backup completed! Rebooting system...")

            # Reboot OS
            mhn.reset()
        # apConfig is correct
        else:
            print("BOOT: wifiAP.json loading completed!")

    # Clean memory
    gc.collect()
    return apConfig
