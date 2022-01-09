from setup_net import SSID, PASS
from network import WLAN, STA_IF

if __name__ == "__main__":
    sta_if = WLAN(STA_IF)

    if not sta_if.isconnected():
        print("Connecting to network")
        sta_if.active(True)
        sta_if.connect(SSID, PASS)
        
        while not sta_if.isconnected():
            pass

    print("Connected to network:", sta_if.ifconfig())       
