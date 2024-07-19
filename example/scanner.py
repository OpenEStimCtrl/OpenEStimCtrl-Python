import asyncio
from bleak import BleakScanner
from openestimctrl import YokoNexES01, DGLabEStim01

async def main():
    found = set()
    async with BleakScanner() as scanner:
        async for bd, ad in scanner.advertisement_data():
            if bd.address in found:
                continue
            if DGLabEStim01.meta_service_estim() in ad.service_uuids:
                print(f"Found DGLabEStim01 device: {bd.address}")
            elif YokoNexES01.meta_service() in ad.service_uuids:
                print(f"Found YokoNexES01 device: {bd.address}")
            found.add(bd.address)

asyncio.run(main())