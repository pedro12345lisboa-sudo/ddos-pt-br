"""Uma conexao HTTP por vez para verificacoes controladas."""
from dataclasses import dataclass

import aiohttp

from src.utils.randomizer import user_agent


@dataclass(frozen=True)
class CheckResult:
    status: int | None
    elapsed_seconds: float
    error: str | None = None


async def check_once(session: aiohttp.ClientSession, url: str) -> CheckResult:
    import time

    started = time.perf_counter()
    try:
        async with session.get(url, headers={"User-Agent": user_agent()}) as response:
            await response.read()
            return CheckResult(response.status, time.perf_counter() - started)
    except (aiohttp.ClientError, TimeoutError) as error:
        return CheckResult(None, time.perf_counter() - started, str(error))
