# 🐝 busy.b: 
## A Plant-Lover's Productivity Tracker

### Link: https://youtu.be/CJe45e0EMPI

![busy.b](static/busyb.png)

## 🌸 Description
busy.b is a productivity tracker that makes completing goals and mini subtasks fun and easy, with a gamified, plant-themed twist! Add 3-part goals, complete subtasks, and watch your progress unfold through different stages of plant growth in your personal garden! 

This app was developed using VisualStudioCode, built in Python 3 using the Flask framework, SQLite3 to manage the database, and HTML/CSS for the UI.

## 🌱 Usage

### Account Information
Users first need to sign up, with new usernames and hashed passwords stored in a secure SQLite3 database. The log out button in the navigation bar redirects users to the login page, clearing current data and allowing for multiple users to access busy.b on the same device.

### Home Page
The home page connects to all the other pages (add goal, continue tasks, and view garden) through both the navigation bar and the main content.

### Add Goal
Users can enter their goal and three smaller subtasks. If no goal is entered, the user encounters an error and is redirected.

### Continue Tasks
Tasks from added goals are tracked and completed through tables, with plant stage status being automatically updated as tasks are completed.

### View Garden
The garden is a viewable collection of all current plant tasks, ordered chronologically. Final flower colors are generated randomly, for a new surprise each time.

### Errors
Errors route through apology.html page, with a short description of the issue at hand.

## ✏️ Dependencies
The app relies on: cs50, Flask, Flask-Session. These are listed in requirements.txt for easy installation.

To install, download and unzip the project folder. Ensure **Python 3.10+** is installed. Install dependencies in requirements.txt, and run the app using `flask run --debug` or `python app.py`.

Then, open browser and navigate to http://127.0.0.1:5000/.

## Authors
Victoria Chen 
Github: @daisies-dots
Last Edited: 12/06/2025
