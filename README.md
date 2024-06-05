# FLASHCARDS 4 ISA

MCS 275 Spring 2024 Project 4 by Jack Chylak

## Description

Flashcards 4 Isa is a web app that uses Flask and SQLite that I created so that my girlfriend, Isabelle, could
have a place to study flashcards without being paywalled or bombarded by advertisements. 
Isabelle is a pre-med students so studying takes up a substantial amount of her time. 
I worked closely with her to create a studying app to fit her needs, thus, Flashcards 4 Isa!
This application uses Flask to generate webpages such as a 'login' page, a 'home' page for users 
to access everything in the app, a 'flashcard' and 'deck' input page for users to add the front and back of 
a flashcard to an SQLite database, and a 'study' page that allows the user to study any decks that they have created 
by displaying the front and back of all flashcards in a deck.

## How to test

Since this program is built off of 'TaskGain' by David Dumas, much of the operation is the same.
Running the flashcards4isa.py file should initialize the 'http://127.0.0.1:5000' or similar link that pops
up in the terminal after clicking run. All app functionality takes place within this flask-generated page. 
Following this link, the user should login with a username. Once the user inputs username, 
they will be taken to a home page view that displays two large buttons to allow the user to add a new flashcard 
or add a new deck. Clicking either one of these buttons will redirect the user to a flashcard or deck input page. 
Filling out these prompts, a flashcard or deck will be added to the flashcards4isa.db SQLite database. 
User can click the 'Flashcards4Isa' logo at the top of each page to return to the home page. Once the user
adds a card or deck, the deck(s) will be displayed at the bottom of the home page, clicking on any of these 
deck buttons will redirect the user to the study page for the clicked deck. Here, the user can scroll through 
that deck and study all of its cards!

## Personal contribution

The front.html page was largely adapted from 'TaskGain' by David Dumas, all other html pages are completely 
my contribution. The 'flashcards4isa.css' page is also adapted from 'TaskGain', although almost completely changed, 
I used it more as a guide to design my pages as I haven't used css or html before. As for the main 'flashcards4isa.py' file, 
the login form was largely adapted from 'TaskGain' the rest of the functions are my contributions. The functions that use 
SQLite and adjacent dictionaries were influenced by 'TaskGain' and David Dumas' teaching of Flask and SQLite 
although largely changed to perform more actions.

## Sources and credits

I consulted David Dumas for advice and ideas when brainstorming my project including the use of SQLite databases, 
much of the project was also heavily influenced by David's project, 'TaskGain', I used much of his project, as a 
working flask app, to guide my program.
I also consulted CSS and HTML documentation to add things like box shadows and text wrapping.