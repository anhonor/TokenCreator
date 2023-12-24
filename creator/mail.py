import requests
import ua_generator
import uuid

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

      def createUser(mail, username: str, password: str, email_username: str, email: str) -> requests.models.Response:
          return requests.post('https://api.mailmasker.com/graphql?name=CreateUser', headers = mail.__construct_headers__({
             'Accept': '*/*',
             'Connection': 'keep-alive',
             'Content-Type': 'application/json',
             'DNT': '1',
             'Host': 'api.mailmasker.com',
             'Origin': 'https://api.mailmasker.com', 
             'Referer': 'https://api.mailmasker.com/',
             'sec-fetch-dest': 'empty',
             'sec-fetch-mode': 'cors',
             'sec-fetch-site': 'same-site'
          }), json = {
             'operationName': 'CreateUser',
             'query': 'mutation CreateUser($username: String!, $password: String!, $uuid: String!, $persistent: Boolean!, $verifiedEmail: String!, $emailMask: String!) {\n  createUser(username: $username, password: $password, uuid: $uuid, persistent: $persistent, verifiedEmail: $verifiedEmail, emailMask: $emailMask) {\n    userID\n    __typename\n  }\n}\n',
             'variables': {
                'emailMask': '{}@mailmasker.com'.format(email_username), 
                'password': password,
                'persistent': True,
                'username': username,
                'uuid': str(uuid.uuid4()),
                'verifiedEmail': email
             }
          }, proxies = mail.proxy)

      def getMe(mail, cookies: requests.cookies.RequestsCookieJar) -> requests.models.Response:
          return requests.post('https://api.mailmasker.com/graphql?name=Me', headers = mail.__construct_headers__({
             'Accept': '*/*',
             'Connection': 'keep-alive',
             'Content-Type': 'application/json',
             'Cookie': mail.__construct_cookies__(cookies),
             'DNT': '1',
             'Host': 'api.mailmasker.com',
             'Origin': 'https://api.mailmasker.com', 
             'Referer': 'https://api.mailmasker.com/',
             'sec-fetch-dest': 'empty',
             'sec-fetch-mode': 'cors',
             'sec-fetch-site': 'same-site'
          }), json = {'operationName': 'Me', 'query': 'query Me {\n  me {\n    user {\n      id\n      username\n      plan {\n        displayName\n        type\n        __typename\n      }\n      routes {\n        id\n        redirectToVerifiedEmail {\n          id\n          email\n          verified\n          __typename\n        }\n        emailMask {\n          id\n          domain\n          alias\n          parentEmailMaskID\n          __typename\n        }\n        expiresISO\n        __typename\n      }\n      verifiedEmails {\n        id\n        email\n        verified\n        __typename\n      }\n      emailMasks {\n        id\n        domain\n        alias\n        parentEmailMaskID\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n', 'variables': {}}, proxies = mail.proxy)

      def verifyEmail(mail, code: str, email: str, cookies: requests.cookies.RequestsCookieJar) -> requests.models.Response:
          return requests.post('https://api.mailmasker.com/graphql?name=VerifyEmailWithCodeMutation', headers = mail.__construct_headers__({
             'Accept': '*/*',
             'Connection': 'keep-alive',
             'Content-Type': 'application/json',
             'Cookie': mail.__construct_cookies__(cookies),
             'DNT': '1',
             'Host': 'api.mailmasker.com',
             'Origin': 'https://api.mailmasker.com', 
             'Referer': 'https://api.mailmasker.com/',
             'sec-fetch-dest': 'empty',
             'sec-fetch-mode': 'cors',
             'sec-fetch-site': 'same-site'
          }), json = {'operationName': 'VerifyEmailWithCodeMutation', 'query': 'mutation VerifyEmailWithCodeMutation($email: String!, $code: String!) {\n  verifyEmailWithCode(email: $email, code: $code) {\n    id\n    email\n    verified\n    __typename\n  }\n}\n', 'variables': {'code': code, 'email': email}}, proxies = mail.proxy)
