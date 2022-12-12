# TIMER WEB APP
### Video Demo:  https://youtu.be/5miYYUGP3cc
### Description:

Productivity timer web-application.

Web-based application. Check out this app using the link: http://apirus.pythonanywhere.com/



# Back-End:
- Flask
- SQL

## app.py 
In this file registration, log-in, log-out actions and field template rendering are implemented.
For the purpose of reducing complexity rendering of main page was separated to the files:
## 1) index_get.py
Rendering of main page.
## 2) index_post.py
Processing of all POST requests.

For data storing was used SQL database: 
##  database.db
Tables:
- users:
    - user_id
    - username
    - hash

- timers:
    - user_id
    - timestamp
    - timeramount
    - is_paused
    - totaltime

- backpack:
    - user_id
    - unlocked

- sprites:
    - sprite_id
    - location
    - seconds_to_unlock


## Front-End:

## HTML:
Layout and pages structure
## CSS: 
Used to create visual effects.
Bootstrap library navigation bar used with some visual modifications. 
- styles.scss: stylesheet for all app design
- animations.scss: stylesheet for sprites animation only.


## Javascript

Most of Javascript was written inside HTML. 
Javascript used to  keep tracking of time for user on the page. Also it helps to display progress bar dynamically. It receives info from database once page loads and start track it itself. When timer is finished it sends POST request to update  database timer data.

Also JS is used to display dynamic content on the field like sprites and decorators. Number, position of decorators and position of sprites are random, but it considers field area on the screen to keep items inside of a fied.

Another script was added to index.html to make user-friendly scroll-select for time choosing.


