#include <cstdint>
#include <events/mbed_events.h>

#include <mbed.h>
#include "DigitalOut.h"
#include "ble/BLE.h"
#include "ble/Gap.h"

#ifndef __LED_SERVICE_H__
#define __LED_SERVICE_H__

class LEDService {
public:
    const static uint16_t LED_SERVICE_UUID              = 0xC000;
    const static uint16_t LED_STATE_CHARACTERISTIC_UUID = 0xC001;

    LEDService(BLE &_ble, DigitalOut &ledGiven) : 
        ble(_ble),
        led(ledGiven),
        ledState(LED_STATE_CHARACTERISTIC_UUID, &led, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_WRITE)
    {
        GattCharacteristic *charTable[] = {&ledState}; // button state : GattCharacteristic
        GattService         ledService(LEDService::LED_SERVICE_UUID, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));
        ble.gattServer().addService(ledService);
    }

    void updateLEDState() {
        uint8_t value[]={}; //initialize a buffer to store the value sent by client to control led1
        uint16_t size = 1;
        ble.gattServer().read(ledState.getValueHandle(), value, &size);
        led = *value;        
    }
    
private:
    BLE                              &ble;
    WriteOnlyGattCharacteristic<DigitalOut> ledState;
    DigitalOut led;
};

#endif /* #ifndef __BLE_BUTTON_SERVICE_H__ */