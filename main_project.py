import mysql.connector
from mysql.connector import Error
import bcrypt

# CONNECT DATABASE
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ananya5*',
            database='FootballDB'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# MAKE TABLES
def create_tables(connection):
    cursor = connection.cursor()

    queries = [
        """
        CREATE TABLE IF NOT EXISTS Users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Team (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            coach VARCHAR(255)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS MatchStats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            team_id INT,
            goals_scored INT,
            fouls INT,
            possession FLOAT,
            FOREIGN KEY (team_id) REFERENCES Team(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Prediction (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            match_id INT,
            predicted_winner VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (match_id) REFERENCES MatchStats(id)
        );
        """
    ]

    for query in queries:
        cursor.execute(query)

    connection.commit()
    print("All tables created successfully.")

# FUNCTIONS
def register_user(connection, username, password):
    cursor = connection.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO Users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()
        print("User registered successfully.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def login_user(connection, username, password):
    cursor = connection.cursor()
    cursor.execute("SELECT id, password_hash FROM Users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
        print("Login successful.")
        return result[0]
    else:
        print("Invalid credentials.")
        return None

def add_team(connection, team_name, coach_name):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Team (name, coach) VALUES (%s, %s)", (team_name, coach_name))
    connection.commit()
    print("Team added successfully.")

def record_match_stats(connection, team_id, goals, fouls, possession):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO MatchStats (team_id, goals_scored, fouls, possession)
        VALUES (%s, %s, %s, %s)
    """, (team_id, goals, fouls, possession))
    connection.commit()
    print("Match stats recorded successfully.")

def predict_match(connection, user_id, match_id, predicted_winner):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Prediction (user_id, match_id, predicted_winner)
        VALUES (%s, %s, %s)
    """, (user_id, match_id, predicted_winner))
    connection.commit()
    print("Prediction recorded.")

# MENU
def main():
    connection = connect_to_db()
    if not connection:
        return

    create_tables(connection)
    user_id = None

    while True:
        print("\n FOOTBALL MANAGEMENT SYSTEM!!!")
        print("1. Register")
        print("2. Login")
        print("3. Add Team")
        print("4. Record Match Stats")
        print("5. Predict Match Outcome")
        print("6. Exit")

        choice = input("Enter your choice (1–6): ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(connection, username, password)

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_id = login_user(connection, username, password)

        elif choice == '3':
            if user_id:
                team_name = input("Enter team name: ")
                coach_name = input("Enter coach name: ")
                add_team(connection, team_name, coach_name)
            else:
                print("Please login first.")

        elif choice == '4':
            if user_id:
                team_id = int(input("Enter team ID: "))
                goals = int(input("Goals scored: "))
                fouls = int(input("Number of fouls: "))
                possession = float(input("Possession (%): "))
                record_match_stats(connection, team_id, goals, fouls, possession)
            else:
                print("Please login first.")

        elif choice == '5':
            if user_id:
                match_id = int(input("Enter match ID: "))
                predicted_winner = input("Enter predicted winner team name: ")
                predict_match(connection, user_id, match_id, predicted_winner)
            else:
                print("Please login first.")

        elif choice == '6':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

