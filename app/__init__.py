import asyncio


async def main():
    keys = ["one", "two", "three"]
    required_keys = ["one", "two"]

    print(set(keys) == set(required_keys))


if __name__ == '__main__':
    asyncio.run(main())