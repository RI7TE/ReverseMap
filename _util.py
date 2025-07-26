import datetime as dt
import os
import sys

from contextlib import contextmanager, redirect_stdout
from pathlib import Path

import ujson as json

from colorama import Fore, Style


sys.path.append(str(Path(__file__).absolute().parent))

from shlex import quote,split


def show(
    *msg,
    color: str = Fore.BLUE,
    log=False,
    debug=False,
    log_file: str | Path = 'debug.log',
    term=True,
) -> str:
    """
    Print a message in the specified color.
    """
    if color == "red":
        color = Fore.RED
    elif color == "green":
        color = Fore.GREEN
    elif color == "yellow":
        color = Fore.YELLOW
    elif color == "blue":
        color = Fore.BLUE
    to_debug = os.getenv('DEBUG', '0') == '1' or debug
    to_log = os.getenv('LOG', '0') == '1' or log
    if len(msg) == 1 and isinstance(msg[0], (list, tuple)):
        msg =  msg[0]
    elif len(msg) == 1 and isinstance(msg[0], dict):
        msg = [f"{k}: {v}".strip() for k, v in msg[0].items()]
    _msg = quote(' '.join(map(str, msg)))
    log_msg = (
        dt.datetime.now(dt.UTC).strftime("%d/%m/%Y, %H:%M:%S") + "\n" + "\t" + _msg
    )
    msg = color + f"{' '.join(map(str, msg))}" + Style.RESET_ALL

    @contextmanager
    def _log():  # Log to a file if LOG environment variable is set
        nonlocal log_file
        log_file = os.getenv('LOG_FILE', str(log_file))
        with Path(log_file).open('a') as f:
            if term:
                f.write(log_msg + '\n')
            yield f
        if sys.stdout.isatty():
            print(Fore.BLACK + f"Logged to {log_file}" + Style.RESET_ALL, flush=True)
        else:
            print(
                Fore.YELLOW + f"Warning: Logged to {log_file}" + Style.RESET_ALL,
                file=sys.stderr,
                flush=True,
            )

    if to_debug:
        if to_log:
            with _log() as f:
                print(
                    log_msg if not term else msg,
                    file=f if not term else sys.stderr,
                    flush=True,
                )
        else:
            print(msg, flush=True)
    elif to_log:
        with _log() as f:
            print(
                log_msg if not term else msg,
                file=f if not term else sys.stderr,
                flush=True,
            )
    elif sys.stdout.isatty():
        # Print to stdout if it is a terminal
        print(msg, flush=True)
        sys.stdout.flush()
    else:
        # Fallback to stderr if stdout is not a terminal
        print(
            Fore.YELLOW + "Warning: Not printing to stdout" + Style.RESET_ALL,
            file=sys.stderr,
            flush=True,
        )
        sys.stderr.write(msg + '\n')
        sys.stderr.flush()

    return _msg.strip()
