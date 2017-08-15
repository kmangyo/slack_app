# slack_app
## My slack app

1. My twit memoy with AWS, Rstudio and Twitter.

### Reference
with aws

http://datum.io/aws-ec2-rserver-installation1/
https://aws.amazon.com/ko/free/
http://www.louisaslett.com/RStudio_AMI/

with slack api

https://api.slack.com/incoming-webhooks
https://api.slack.com/apps/A5FUJL2CT/oauth
https://github.com/hrbrmstr/slackr

with schedular

win) https://github.com/bnosac/taskscheduleR
linux) https://github.com/bnosac/cronR

## My slack bot

1. slackbot w/ artworks in Seoul Museum of Art
- Using slack, heroku and Seoul Open API.

```
cd slackbot
virtualenv slackbot
source slackbot/bin/activate

pip freeze> requirements.txt
echo python-2.7.11 > runtime.txt
echo worker: python myslackbot.py > Procfile
printf "*.pyc\nslackbot/" > .gitignore

heroku login
git init

heroku create --buildpack heroku/python

git add .
git commit -m ‘init’
git push heroku master

heroku ps:scale worker=1
```

### Reference
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
http://www.craftplustech.com/blog/?p=1434

