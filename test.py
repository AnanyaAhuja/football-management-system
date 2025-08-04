import mysql.connector
from main_project import register_user, login_user, add_team, record_match_stats, predict_match

# MAKE CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ananya5*",
    database="FootballDB"
)

print("Registering new user")
register_user(db, "ananya_demo", "hello123")

print("Logging in user")
user_id = login_user(db, "ananya_demo", "hello123")

if user_id:
    

    print("Adding a team")
    add_team(db, "Barcelona", "Xavi")

    print("Recording match stats")
    record_match_stats(db, 1, 3, 5, 68.4)

    print("Making prediction")
    predict_match(db, user_id, 1, "Barcelona")
else:
    print("Login failed.")
