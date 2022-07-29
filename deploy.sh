#!/bin/sh

sam validate
sudo sam build --use-container --debug
sam package --s3-bucket steamgametracker-lambda --output-template-file out.yml --region us-east-1
sam deploy --template-file out.yml --stack-name steam-game-tracker-api --region us-east-1 --no-fail-on-empty-changeset --capabilities CAPABILITY_IAM