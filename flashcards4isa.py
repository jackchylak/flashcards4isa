# Jack Chylak
# MCS 275 Project 4
# Flashcards 4 Isa
# Adapted from "TaskGain" by David Dumas and I am the sole author of the changes except as noted in README.md.
# Spring 2024, Dumas


"""
Flashcards 4 Isa is a web app that uses Flask and SQLite that I created so that my girlfriend, Isabelle, could
have a place to study flashcards without being paywalled or bombarded by advertisements. 
Isabelle is a pre-med students so studying takes up a substantial amount of her time. 
I worked closely with her to create a studying app to fit her needs, thus, Flashcards 4 Isa!
This application uses Flask to generate webpages such as a 'login' page, a 'home' page for users 
to access everything in the app, a 'flashcard' and 'deck' input page for users to add the front and back of 
a flashcard to an SQLite database, and a 'study' page that allows the user to study any decks that they have created 
by displaying the front and back of all flashcards in a deck.
"""


import time
import sqlite3
from flask import Flask, render_template, request, redirect


flashcards_db = "flashcards4isa.db"

USERNAME = ""   #global username that updates when user logs in to allow user to click logo and return to home page

UPDATABLE_COLS = ["card_front", "card_back", "deck"]    #indicates which database table attributes can be modified


app = Flask(__name__)


# The next function implements the / route that displays the login page and is adapted from 'TaskGain' by David Dumas
@app.route("/") 
def front():
    "Front login page"
    return render_template("front.html", fail=request.values.get("fail"))   #renders login page or error message if username is empty


# The next function implements the /login route that allows the user to input a username and is 
# adapted from 'TaskGain' by David Dumas
@app.route("/login", methods=["GET", "POST"])
def login():
    "Login action: sends user to home view"
    global USERNAME
    USERNAME = request.values.get("username") # assign global variable USERNAME for activation of home button (when user clicks logo)
    if USERNAME is None or (not USERNAME.strip()):
        return redirect("/?fail=1", code=302)
    return redirect("/home/{}/".format(USERNAME), code=302) # redirects user to their home page


@app.route("/home/<username>/")
def flashcards_home_view(username):
    "View of user's decks and allow creation of new cards and decks"
    global USERNAME
    USERNAME = username
    con = sqlite3.connect(flashcards_db)

    user_home = con.execute(
        """
        SELECT cardid, deck, deck_status, created_ts, updated_ts
        FROM flashcards
        WHERE owner=?
        ORDER BY updated_ts DESC;
        """,
        [username],
    )
    user_decks = {} #create parallel dictionary that mirrors SQLite database for use in html files
    for row in user_home:
        deck = row[1]
        user_decks[deck] = (
            {
                "cardid": row[0],
                "deck": row[1],
                "deck_status_str": row[2],
                "created_ts": row[3],
                "created_str": row[3],
                "updated_ts": row[4],
                "last_studied": row[4],
            }
        )   # The use of a parallel dictionary to go with the SQLite database was inspired by 'TaskGain' by David Dumas

    return render_template(
        "home.html",
        username=username,
        user_decks=user_decks,
    )


@app.route("/card/new/")
def add_card_form():
    "Display the form to create a new card"
    global USERNAME
    username_home = USERNAME
    return render_template(
        "add_card.html",
        username_home = username_home,
        )


@app.route("/card/new/submit", methods=["GET", "POST"])
def add_card():
    "Adds inputted card to database"
    now = time.time()
    con = sqlite3.connect(flashcards_db)
    con.execute(
        """
                INSERT INTO flashcards (card_front,card_back,deck,owner,created_ts,updated_ts)
                VALUES (?,?,?,?,?,?);
                """,
        [
            request.values.get("card_front"),
            request.values.get("card_back"),
            request.values.get("deck"),
            request.values.get("owner"),
            now,
            now,
        ],
    )
    con.commit()
    con.close()

    return redirect("/card/new/", code=302)


@app.route("/deck/new/")
def add_deck_form():
    "Display the form to create a new deck"
    global USERNAME
    username_home = USERNAME
    return render_template(
        "add_deck.html",
        username_home = username_home,
        )


@app.route("/deck/new/submit", methods=["GET", "POST"])
def add_deck():
    "Adds inputted deck to database"
    now = time.time()
    deck_name = request.values.get("deck")
    owner_name = request.values.get("owner")
    con = sqlite3.connect(flashcards_db)
    con.execute(
        """
                INSERT INTO flashcards (card_front,card_back,deck,owner,created_ts,updated_ts)
                VALUES (?,?,?,?,?,?);
                """,
        [
            deck_name,
            deck_name,
            deck_name,
            owner_name,
            now,
            now,
        ],
    )   # when user creates new deck, front and back of card are the deck name by default
    con.commit()
    con.close()
    return redirect("/deck/new/", code=302)


@app.route("/study/<deck>/")
def study_deck(deck):
    "Page for user to study chosen deck"
    global USERNAME
    username_home = USERNAME
    con = sqlite3.connect(flashcards_db)

    get_user_cards = con.execute(
        """
        SELECT cardid, card_front, card_back, card_status, deck_status, updated_ts
        FROM flashcards
        WHERE deck=?
        ORDER BY updated_ts DESC;
        """,
        [deck],
    )
    user_cards = {deck: []}
    for row in get_user_cards:
        user_cards[deck].append(
            {
                "cardid": row[0],
                "card_front": row[1],
                "card_back": row[2],
                "card_status": row[3],
                "deck_status": row[4],
                "updated_ts": row[5],
            }
        )

    return render_template(
        "study.html",
        deck=deck,
        user_cards=user_cards,
        username_home = username_home
    )

# The next function implements the try/except/finally code route that checks if the user already 
# has an active database or creates a new one if not and is adapted from 'TaskGain' by David Dumas
try:    #attempt to open database
    main_con = sqlite3.connect(flashcards_db)
    main_con.execute("SELECT COUNT(*) FROM flashcards;")
    print("Opening Database...")
except sqlite3.OperationalError:    #if database not found, create new one
    print("Database not found, creating database...")
    main_con.execute("DROP TABLE IF EXISTS flashcards;")
    main_con.execute(
        """
        CREATE TABLE flashcards (
            cardid INTEGER PRIMARY KEY,
            owner TEXT NOT NULL,
            card_front TEXT NOT NULL,
            card_back TEXT,
            card_status INTEGER DEFAULT 0,
            deck TEXT NOT NULL,
            deck_status INTEGER DEFAULT 0,
            created_ts REAL NOT NULL,
            updated_ts REAL NOT NULL
        );"""
    )

    main_con.commit()
finally:
    main_con.close()

app.run()

