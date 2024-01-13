import base64
import hashlib
import json
import random
import tls_client
import ua_generator
import websocket
from creator.modules.properties import Properties

config = json.load(open('./data/config.json', 'r'))
proxies = list(proxy.strip() for proxy in open('./data/proxies.txt', 'r').readlines())

def __get_proxy__() -> str | None:
    if len(proxies):
       return random.choice(proxies)
    
def __get_client_identifier__() -> str:
    return random.choice([
       'chrome_103',
       'chrome_104',
       'chrome_105',
       'chrome_106',
       'chrome_107',
       'chrome_108',
       'chrome_109',
       'chrome_111',
       'chrome_112',
       'chrome_117'
    ])

def __get_client__(random_tls_extension_order: bool = True) -> tls_client.Session:
    return tls_client.Session(random_tls_extension_order = random_tls_extension_order, client_identifier = __get_client_identifier__())

def __get_websocket_client__() -> websocket.WebSocket:
    return websocket.WebSocket()

class Client:
      def __init__(this, proxy: str | None = None) -> None:
          this.agent = ua_generator.generate(device = ('desktop'), browser = ('chrome'))
          this.proxy = ({
              'http' : 'http://{}'.format(proxy),
              'https': 'http://{}'.format(proxy)} if proxy != None else None)
          this.websocket_client = __get_websocket_client__()
          this.client = __get_client__()
          if this.proxy:
             this.client.proxies.update(this.proxy)
          this.properties = Properties(this.agent)
          this.super_properties = this.properties.__get_super_properties__()
          this.cookies = this.getCookies()
          this.experiments = this.getExperiments()

      def __construct_cookies__(this, cookies: tls_client.cookies.RequestsCookieJar) -> str:
          return ' '.join('{}={};'.format(cookie.name, cookie.value) for cookie in cookies)

      def __construct_headers__(this, headers: dict = {}) -> dict:
          return {
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'en-US,en;q=0.9',
             'sec-ch-ua': this.agent.ch.brands,
             'sec-ch-ua-mobile': this.agent.ch.mobile,
             'sec-ch-ua-platform': this.agent.ch.platform,
            **headers,
             'User-Agent': this.agent.text
          }
      
      def getCookies(this) -> tls_client.response.Response:
          return this.client.get('https://discord.com/login', headers = this.__construct_headers__({
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
             'Connection': 'keep-alive',
             'DNT': '1',
             'Host': 'discord.com',
             'sec-fetch-dest': 'document',
             'sec-fetch-mode': 'navigate',
             'sec-fetch-site': 'none',
             'sec-fetch-user': '?1'
          })) 

      def getExperiments(this) -> tls_client.response.Response:
          return this.client.get('https://discord.com/api/v9/experiments', headers = this.__construct_headers__({
             'Accept': '*/*',
             'Connection': 'keep-alive',
             'Cookie': this.__construct_cookies__(this.cookies.cookies),
             'DNT': '1',
             'Host': 'discord.com',
             'Referer': 'https://discord.com/register',
             'sec-fetch-dest': 'empty',
             'sec-fetch-mode': 'cors',
             'sec-fetch-site': 'same-origin',
             'X-Context-Properties': this.properties.__get_custom_properties__({'location': 'Register'}),
             'X-Debug-Options': 'bugReporterEnabled',
             'X-Discord-Locale': 'en-US',
             'X-Discord-Timezone': 'UTC',
             'X-Super-Properties': this.super_properties
          }))
    
      def signUp(this, email: str, username: str, password: str, global_name: str | None, date_of_birth: str, invite: str | None = None, captcha_key: str | None = None, cookies: tls_client.cookies.RequestsCookieJar | None = None) -> tls_client.response.Response:
          return this.client.post('https://discord.com/api/v9/auth/register', headers = this.__construct_headers__({
             'Accept': '*/*',
             'Connection': 'keep-alive',
             'Content-Type': 'application/json',
             'Cookie': this.__construct_cookies__(this.cookies.cookies) + ' ' + this.__construct_cookies__(cookies) if cookies else this.__construct_cookies__(this.cookies.cookies),
             'DNT': '1',
             'Host': 'discord.com',
             'Origin': 'https://discord.com',
             'Referer': 'https://discord.com/register',
             'sec-fetch-dest': 'empty',
             'sec-fetch-mode': 'cors',
             'sec-fetch-site': 'same-origin',
         **({'X-Captcha-Key': captcha_key} if captcha_key else {}),
             'X-Debug-Options': 'bugReporterEnabled',
             'X-Discord-Locale': 'en-US',
             'X-Discord-Timezone': 'UTC',
         **({'X-Fingerprint': this.experiments.json().get('fingerprint')} if this.experiments.json().get('fingerprint') else {}),
             'X-Super-Properties': this.super_properties,
          }), json = {
             'consent': True,
             'date_of_birth': date_of_birth,
             'email': email,
             'fingerprint': this.experiments.json().get('fingerprint'),
             'gift_code_sku_id': None,
             'global_name': global_name,
             'invite': invite,
             'password': password,
             'username': username
          })

      def getVerificationLink(this, verification_link: str) -> tls_client.response.Response:
          return this.client.get(verification_link, headers = this.__construct_headers__({
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
             'Connection': 'keep-alive',
             'Cookie': this.__construct_cookies__(this.cookies.cookies),
             'Host': 'discord.com',
             'DNT': '1',
             'sec-fetch-dest': 'document',
             'sec-fetch-mode': 'navigate',
             'sec-fetch-site': 'none',
             'sec-fetch-user': '?1'
          }))
      
      def verifyEmail(this, token: str, captcha_key: str) -> tls_client.response.Response:
          return this.client.post('https://discord.com/api/v9/auth/verify', headers = this.__construct_headers__({
              'Accept': '*/*',
              'Connection': 'keep-alive',
              'Content-Type': 'application/json',
              'Cookie': this.__construct_cookies__(this.cookies.cookies),
              'Host': 'discord.com',
              'DNT': '1',
              'sec-fetch-dest': 'empty',
              'sec-fetch-mode': 'cors',
              'sec-fetch-site': 'same-origin',
              'X-Debug-Options': 'bugReporterEnabled',
              'X-Discord-Locale': 'en-US',
              'X-Discord-Timezone': 'UTC',
              'X-Super-Properties': this.super_properties,
          **({'X-Fingerprint': this.experiments.json().get('fingerprint')} if this.experiments.json().get('fingerprint') else {})
          }), json = {'token': token, 'captcha_key': captcha_key})
      
      def acceptAgreements(this, token: str) -> tls_client.response.Response:
          return this.client.patch('https://discord.com/api/v9/users/@me/agreements', headers = this.__construct_headers__({
             'Accept': '*/*',
             'Authorization': token, 
             'Connection': 'keep-alive',
             'Content-Type': 'application/json',
             'Cookie': this.__construct_cookies__(this.cookies.cookies),
             'Host': 'discord.com',
             'DNT': '1',
             'sec-fetch-dest': 'empty',
             'sec-fetch-mode': 'cors',
             'sec-fetch-site': 'same-origin',
             'X-Debug-Options': 'bugReporterEnabled',
             'X-Discord-Locale': 'en-US',
             'X-Discord-Timezone': 'UTC',
             'X-Super-Properties': this.super_properties,
          }), json = {'terms': True, 'privacy': True})
      
      def connectWebsocketClient(this) -> None:
          this.websocket_client.connect('wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream')

      def initalizeVoice(this) -> None:
          return this.websocket_client.send(json.dumps({
             'd': {
               'channel_id': None, 
               'flags': 2,
               'guild_id': None,
               'self_deaf': False,
               'self_mute': True,
               'self_video': False
             },
             'op': 4
          }))

      def initalizeAccount(this, token: str) -> None:
          return this.websocket_client.send(json.dumps({
             'd': {
               'token': token,
               'capabilities': 16381,
               'compress': False,
               'properties': {pn: pv for pn, pv in json.loads(base64.b64decode(this.super_properties).decode()).items()},
               'client_state': {
                  'api_code_version': 0,
                  'guild_versions': {},
                  'highest_last_message_id': '0', 
                  'private_channels_version': '0',
                  'read_state_version': 0,
                  'user_guild_settings_version': -1,
                  'user_settings_version': -1
               },
               'presence': {
                  'activities': [],
                  'afk': False,
                  'since': 0,
                  'status': 'unknown'
               }
             },
             'op': 2, 
        }))
