#include <cstdio>
#include <events/mbed_events.h>

#include <mbed.h>
#include "EventQueue.h"
#include "ble/BLE.h"
#include "ble/Gap.h"

#ifndef __ID_SERVICE_H__
#define __ID_SERVICE_H__

#include <string>


class IDService {
    typedef IDService Self;
public:
    const static uint16_t ID_SERVICE_UUID              = 0xB000;
    const static uint16_t ID_STATE_CHARACTERISTIC_UUID = 0xB001;

    IDService(BLE &_ble, char * ID_given, events::EventQueue &event_queue, bool enable=false):
        ble(_ble), 
        ID_State(ID_STATE_CHARACTERISTIC_UUID, ID_given, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_READ),
        ID(ID_given),
        _event_queue(event_queue)
        {
            GattCharacteristic *charTable[] = {&ID_State};
            GattService IDService(IDService::ID_SERVICE_UUID, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));
            ble.gattServer().addService(IDService);
    }

    void sendIDValue() {
        ble.gattServer().write(ID_State.getValueHandle(), (uint8_t *)ID, 9);
    }

private:
    BLE &ble;
    char * ID;
    ReadOnlyArrayGattCharacteristic<char,9> ID_State; //**use readonlyarray to read more than 4 bytes
    events::EventQueue &_event_queue;
};

#endif /* #ifndef __BLE_BUTTON_SERVICE_H__ */
