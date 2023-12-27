import base64
import json
import re
import requests
import ua_generator
import ua_parser.user_agent_parser

def __get_build_number__() -> str:
    login_page = requests.get('https://discord.com/login')
    asset_file = 'https://discord.com/assets/' + re.compile(r'assets/+([a-z0-9\.]+)\.js').findall(login_page.text)[94] + '.js'
    asset_file = requests.get(asset_file)
    build_numb = asset_file.text.split('".concat("')[1].split('"')[0]
    return build_numb

build_number = __get_build_number__()

class Properties:
      def __init__(this, agent: ua_generator.useragent.UserAgent) -> None:
          this.agent = agent.text

      def __get_custom_properties__(this, data: dict = {}) -> str:
          return base64.b64encode(json.dumps({**data}, separators = (',', ':')).encode()).decode() + '='

      def __get_super_properties__(this, additional: dict = {}) -> str:
          agent = ua_parser.user_agent_parser.Parse(this.agent)
          return base64.b64encode(json.dumps({
               'os': agent['os']['family'],
               'browser': agent['user_agent']['family'],
               'device': '',
               'system_locale': 'en-US',
               'browser_user_agent': this.agent,
               'browser_version': '.'.join(filter(None, [agent['user_agent']['major'], agent['user_agent']['minor'], agent['user_agent']['patch']])),
               'os_version': '.'.join(filter(None, [agent['os']['major'], agent['os']['minor'], agent['os']['patch']])),
               'referer': '',
               'referring_domain': '',
               'referring_current': '',
               'referring_domain_current': '',
               'release_channel': 'stable',
               'client_build_number': build_number,
               'client_event_source': None,
               **additional
          }, separators = (',', ':')).encode()).decode()
