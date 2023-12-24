import colorama
import datetime
import os
import pytz
import time

def __clear__() -> int:
    return os.system('clear || cls')

def __get_time__(timezone: pytz.BaseTzInfo) -> datetime.datetime:
    return datetime.datetime.now(timezone)

def __strf_time__(_time: datetime.datetime) -> str:
    return _time.strftime('%H:%M:%S')

SUCCESS_V1 = '{}*{}'.format(colorama.Fore.LIGHTBLUE_EX, colorama.Style.RESET_ALL)
SUCCESS_V2 = '{}*{}'.format(colorama.Fore.LIGHTGREEN_EX, colorama.Style.RESET_ALL)
FAILURE = '{}*{}'.format(colorama.Fore.RED, colorama.Style.RESET_ALL)
WARNING = '{}*{}'.format(colorama.Fore.YELLOW, colorama.Style.RESET_ALL)
UNKNOWN = '{}?{}'.format(colorama.Fore.YELLOW, colorama.Style.RESET_ALL)

class Console:
      def __unknown__(this, text: str, brighten: bool = False) -> None:
          print(('{} {}'.format(UNKNOWN, text) if brighten == False else '{}{} {}'.format(colorama.Style.BRIGHT, UNKNOWN, text)))

      def __warning__(this, text: str, brighten: bool = False) -> None:
          print(('{} {}'.format(WARNING, text) if brighten == False else '{}{} {}'.format(colorama.Style.BRIGHT, WARNING, text)))

      def __failure__(this, text: str, brighten: bool = False) -> None:
          print(('{} {}'.format(FAILURE, text) if brighten == False else '{}{} {}'.format(colorama.Style.BRIGHT, FAILURE, text)))

      def __success__(this, text: str, brighten: bool = False, v1: bool = True) -> None:
          print(('{} {}'.format(SUCCESS_V1, text) if brighten == False else '{}{} {}'.format(colorama.Style.BRIGHT, SUCCESS_V1, text)) if v1 == True else ('{} {}'.format(SUCCESS_V2, text) if brighten == False else '{}{} {}'.format(colorama.Style.BRIGHT, SUCCESS_V2, text))) 
