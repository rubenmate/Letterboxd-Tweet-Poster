# Letterboxd-Tweet-Poster
Post your logged films/created lists on Lettterboxd to a Twitter thread

## Instructions

1. You should build the image: ```docker build . -t letterbot```
2. Ask for Twitter Developer access.
3. Run the container export the following environmental variables: '
```
docker run -it -e CONSUMER_KEY="uDRNy31oWfoiKV9AvPoNavy0I" \
-e CONSUMER_SECRET="lnAL5VAgZLWNspQVpd3X6tEo47PRCmsPEwuxpvLCLSR08DMa4O" \
-e ACCESS_TOKEN="622518593-j7gWSqzQO31ju7Bf7idB47NlZeSENsuADGU9B69I" \
-e ACCESS_TOKEN_SECRET="iutFsxvP5IglRckJ1I1why6017xMNkzxqBID48Azw0GvT" \
-v /home/pi/.config/appdata/letterbot:/src \
letterbot
 ```
 
Note: These are examples, you should export your own Twitter tokens.