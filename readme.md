# Trading Alert Bot

This bot monitors a range of HIGH performing Stock and crypto. 
It monitors their prices throughout the day, by cheching their prices evry minute, if there is a 0.1% increase or decrease in their price a notification would be sent to a phone number Via Twilio to notify of this change.

## Deployment on Heroku

1. Sign up for Heroku and install CLI.
2. Set environment variables:
   - STOCK_API_KEY
   - TWILIO_SID
   - TWILIO_AUTH
   - FROM_NUM
   - TO_NUM
3. Create a new app:
   `heroku create your-bot-name`
4. Push code:
