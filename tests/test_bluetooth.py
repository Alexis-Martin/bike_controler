import asyncio
from bleak import BleakScanner, BleakClient

# UUID du service et de la caractéristique sur l'ESP32
SERVICE_UUID = "b761234b-a9bf-4bb2-bcd4-fe4de0a8711d"
CHAR_UUID = "b761234c-a9bf-4bb2-bcd4-fe4de0a8711d"

MAX_CHUNK_SIZE = 256

async def scan_and_select_device():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()

    if not devices:
        print("No BLE devices found.")
        return None

    print("Available BLE devices:")
    for i, device in enumerate(devices):
        print(f"{i + 1}: {device.name} ({device.address})")

    choice = int(input("Enter the number of the device you want to connect to: ")) - 1

    if choice < 0 or choice >= len(devices):
        print("Invalid choice.")
        return None

    return devices[choice].address

async def connect_and_send_data(address, filename, text):
    async with BleakClient(address) as client:
        print(f"Connected to {address}")

        # Convertir le texte en bytes
        data_to_send = text.encode('utf-8')

        # Envoyer le nom du fichier
        await client.write_gatt_char(CHAR_UUID, filename.encode('utf-8') + b'\x00')

        # Diviser les données en morceaux et les envoyer
        for i in range(0, len(data_to_send), MAX_CHUNK_SIZE):
            chunk = data_to_send[i:i+MAX_CHUNK_SIZE]
            await client.write_gatt_char(CHAR_UUID, chunk)

        # Indiquer la fin du fichier
        await client.write_gatt_char(CHAR_UUID, b'\x03')
        print("Data sent successfully.")

async def main():
    #address = await scan_and_select_device()
    filename = "../button_utils.py"
    address = "A9858CB4-0A11-B227-80E3-1DE2CC5BC43B"
    if address:
        with open(filename, 'r') as f:
            text = f.read()
        await connect_and_send_data(address, filename, text)

# Exécuter le script
asyncio.run(main())
