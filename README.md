# TIMER WEB APP
### Video Demo:  https://youtu.be/5miYYUGP3cc
### Description: Productivity timer web-application.

Web-based application. Check out this app using the link: http://apirus.pythonanywhere.com/


# How the webpage works?
The idea is simple. User creates an account. During registration you need to enter fields:
Username: must be at least 3 symbols long,  checked to be unique.
Password, Confirm password: it is checked to match, must be at least 8 symbols long.

After registration user can select time and start timer. The idea is not to distract users when they use app.
User can pause or stop timer at any time. As a reward for productive work user unlock different animals. Progress bar at the bottom of the page shows dynamically users progress and next goal. All of unlocked animals show up on the Field tab.
Every time new animal unlocked user will see an animation showing it.

# Back-End:
- Flask
- SQL

## app.py 
In this file registration, log-in, log-out actions and field template rendering are implemented.
For the purpose of reducing complexity rendering of main page was separated to the files:
## 1) index_get.py
Rendering of main page.
## 2) index_post.py
Processing of all POST requests: start_timer, finish_timer, stop_timer, pause_timer, resume_timer, upgrade.

For data storing was used SQL database: 
##  database.db
Tables:
- users:
    - user_id 
    - username - created by user
    - hash - storing passwords

- timers:
    - user_id
    - timestamp - start of timer in format of '2022-11-11 11:11:11';
    - timeramount - time for which user set timer, seconds;
    - is_paused - boolean, if timer is running - 0, if paused - 1;
    - totaltime - total time user spend using timer. Used to track user progress in unlocking new animals and progtress bar.

- backpack:
    - user_id
    - unlocked - sprite_id (int) adds to users own backpack when they unlock new animal.

- sprites:
    - sprite_id
    - location - relative path of sprite image;
    - seconds_to_unlock - amount of seconds to unlock each animal.



## Front-End:

## HTML:
Layout and pages structure.
## CSS: 
Used to create visual effects.
Bootstrap library navigation bar used with some visual modifications. 
- styles.scss: stylesheet for all app design
- animations.scss: stylesheet for sprites animation only.
Responsive design achived using using Bootstrap and CSS @media rule.
Animations made using @keyframes rule. Sprite sheets were used for animations as div's background image and by moving background image position to the left using steps. 

## Javascript

Most of Javascript was written inside HTML. 
Javascript used to  keep tracking of time for user on the page. Also it helps to display progress bar dynamically. It receives info from database once page loads and start track it itself. When timer is finished it sends POST request to update  database timer data. Main idea was to reduce number of database updates. So time trackind is going in JS, and updates are send to database only if user interacts(start, pause, resume, stop) or end of timer.

Also JS is used to display dynamic content on the field like sprites and decorators. Number, position of decorators and position of sprites are random, but it considers field area on the screen to keep items inside of a fied.

Another script was added to index.html to make user-friendly scroll-select for time choosing.

***confetti.js*** was taken from https://www.cssscript.com/confetti-falling-animation/ , created by **mathusummut**.


