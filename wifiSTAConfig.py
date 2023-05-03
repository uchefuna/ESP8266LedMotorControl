

import json as jsn

# trying to read config --------------------------------------------------------


def staLoadConfig():

    # Load and check the ap_config file
    print("\nLoading STA config json file...")
    global staConfig
    try:
        with open("wifiSTA.json", "r") as fd:
            staConfig = jsn.load(fd)
    except OSError as err:
        print(f'error due to: {err}')
    finally:
        print(f"\nSTA config: {staConfig}")

    return staConfig
# -------------------------------------------------------


# Starting the system
# --------------------------------------------------------
# Prog to start the system
def startSystem():
    print("\nStarting System")

# --------------------------------------------------------
