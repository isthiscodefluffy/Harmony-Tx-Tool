from typing import List, Type, Callable
import logging
import os
from requests.exceptions import (
    HTTPError,
    ConnectionError as HTTPConnectionError,
    JSONDecodeError,
)
from tenacity import (
    retry,
    retry_any as RetryChain,  # noqa
    stop_after_attempt,
    retry_if_exception_type as r,
    wait_exponential,
    wait_random,
)

T_EXCEPTION = Type[BaseException]

COMMON_API_EXCEPTIONS: List[T_EXCEPTION] = [
    HTTPError,
    HTTPConnectionError,
    JSONDecodeError,
]

MAIN_LOGGER = logging.getLogger("main")


def make_yellow(log_output: str) -> str:
    return "\x1b[33;20m" + log_output


def retry_on_exceptions(
    exceptions: List[T_EXCEPTION],
    max_tries: int = 7,
    jitter_range_sec: int = 2,
    max_wait_sec: int = 120,
) -> Callable:
    return retry(
        retry=_build_exceptions(exceptions),
        reraise=True,
        wait=(
            wait_exponential(multiplier=1, min=5, max=max_wait_sec)
            + wait_random(0, jitter_range_sec)
        ),
        stop=stop_after_attempt(max_tries),
    )


def _build_exceptions(exceptions: List[T_EXCEPTION], i: int = 0) -> RetryChain:
    return r(exceptions[i]) | (
        i + 1 == len(exceptions) - 1
        and r(exceptions[i + 1])
        or _build_exceptions(exceptions, i + 1)
    )


def api_retry(custom_exceptions: List[T_EXCEPTION]) -> Callable:
    return retry_on_exceptions(COMMON_API_EXCEPTIONS + custom_exceptions)


def get_local_abi(abi_json_filename: str) -> str:
    """
    Copyright 2021 Paul Willworth <ioscode@gmail.com>
    """
    location = os.path.abspath(__file__)
    path = "{0}/abi/{1}.json".format(
        "/".join(location.split("/")[0:-1]), abi_json_filename
    )

    with open(path, "r", encoding="UTF-8") as f:
        abi = f.read()

    return abi
