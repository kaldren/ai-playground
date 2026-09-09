"""A minimal asyncio example."""

import asyncio


async def main() -> None:
    await asyncio.sleep(0.1)
    print("Hello from asyncio")


if __name__ == "__main__":
    asyncio.run(main())
