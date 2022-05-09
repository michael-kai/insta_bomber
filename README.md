# insta_sender
Insta_sender is python script for Instagram.

This script let you collect subscribers of any given account and then send Direct Messages to this subscribers.

## Instruction
- Install requirements.txt
- Create .env file in project dir.
  Place there 2 variables - login and password. This credentials will be used to login to account which will send messages.
  
  E.g.:
  
  login=YOUR_LOGIN
  
  password=YOUR_PASSWORD
  
 - In the end of insta_sender.py enter account you want to scrape.
 - Prepare message you want to share. This message must contain random variables. This will help you to avoid bans from Instagram longer. In method **prepare_msg** given example of variables and message.
 - Run script.

## Caution!
- Limits - max count of subscribers to send messages limited to 500 in **MaxSubsCount** attr. Because of Instagram bans, between each sent message script take pause for 420 seconds (7min). Now count how long it will takes for 1000 subs and more!
- Script sends messages only to not private subscribers.
- If in some case **sending** process will be aborted, you can just rerun script and continue send messages without duplicates.
