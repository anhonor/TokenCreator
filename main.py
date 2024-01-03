import threading
from creator.modules.console import Console
from creator.modules.misc import __get_date_of_birth__, __get_random_string__
from creator.captcha import *
from creator.client import config, __get_proxy__, Client
from creator.cloudflare import *
from creator.mail import Mail
from creator.tempmail import Tempmail

console = Console()

def __solve_captcha__(site_key: str = DISCORD_SITE_KEY, site_url: str = DISCORD_SITE_URL) -> str | None:
    if config['captcha_provider'].upper() == 'CAPSOLVER':
       capsolver = Capsolver(config['captcha_key'])
       task_id = capsolver.__create_task__(site_key, site_url, None if config['captcha_proxyless'] else __get_proxy__())
       if not task_id:
          return
       captcha_key = capsolver.__get_task_result__(task_id)
       if captcha_key:
          console.__success__('Captcha Solved: {}** ({}s)'.format(captcha_key[0][:35], captcha_key[1]))
          return captcha_key[0]
       return
    
    if config['captcha_provider'].upper() == 'CAPMONSTER':
       capmonster = Capmonster(config['captcha_key'])
       task_id = capmonster.__create_task__(site_key, site_url)
       if not task_id:
          return
       captcha_key = capmonster.__get_task_result__(task_id)
       if captcha_key:
          console.__success__('Captcha Solved: {}** ({}s)'.format(captcha_key[0][:35], captcha_key[1]))
          return captcha_key[0]
       return
    
class Sequence:
      def __start__(this) -> None:
          def getClearance(client: Client) -> tls_client.cookies.RequestsCookieJar | None:
              cloudflare = Cloudflare(client)
              try:
                cloudflare_ray = str(cloudflare.getRay().headers.get('Cf-Ray')).split('-')[0]
                cloudflare_clearance = cloudflare.getClearance(cloudflare_ray)
                if len(cloudflare_clearance.cookies):
                   console.__success__('Retrieved Clearence ({})'.format(cloudflare_clearance.cookies.get('cf_clearance')))
                else:
                   console.__failure__('Failed Retrieving Cloudflare Clearance')
                return cloudflare_clearance.cookies
              except Exception as E:
                 console.__warning__('{}: {}'.format(type(E), str(E)))
              
          def getMailmask(client: Client, tempmail: Tempmail) -> tuple | None:
              mail = Mail(client.proxy)
              try:
                username = __get_random_string__(7)
                password = __get_random_string__(7) + '*'

                create_user = mail.createUser(username, password, username, tempmail.address)
                if create_user.json().get('data') and create_user.json()['data'].get('createUser'):
                   open('./data/output/mailmask.txt', 'a+').write('{}:{}:{}\n'.format(tempmail.address, username, password))
                  
                   address = username + '@mailmasker.com'
                   console.__success__('Created Mailmask: {} ({}:{})'.format(address, username, password))

                   me = mail.getMe(create_user.cookies)
                   if me.json().get('data') and me.json()['data'].get('me'):
                      verification_link = tempmail.__find_mask_verification_link__(config['mailmask_email_verification_attempts'], config['mailmask_email_verification_attempt_delay'])
                      if '/code/' in str(verification_link):
                         code = verification_link.split('/code/')[1]
                         verify_email = mail.verifyEmail(code, tempmail.address, create_user.cookies)
                         if verify_email.json().get('data') and verify_email.json()['data'].get('verifyEmailWithCode'):
                            open('./data/output/mailmask-verified.txt', 'a+').write('{}:{}:{}\n'.format(tempmail.address, username, password))
                            
                            console.__success__('Verified Mailmask: {} ({}:{})'.format(address, username, password))
                            return (address, username, password)
                         else:
                            console.__failure__('Mailmask Not Verified: {} ({})'.format(address, tempmail.address))
                      else:
                         console.__failure__('Mailmask Verification Link Not Returned: {}'.format(tempmail.address))
                else:
                   console.__failure__('Mailmask Not Created: {}'.format(tempmail.address))
              except Exception as E:
                 console.__warning__('{}: {}'.format(type(E), str(E)))

          try:
            client = Client(__get_proxy__())
            clearance = getClearance(client)

            email_username = __get_random_string__(7).lower()
            email_password = __get_random_string__(7).lower()
            tempmail = Tempmail(email_username, email_password, client.proxy)
            mailmask = getMailmask(client, tempmail)
            if not mailmask:
               return          
            
            captcha_key = __solve_captcha__()
            display_name = config['global_name'] if config['global_name'] else None
            username = __get_random_string__(8)
            password = __get_random_string__(8) + '*'

            signup = client.signUp(mailmask[0], username, password, display_name, __get_date_of_birth__(), config['invite'] if config['invite'] else None, captcha_key, clearance)  
            if signup.json().get('token'):
               open('./data/output/tokens.txt', 'a+').write(f'{signup.json()["token"]}:{mailmask[0]}:{password}\n')

               console.__success__('Token Created: {} ({}:{})'.format(signup.json()['token'], mailmask[0], password))
               try:
                 client.connectWebsocketClient()
                 client.initalizeVoice()
                 client.initalizeAccount(signup.json()['token'])
                 console.__success__('Emitted Voice & Account Websockets ({})'.format(signup.json()['token']))
               except Exception as E:
                 console.__failure__('Websocket Emission Failed ({})'.format(signup.json()['token']))

               verification_link = tempmail.__find_discord_verification_link__(config['discord_email_verification_attempts'], config['discord_email_verification_attempt_delay'])
               if verification_link:
                  console.__success__('Retrieved Discord Verification Link: {} ({})'.format(verification_link, signup.json()['token']))

                  verification = client.getVerificationLink(verification_link)
                  if verification.headers.get('Location'):
                     console.__success__('Redirected: {} ({})'.format(verification.headers['Location'], signup.json()['token']))

                     verification_token = verification.headers['Location'].split('#token=')[1]
                     captcha_key = __solve_captcha__(DISCORD_EMAIL_SITE_KEY)
                     verify = client.verifyEmail(verification_token, captcha_key)
                     if verify.json().get('token'):
                        open('./data/output/tokens-verified.txt', 'a+').write('{}:{}:{}\n'.format(verify.json()['token'], mailmask[0], password))
                        console.__success__('Token Verified: {} ({}:{})'.format(verify.json()['token'], mailmask[0], password))
                        
                        agreements = client.acceptAgreements(signup.json()['token'])
                        if agreements.status_code in [200, 201, 202, 203, 204]:
                           console.__success__('Token Unlocked: {} ({}:{})'.format(verify.json()['token'], mailmask[0], password), v1 = False)
                           open('./data/output/tokens-unlocked.txt', 'a+').write('{}:{}:{}\n'.format(verify.json()['token'], mailmask[0], password))
                        else:
                           console.__failure__('Token Locked: {} ({}:{})'.format(verify.json()['token'], mailmask[0], password))
                     else:
                        console.__failure__('Token Not Verified: {}'.format(signup.json()['token']))
                  else:
                     console.__failure__('Invalid Discord Verification Link: {}')
               else:
                  console.__failure__('Discord Verification Link Not Returned ({})'.format(signup.json()['token']))
          except Exception as E: 
             console.__unknown__('{}: {}'.format(type(E), str(E)))
      
def __main__():
    while 1:
       sequence = Sequence()
       sequence = sequence.__start__()
       time.sleep(config['thread_retry_delay'])

for thread in range(config['threads']):
    thread = threading.Thread(target = __main__)
    thread.start()
