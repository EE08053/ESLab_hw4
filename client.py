from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
import binascii
import time

BUTTON_SERVICE_UUID = 0xA000
BUTTON_STATE_CHARACTERISTIC_UUID = 0xA001
ID_SERVICE_UUID = 0xB000
ID_CHARACTERISTIC_UUID = 0xB001
LED_SERVICE_UUID = 0xC000
LED_CHARACTERISTIC_UUID = 0xC001

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device",dev.addr)
        elif isNewData:
            print("Received new data from",dev.addr)

class NotifyDelegate(DefaultDelegate):
    def __init__(self, hndl):
        print("New delegate init")
        DefaultDelegate.__init__(self)
        self.hndl = hndl
    def handleNotification(self, cHandle, data):
        print(data)
        print("Handling Notification")

def enable_notify(ch):
    setup_data = b"\x01\x00"
    cccd = ch.getHandle() + 1
    res = dev.writeCharacteristic(cccd, setup_data, withResponse=True)
    print(res)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(30.0)

print("Connecting...")

n = 0
number = 0
for dev in devices:
    print("%d:Device %s(%s), RSSI=%d dB" % (n,dev.addr,dev.addrType,dev.rssi))
    for(adtype, desc, value) in dev.getScanData():
        print(" %s = %s"%(desc,value))
    n+=1

MAC_ADDR = "d8:ad:d4:80:b9:e4" # our STM32 address
dev = Peripheral(MAC_ADDR,'random')

print("Services...")
for svc in dev.services:
    print(str(svc))

try:
    # connect the three services
    ButtonService = dev.getServiceByUUID(UUID(BUTTON_SERVICE_UUID))
    Button_State_Ch = ButtonService.getCharacteristics(UUID(BUTTON_STATE_CHARACTERISTIC_UUID))[0]
    print(Button_State_Ch)

    IdService = dev.getServiceByUUID(UUID(ID_SERVICE_UUID))
    ID_State_Ch = IdService.getCharacteristics(UUID(ID_CHARACTERISTIC_UUID))[0]
    print(ID_State_Ch)

    LedService = dev.getServiceByUUID(UUID(LED_SERVICE_UUID))
    Led_Control_Ch = LedService.getCharacteristics(UUID(LED_CHARACTERISTIC_UUID))[0]
    print(Led_Control_Ch)

    # Read: Student ID 
    if ID_State_Ch.supportsRead():
        id = ID_State_Ch.read().decode('utf-8')
        print("Student ID : " + id)

    # Notify: Button State
    dev.withDelegate(NotifyDelegate(Button_State_Ch.getHandle()))
    enable_notify(Button_State_Ch)

    while True:
        if dev.waitForNotifications(1.0):
            print("Notification received")
            b = Button_State_Ch.read()
            print(type(b))
            print("button state:" + b.decode('utf-8'))
            break

    # Write: Control LED 
    if "WRITE" in Led_Control_Ch.propertiesToString():
        flag = False
        for i in range(6):
            if flag:
                res = Led_Control_Ch.write(b"\x01", withResponse=True)
            else:
                res = Led_Control_Ch.write(b"\x00", withResponse=True)
            print(i+1, res)
            flag = not flag
            time.sleep(1.0)
        
finally:
    dev.disconnect()
