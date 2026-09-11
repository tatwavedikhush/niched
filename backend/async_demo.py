import asyncio


async def task(name, seconds):
    print(f"{name} started")
    await asyncio.sleep(seconds)
    print(f"{name} finished")


async def main():
    await asyncio.gather(task("Reddit", 3), task("Trends", 2), task("Gumroad", 4))


asyncio.run(main())
