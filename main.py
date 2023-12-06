import asyncio

from claimer import Claimer


async def main():
    await Claimer.menu()


if __name__ == "__main__":
    asyncio.run(main=main())
