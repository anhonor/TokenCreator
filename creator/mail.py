import requests
import ua_generator

class Mail:
      def __init__(mail, proxy: dict | None = None) -> None:
          mail.agent = ua_generator.generate(device = ('desktop'), browser = ('chrome'))
          mail.proxy = proxy

      def __construct_cookies__(mail, cookies: requests.cookies.RequestsCookieJar) -> str:
          return ' '.join('{}={};'.format(cookie.name, cookie.value) for cookie in cookies)

      def __construct_headers__(mail, headers: dict = {}) -> dict:
          return {
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'en-US,en;q=0.9',
             'sec-ch-ua': mail.agent.ch.brands,
             'sec-ch-ua-mobile': mail.agent.ch.mobile,
             'sec-ch-ua-platform': mail.agent.ch.platform,
            **headers,
             'User-Agent': mail.agent.text
          }

      def createUser(mail, forwarding_address: str) -> requests.Response:
          return requests.post('https://423ghva5nf.execute-api.eu-west-1.amazonaws.com/prod/mails', headers = mail.__construct_headers__({
             'Accept': '*/*',
             'Content-Type': 'application/JSON',
             'Origin': 'https://www.mailmask.me',
             'Referer': 'https://www.mailmask.me/',
             'sec-fetch-dest': 'empty',
             'sec-fetch-mode': 'cors',
             'sec-fetch-site': 'cross-site'
          }), json = {'forwardingAddress': forwarding_address, 'label': ''})
