import mysql.connector
from faker import Faker
import time
import random
from dotenv import load_dotenv
load_dotenv()
import os

database_name = os.getenv("MYSQL_DATABASE")
database_username = os.getenv("MYSQL_USER")
database_password = os.getenv("MYSQL_PASSWORD")

# Initialize Faker for generating random names
fake = Faker()

# Database connection configuration
db_config = {
    "host": "localhost",  
    "user": database_username,
    "password": database_password,
    "database": database_name
}


def get_random_student_id(cursor):
    """Fetch a random student ID from the students table."""
    cursor.execute("SELECT id FROM students ORDER BY RAND() LIMIT 1")
    result = cursor.fetchone()
    return result[0] if result else None


def delete_student(cursor, conn):
    """Randomly delete a student from the database."""
    student_id = get_random_student_id(cursor)
    if student_id:
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        print(f"Deleted student with ID: {student_id}")
    else:
        print("No students found to delete.")

def insert_student(cursor, conn):
    """Insert a new random student into the database."""
    first_name = fake.first_name()
    last_name = fake.last_name()
    score = random.randint(50, 100)  # Random score between 50 and 100
    cursor.execute("INSERT INTO students (first_name, last_name, score) VALUES (%s, %s, %s)", 
                   (first_name, last_name, score))
    conn.commit()
    print(f"Inserted new student: {first_name} {last_name} with score {score}")

def update_student(cursor, conn):
    """Update the score of a random student."""
    student_id = get_random_student_id(cursor)
    if student_id:
        new_score = random.randint(50, 100)
        cursor.execute("UPDATE students SET score = %s WHERE id = %s", (new_score, student_id))
        conn.commit()
        print(f"Updated student ID {student_id} with new score {new_score}")
    else:
        print("No students found to update.")

def perform_random_action():
    """Randomly select and execute an action every 2 minutes."""
    actions = [delete_student, insert_student, update_student]
    
    while True:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            action = random.choice(actions)
            action(cursor, conn)
            
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        
        print("Waiting for 2 minutes...")
        time.sleep(120)  # Wait for 2 minutes

if __name__ == "__main__":
    perform_random_action()