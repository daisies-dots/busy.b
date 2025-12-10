# busy.b Design: A Comprehensive Tour

## Context
In high school, I was really passionate about bullet journaling, however since coming to college, I haven't had as much time to maintain that passion. So, this app is greatly inspired by nature-themed bullet journal spreads, as well as video-game pixel art - one of my favorite styles. I also wanted to expand my skillset in Flask and JavaScript, and I did so by learning how to change images upon task completion, implementing an interactive rain element, and more!

## Organization
The project follows a typical Flask structure, separating backend logic (Flask), presentation (HTML/CSS) and assets (images):
```
/static
    /css
    /js
    /images (plant stages, UI assets)
    
/templates
    apology.html
    garden.html
    goal.html
    index.html
    login.html
    signup.html
    tasks.html

app.py
helpers.py
busyb.db
DESIGN.md
README.md
requirements.txt
```

## Back End Implementation Choices
I used Python and Flask as the basis for my app. I chose Flask for its Jinja templating, easy session control, and simple integration with SQLite3 databases. 

### Account Management
For the login, my Flask routes and my SQLite3 database were based off of CS50 Finance, including a hashed password for extra security. 

### Main Pages
I researched how to use a POST request to insert new tasks from the goal addition page into the tasks table, and how to relate task completion to the plant growth cycle (switching image variants from 1 (seed) to 4 (flower)). 

### Flask Routes
- `/` — home page  
- `/login` — handles POST login; checks hashed password  
- `/signup` — inserts new user in database
- `/logout` - clears session and redirects to login  
- `/goal` — allows users to create goals and subtasks
- `/save_goal` - validates that goals exist and redirects the user to the tasks page
- `/tasks` — retrieves goals and subtasks for the logged-in user
- `/complete_task` - updates subtask rows in the database to display the next stage in plant growth
- `/garden` — computes goal and subtask progress, shows all plants with their current images  
- `/logout` — clears session 

### SQLite3 Databases
Within my main database, busyb.db, I have included a users table (id/PRIMARY KEY, username, password), a goals table (id, user_id, goal_text, timestamp), and a subtasks table (id, goal_id, task_text, completed status).

Whenever users check off subtasks, the route recalculates number of completed subtasks, and sets the correct plant stage image. Once the last stage is reached, a random flower color is chosen and the corresponding image path is stored to update the garden and task pages instantaneously. All stage changes are displayed using Jinja templates

## Front End Design Choices
For the UI, I used HTML/CSS, as well as JavaScript for some additional decorations and button commands (rain animation, click sensing). I also uploaded my digital hand-drawn plant stages into the static folder, sizing and arranging them accordingly using HTML and CSS. I made sure to have a consistent, accessibility-friendly color scheme across all pages, and used several layout classes - textareas, forms, and tables to name a few - to introduce variability into my pages.

## My Original Goals
I was able to achieve my baseline goals (to have a full "plant growth cycle" with drawn visuals, 3 subtasks, a functioning SQL database, and several Flask pathways) as well as the "better outcome" goals(having several randomized flower types/colors, a login system, and small animations like rain) from my original proposal. The randomized flower color allowed for extra personality, without requiring too much effort or reworking of code.

Overall, I feel that I had a good balance of interactive elements and static pixel artwork. I'm excited to share it with you all!
