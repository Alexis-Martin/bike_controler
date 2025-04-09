import ubluetooth
import struct
from micropython import const
import os 


_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)

    
FLASHER_UUID = ubluetooth.UUID("b761234b-a9bf-4bb2-bcd4-fe4de0a8711d")
FLASHER_WRITE = (ubluetooth.UUID("b761234c-a9bf-4bb2-bcd4-fe4de0a8711d"), ubluetooth.FLAG_WRITE,)
FLASHER_SERVICE = (FLASHER_UUID, (FLASHER_WRITE,),)

# Generate a payload to be passed to gap_advertise(adv_data=...).
def advertising_payload(limited_disc=False, br_edr=False, name=None, services=None, appearance=0):
    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack('BB', len(value) + 1, adv_type) + value

    _append(_ADV_TYPE_FLAGS, struct.pack('B', (0x01 if limited_disc else 0x02) + (0x00 if br_edr else 0x04)))

    if name:
        _append(_ADV_TYPE_NAME, name)

    if services:
        for uuid in services:
            b = bytes(uuid)
            if len(b) == 2:
                _append(_ADV_TYPE_UUID16_COMPLETE, b)
            elif len(b) == 4:
                _append(_ADV_TYPE_UUID32_COMPLETE, b)
            elif len(b) == 16:
                _append(_ADV_TYPE_UUID128_COMPLETE, b)

    # See org.bluetooth.characteristic.gap.appearance.xml
    _append(_ADV_TYPE_APPEARANCE, struct.pack('<h', appearance))

    return payload


class BLE:
    def __init__(self):
        self.interval_us=160
        self.name = 'Bike_Ctrler'
        self.services = (FLASHER_SERVICE,)

        self._connections = set()
        self.file_buffer = {}
        self.directory = 'test'
        if self.directory not in os.listdir():
            os.mkdir(self.directory)
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.irq)
        self.register()
        self.payload = advertising_payload(name=self.name)
        self.advertise()

    def irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _, = data
            self._connections.add(conn_handle)
            self.ble.gattc_exchange_mtu(conn_handle)
            print("Device connected")
            
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _, = data
            self._connections.remove(conn_handle)
            print("Device disconnected")

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, attr_handle = data

            value = self.ble.gatts_read(attr_handle)
            print(value)
            print(len(value))
            self.handle_write(value)

    def register(self):  
        ( (self.hr,)) = self.ble.gatts_register_services(self.services)
        self.ble.gatts_set_buffer(self.hr[0], 256)
      
    def advertise(self):
        self.ble.gap_advertise(self.interval_us, adv_data=self.payload)
        print("BLE start")

    def handle_write(self, value):
        # Supposons que `value` contient le nom du fichier et les données
        if b'\x00' in value:
            self.filename, filedata = value.split(b'\x00', 1)
            self.filename = self.filename.decode('utf-8')
        else:
            filedata = value
        # Ajouter les données au buffer
        if self.filename in self.file_buffer:
            self.file_buffer[self.filename] += filedata
        else:
            self.file_buffer[self.filename] = filedata

        # Si le fichier est complet, écrire sur le système de fichiers
        if b'\x03' in filedata:  # Supposons que '\x03' indique la fin du fichier
            self.write_file(self.filename)
            self.file_buffer.pop(self.filename)
            self.filename = None

    def write_file(self, filename):
        filepath = f"{self.directory}/{filename}"
        with open(filepath, 'wb') as f:
            f.write(self.file_buffer[filename].replace(b'\x03', b''))
        print(f"File {filename} received and saved in {self.directory}.")
        with open(filepath, 'r') as f:
            print(f.read())

    def restart(self):
        import machine
        machine.reset()