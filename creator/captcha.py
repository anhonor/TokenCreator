import requests
import time

DISCORD_EMAIL_SITE_KEY = 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34'
DISCORD_SITE_KEY = '4c672d35-0701-42b2-88c3-78380b0db560'
DISCORD_SITE_URL = 'https://discord.com'

class Capsolver: 
      def __init__(this, key: str) -> None:
          this.key = key
          this.session = requests.Session()

      def __base_payload__(this, extra: dict = {}) -> dict:
          return {
             'clientKey': this.key,
            **extra
          }

      def __get_balance__(this) -> int | None:
          return requests.get('https://api.capsolver.com/getBalance', headers = {'Host': 'api.capsolver.com', 'Content-Type': 'application/json'}, json = this.__base_payload__()).json().get('balance')

      def __create_task__(this, site_key: str = DISCORD_SITE_KEY, site_url: str = DISCORD_SITE_URL, proxy: str | None = None, rq_data: str | None = None) -> int | bool:
          return requests.post('https://api.capsolver.com/createTask', headers = {'Host': 'api.capsolver.com', 'Content-Type': 'application/json'}, json = this.__base_payload__({
             'task': {
                'websiteURL': site_url,
                'websiteKey': site_key,
                'type': 'HCaptchaTask' if proxy else 'HCaptchaTaskProxyless',
                **({'enterprisePayload': {'rqdata': rq_data}} if rq_data else {}),
                **({
                    'proxyType': 'http',
                    'proxyLogin': proxy.split(':')[0], 
                    'proxyPassword': proxy.split(':')[1].split('@')[0], 
                    'proxyAddress': proxy.split('@')[1].split(':')[0],
                    'proxyPort': int(proxy.split('@')[1].split(':')[1])
                } if proxy else {})
             }
          })).json().get('taskId')

      def __get_task_result__(this, task_id: int) -> tuple | None:
          counter = time.perf_counter()
          for attempt in range(120):
              request = requests.post('https://api.capsolver.com/getTaskResult', json = this.__base_payload__({'taskId': task_id}))
              if request.json().get('solution'):
                 return request.json()['solution']['gRecaptchaResponse'], round(time.perf_counter() - counter, 2)
              time.sleep(1)

class Capmonster: 
      def __init__(this, key: str) -> None:
          this.key = key
          this.session = requests.Session()

      def __base_payload__(this, extra: dict = {}) -> dict:
          return {
             'clientKey': this.key,
            **extra
          }

      def __get_balance__(this) -> int | None:
          return requests.get('https://api.capmonster.cloud/getBalance', json = this.__base_payload__()).json().get('balance')

      def __create_task__(this, site_key: str = DISCORD_SITE_KEY, site_url: str = DISCORD_SITE_URL, proxy: str | None = None, rq_data: str | None = None) -> int | bool:
          return requests.post('https://api.capmonster.cloud/createTask', json = this.__base_payload__({
             'task': {
                'websiteURL': site_url,
                'websiteKey': site_key,
                'type': 'HCaptchaTask' if proxy else 'HCaptchaTaskProxyless',
              **({'enterprisePayload': {'rqdata': rq_data}} if rq_data else {}),
              **({
                    'proxyType': 'http',
                    'proxyLogin': proxy.split(':')[0], 
                    'proxyPassword': proxy.split(':')[1].split('@')[0], 
                    'proxyAddress': proxy.split('@')[1].split(':')[0],
                    'proxyPort': int(proxy.split('@')[1].split(':')[1])
              } if proxy else {})
             }
          })).json().get('taskId')

      def __get_task_result__(this, task_id: int) -> tuple | None:
          counter = time.perf_counter()
          for attempt in range(120):
              request = requests.post('https://api.capmonster.cloud/getTaskResult', json = this.__base_payload__({'taskId': task_id}))
              if request.json().get('solution'):
                 return request.json()['solution']['gRecaptchaResponse'], round(time.perf_counter() - counter, 2)
              time.sleep(1)
