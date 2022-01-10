# Letterboxd-Tweet-Poster

Post your logged Letterboxd films to a Twitter thread

## Instructions

1. Edit source code with the main tweet and your desired wait time.
2. Ask for your Twitter Developer access
3. Export your keys as environmental variables.
4. Run the script.
5. You can adjust the settings with the config.json what will be created.
6. If you want to run it as a docker container you can use the dockerfile.

### Docker Container
1. Clone repository `git clone https://github.com/rubenmate/Letterboxd-Tweet-Poster`
2. Move to the cloned folder
3. Build the image `docker build -t letterbot .`
4. Export environment variables to a file `echo CONSUMER_SECRET=foo >> my-env.txt`
5. Run the container `docker run --env-file ~/my-env.txt letterbot`
