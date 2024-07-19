import asyncio
from bleak import BleakClient
from openestimctrl import YokoNexES01
import threading

address = "24:8B:B5:1E:FE:E4"

async def main(address):
    async with BleakClient(address) as client:
        def send_ble_data(service, characteristic, data):
            thread = threading.Thread(target=asyncio.run, args=(client.write_gatt_char(characteristic, bytearray(data), response=False),))
            thread.start()
            thread.join()
            
        protocol = YokoNexES01('libOpenEstimCtrl.dll', send_ble_data)
        def notification_handler(characteristic, data: bytearray):
            protocol.parse_ble_data(data)
        await client.start_notify(YokoNexES01.meta_service_characteristic_rx(), notification_handler)
        ###
        def angle_handler(accX, accY, accZ, gyroX, gyroY, gyroZ):
            print('Angle:', accX, accY, accZ, gyroX, gyroY, gyroZ)
        protocol.set_on_battery_status_change(lambda battery: print('Battery:', battery))
        protocol.set_on_motor_status_change(lambda motor: print('Motor:', motor))
        protocol.set_on_angle_status_change(angle_handler)
        protocol.set_on_exception(lambda exception: print('Exception:', exception))
        protocol.query(YokoNexES01.Query.BATTERY)
        await asyncio.sleep(3) # YokoNexES01 役次元设备在连接后需要等待一段时间才能完成初始化，否则会报 Exception 4
        protocol.trigger_motor(YokoNexES01.Motor.INTERNAL_1)
        await asyncio.sleep(0.1)
        protocol.query(YokoNexES01.Query.MOTOR)
        await asyncio.sleep(3)
        protocol.trigger_motor(YokoNexES01.Motor.OFF)
        await asyncio.sleep(0.1)
        protocol.query(YokoNexES01.Query.MOTOR)
        await asyncio.sleep(0.5)
        protocol.set_angle(YokoNexES01.Angle.ON)
        await asyncio.sleep(10)
        protocol.set_angle(YokoNexES01.Angle.OFF)
        await asyncio.sleep(0.5)
        

asyncio.run(main(address))