# Advpy Final App


### Must Need

To use these files you will need a config file that stores your api keys and auth codes which I will give out. I have a mongodb cluster set up and the movie database api key and authcode, I will get this setup for you both when you want me too. Finally, the files that are not included into the repository are the files from Dr. Basnet's repository for the [docker-heroku](https://github.com/rambasnet/flask-docker-mongo-heroku) files.

I changed my tune with the config file being available on github and instead I changed the file to a .env file. The reason being is that if I change the repo to public I do not want my sensitive info on github, so to fix this for this app you will need to change the file to a .env in the program directory then you will have to add: 

```
MONGODB_USRNM='your_actual_username'
MONGODB_PASS='your_actual_pass'
TMDB_API_KEY='tmdb_api_key'
TMDB_AUTH_KEY='tmdb_auth_key'
```
Deplyment through Heroku is already setup so no need to worry about adding these variables to it.

Hello just a test
