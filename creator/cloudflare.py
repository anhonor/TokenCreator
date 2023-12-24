import tls_client

class Cloudflare: 
      def __init__(this, client) -> None:
          this.client = client

      def getRay(this) -> tls_client.response.Response:
          return this.client.client.get('https://discord.com/cdn-cgi/challenge-platform/h/b/scripts/56d3063b/main.js', headers = this.client.__construct_headers__({
             'Accept': '*/*',
             'Connection': 'keep-alive',
             'Cookie': this.client.__construct_cookies__(this.client.cookies.cookies),
             'DNT': '1',
             'Host': 'discord.com',
             'sec-fetch-dest': 'script',
             'sec-fetch-mode': 'no-cors',
             'sec-fetch-site': 'same-origin'
          }))

      def getClearance(this, ray: str) -> tls_client.response.Response:
          return this.client.client.post('https://discord.com/cdn-cgi/challenge-platform/h/b/jsd/r/{}'.format(ray.split('-')[0]), headers = this.client.__construct_headers__({
             'Accept': '*/*',
             'Connection': 'keep-alive',
             'Cookie': this.client.__construct_cookies__(this.client.cookies.cookies),
             'DNT': '1',
             'Host': 'discord.com',
             'Origin': 'https://discord.com',
             'Referer': 'https://discord.com/',
             'sec-fetch-dest': 'script',
             'sec-fetch-mode': 'no-cors',
             'sec-fetch-site': 'same-origin'
          }), json = {'s': None, 'wp': None})
