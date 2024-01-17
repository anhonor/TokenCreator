# `TOKENCREATOR`
## `✴️` `INTRODUCTION`
**TokenCreator** is a simple tool used for creating unlocked and email verified tokens simultaneously. The program is comepletely requests based, so you can leave the program running and do anything you like while it is.
## `✴️` `REQUIREMENTS`
- `pip install -r requirements.txt`
- `python3 -m pip install -r requirements.txt`
## `✴️` `SETUP`
`config.json`
```json
{
    "threads": 175, // Thread Amount
    "thread_retry_delay": 0.25, // Thread Retry Delay,

    "global_name": "", // Name of Tokens -- [Optional]
    "invite": "", // Invite of Server -- [Optional]

    "captcha_key": "", // Paste Capmonster or Capsolver Key
    "captcha_provider": "", // Capmonster or Capsolver
    "captcha_proxyless": false, // Enables Proxied Solving -- [Optional]

    // DON'T CHANGE IF YOU DON'T UNDERSTAND
    "discord_email_verification_attempts": 5,
    "discord_email_verification_attempt_delay": 3,
    "mailmask_email_verification_attempts": 10,
    "mailmask_email_verification_attempt_delay": 2.5
}
```
