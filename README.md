# Advpy Final App

| Names | Dan, Jack, and Quentin |
|:---|:---|
| **Course** | CSCI310-001-25688 Adv Prog: Python |
| **Section** | 1 |
| **Semester** | Fall 2023 |
| **Repository**          | https://github.com/LobotomyTerror/advpy-final |
| **Self Grade** | We used a public API, Mongodb, and flask. We used the course container and adhered to Git best practices. In addition, we assigned ussues to each member and created branches for each issue. We also used a Makefile to automate local tests, unittest, mypy type checking, and pep8 style checking. Self grade: 100% |
| **Notes** | Why we gave ourselves a self grade of 100% is because we felt that we followed the directions very well in creating this app. Using a public api and getting that to operate properly. As well as the setup and use of MongoDB where we utilized this feature appropriately with storing, retrieving, and deleting from said cluster. Were we lacked on making good issues on github projects communictaion between team members was still good, since we would meet up and message about issues and planned implementations. Also the entire time we made any changes to the program we utilized the provided makefile from Dr. Basnet's repo so we were adhereing to the type checking and styling best practices. Along with, keeping good documentation in the code to understand what was happening in the different functions that we used. The one thing that I messed up on was that I didn't realize I needed the workflows file for the green check mark but I quickly changed it and added the required modules to the ci/cd text file.|



### Must Need

To use these files you will need a env file that stores your api keys and auth codes which can be created on the TMDB website. The same goes for MongoDB as well if that is the cloud storage service you are using. I included Dr. Basnet's files from his [docker-heroku](https://github.com/rambasnet/flask-docker-mongo-heroku) repo so that the githooks and workflows will run correctly and git the :white_check_mark: when pushing to the repo. 

I changed my tune with the config file being available on github and instead I changed the file to a .env file. The reason being is that if I change the repo to public I do not want my sensitive info on github, so for this to work you need a env file in the root directory so that when the program is ran it will know where to look: 

```
MONGODB_USRNM='your_actual_username'
MONGODB_PASS='your_actual_pass'
TMDB_API_KEY='tmdb_api_key'
TMDB_AUTH_KEY='tmdb_auth_key'
```
Deplyment through Heroku is already setup so no need to worry about adding these variables to it. I didn't realize that when deploying through Heroku you can config the environment variables so that Heroku can easily run the program. Thus, the env file is still needed with your own clone of this repo along with your own credential. 

### Overview

I just wanted to give a brief explination on what this program really is. To start the purpose of this program is to allow a user the ability to enter in a genre for movies or tv shows that are randomly display to help the user choose something to watch. The homepage allows for the user to select from either searching for movies by genre or tv shows by genre, then changing to the next screen where the user can then enter specific search parameters pertaining to a specific genere that they want browse through. Then once the genre is entered the endpoint calls the api returning the data for said genre and then storing it into a database of our own to be acessed in the next couple of webpages. On the last couple of screens there is a layout where the user can scroll through the tiles of movies or tv shows and see the poster of the movie along with the title and the voter's average score from the TMDB site. Finally, you can click on any of the tiles and it brings you to a new page showing some of the same information, adding a trailer and a description about the movie (I had planned on adding more to that screen but was a little limted on data that I could use from TMDB I might mess with it on my free time). 

The program is sperated into three main files that are the "back bone" of the app that we created. A main, app, and database file were used as a stepping stone to separate the functionality of the operation of the program and easier navigation of how it all worked. The main file handled all the api calls and processing of that data since it required quite a bit of work to operate correctly to get the data that we were looking for to match the design of the app we created. The app file is the flask implementation of the app so it handled all the POST and GET requests so that we could appropriately query the api endpoints for said data we wanted to recieve. Lastly, is the database file, as the name states it handled all the database insertion, deletion, and retrieval into our MongoDB cluster that we used to store the data and retrieve when needed. To me this made the most sense as it had a lot of movie parts and it was only reasonable to have these operations separated into different files so and work preformed could be easily tracked to where it needed to go and where it was coming from.
