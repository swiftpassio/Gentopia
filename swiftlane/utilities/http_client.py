from typing import Union

import aiohttp


_session = None


async def initialize_session() -> aiohttp.ClientSession:
    global _session
    _session = aiohttp.ClientSession()
    return _session


async def close_session() -> None:
    await _session.close()


def session() -> Union[aiohttp.ClientSession, None]:
    return _session
