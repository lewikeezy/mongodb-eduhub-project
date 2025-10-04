# ---Part 1: Database Setup and Data Modeling
#importing neccsary libraries
from pymongo import MongoClient
from datetime import datetime, timedelta, UTC
import pandas as pd

# Establish MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

# Create or access the database
db = client["eduhub_db"]

# Create collections with validation rules

# Students collection schema
students_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["student_id", "name", "email", "enrollment_date"],
        "properties": {
            "student_id": {"bsonType": "string", "description": "Unique student ID"},
            "name": {"bsonType": "string", "description": "Full name of the student"},
            "email": {"bsonType": "string", "pattern": "^.+@.+$", "description": "Valid email address"},
            "enrollment_date": {"bsonType": "date", "description": "Date of enrollment"},
            "courses": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
                "description": "List of enrolled course IDs"
            }
        }
    }
}

# Courses collection schema
courses_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["course_id", "title", "instructor"],
        "properties": {
            "course_id": {"bsonType": "string", "description": "Unique course ID"},
            "title": {"bsonType": "string", "description": "Course title"},
            "instructor": {"bsonType": "string", "description": "Instructor name"},
            "credits": {"bsonType": "int", "minimum": 1, "maximum": 10, "description": "Credit hours"}
        }
    }
}

# Instructors collection schema
instructors_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["instructor_id", "name", "email"],
        "properties": {
            "instructor_id": {"bsonType": "string", "description": "Unique instructor ID"},
            "name": {"bsonType": "string", "description": "Instructor full name"},
            "email": {"bsonType": "string", "pattern": "^.+@.+$", "description": "Valid email"},
            "department": {"bsonType": "string", "description": "Department name"}
        }
    }
}


# Drop old collections if exist (to prevent errors during re-run)

db.drop_collection("students")
db.drop_collection("courses")
db.drop_collection("instructors")


# Create collections with validators

db.create_collection("students", validator=students_validator)
db.create_collection("courses", validator=courses_validator)
db.create_collection("instructors", validator=instructors_validator)

print("successfully created Database 'eduhub_db' and collections with validation rules.")


##---Part 2: Data Population--
# Import libraries
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta, UTC
import random

# Connection to MongoDB
MONGO_URI = "mongodb://localhost:27017/"
try:
    client = MongoClient(MONGO_URI)
    # The 'ping' command is to check the connection status
    client.admin.command('ping')
    print("Connection to MongoDB successful! You're ready to go.")
except ConnectionFailure as e:
    print(f"Connection failed: {e}")
    print(f"Please ensure your MongoDB server is running and accessible at {MONGO_URI}")
    exit()

# Get the 'eduhub_db' database and collections from the previous part at the initial insertions
db = client['eduhub_db']
users_collection = db['users']
courses_collection = db['courses']
enrollments_collection = db['enrollments']
lessons_collection = db['lessons']
assignments_collection = db['assignments']
submissions_collection = db['submissions']


#Drop the 'users' collection before insertion to clear old data and prevent duplicate Key errors
users_collection.drop()

print("Database 'eduhub_db' and all collections are set up.")
print("********************************************")


# 2.1 Insert 20 users (15 students, 5 instructors) 
print("Inserting 20 users in progress")

# Sample data contianing names of instructors and studeents
name_pairs = [
    ("Tolu", "Akinola"), ("Chukwudi", "Dike"), ("Femi", "Ojo"), ("Chidi", "Okoye"), ("Emeka", "Nwachukwu"),
    ("Ayomide", "Adewale"), ("Ijeoma", "Okafor"), ("Folake", "Ogunleye"), ("Chioma", "Nwankwo"), ("Zainab", "Umar"),
    ("Halima", "Ibrahim"), ("Aisha", "Bello"), ("Musa", "Abdullahi"), ("Abubakar", "Suleiman"), ("Segun", "Adeyemi"),
    ("Obinna", "Adebayo"), ("Tunde", "Yusuf"), ("Ifeyinwa", "Eke"), ("Sani", "Usman"), ("Bode", "Musa")
]

users_to_insert = []
instructor_ids = []
student_ids = []

for i in range(20):
    role = 'instructor' if i < 5 else 'student'
    
    # Get the name pair from the list using the loop index
    first_name, last_name = name_pairs[i]
    
    user_doc = {
        "userId": f"user_{i+1}",
        "email": f"{first_name.lower()}{last_name.lower()}{i+1}@eduhub.com",
        "firstName": first_name,
        "lastName": last_name,
        "role": role,
        "dateJoined": datetime.now(UTC) - timedelta(days=random.randint(1, 365)),
        "profile": {
            "bio": f"A dedicated {role} on EduHub.",
            "avatar": f"https://example.com/avatars/{i+1}.jpg",
            "skills": ["Python", "MongoDB", "Data Analysis"] if role == 'instructor' else ["Learning"]
        },
        "isActive": True
    }
    users_to_insert.append(user_doc)
    if role == 'instructor':
        instructor_ids.append(user_doc['userId'])
    else:
        student_ids.append(user_doc['userId'])

# Inserting sample data into users collection
users_collection.insert_many(users_to_insert)
print(f" Successfully Inserted {len(users_to_insert)} users.")


#2.2 Insert 8 courses
print("Inserting 8 courses in progress")
courses_to_insert = []
course_ids = []
course_categories = ["Programming", "Design", "Business", "Marketing", "Art", "Science"]
course_titles = [
    "Introduction to Python", "Data Science with Pandas", "UI/UX Design Fundamentals",
    "Digital Marketing Strategies", "Foundations of Art History", "Organic Chemistry",
    "Web Development with MongoDB", "Project Management Basics"
]

for i in range(8):
    course_id = f"course_{i+1}"
    instructor_id = random.choice(instructor_ids)
    course_doc = {
        "course_id": course_id,
        "title": course_titles[i],
        "description": f"A comprehensive course on {course_titles[i]}.",
        "instructor": instructor_id,  #picking a user as an instructor
        "category": random.choice(course_categories),
        "level": random.choice(['beginner', 'intermediate', 'advanced']),
        "duration": random.randint(10, 60),
        "price": random.randint(50, 200),
        "tags": ["online", "2025"],
        "createdAt": datetime.now(UTC),
        "updatedAt": datetime.now(UTC),
        "isPublished": True
    }
    courses_to_insert.append(course_doc)
    course_ids.append(course_id)

courses_collection.insert_many(courses_to_insert)
print(f"{len(courses_to_insert)} courses inserted.")

#2.3 Insert 15 enrollments 
print("Inserting 15 enrollments in progrss")
enrollments_to_insert = []
for i in range(15):
    enrollment_doc = {
        "enrollmentId": f"enrollment_{i+1}",
        "studentId": random.choice(student_ids),  # picking a student user
        "": random.choice(course_ids),    # picking a course
        "enrollmentDate": datetime.now(UTC) - timedelta(days=random.randint(1, 100)),
        "progress": random.uniform(0, 100),
        "status": random.choice(['in-progress', 'completed', 'dropped'])
    }
    enrollments_to_insert.append(enrollment_doc)

enrollments_collection.insert_many(enrollments_to_insert)
print(f"Inserted {len(enrollments_to_insert)} enrollments.")

# 2.4 Insert 25 lessons
print("Inserting 25 lessons in progress")
lessons_to_insert = []
for i in range(25):
    lesson_doc = {
        "lessonId": f"lesson_{i+1}",
        "course_id": random.choice(course_ids),  #picking a course
        "title": f"Lesson {i+1} Title",
        "content": f"Content for lesson {i+1}.",
        "videoUrl": "https://example.com/videos/lesson.mp4",
        "durationMinutes": random.randint(5, 30),
        "order": i + 1,
        "createdAt": datetime.now(UTC)
    }
    lessons_to_insert.append(lesson_doc)

lessons_collection.insert_many(lessons_to_insert)
print(f"Inserted {len(lessons_to_insert)} lessons.")

#2.5 Insert 10 assignments
print("Inserting 10 assignments in progress")
assignments_to_insert = []
assignment_ids = []
for i in range(10):
    assignment_id = f"assignment_{i+1}"
    assignment_doc = {
        "assignmentId": assignment_id,
        "course_id": random.choice(course_ids),  #picking a course
        "title": f"Assignment {i+1} Title",
        "description": f"Description for assignment {i+1}.",
        "dueDate": datetime.now(UTC) + timedelta(days=random.randint(7, 30)),
        "maxScore": 100,
        "createdAt": datetime.now(UTC)
    }
    assignments_to_insert.append(assignment_doc)
    assignment_ids.append(assignment_id)

assignments_collection.insert_many(assignments_to_insert)
print(f"Inserted {len(assignments_to_insert)} assignments.")

# 2.6 Insert 12 assignment submissions
print("Inserting 12 assignment submissions in progress")
submissions_to_insert = []
for i in range(12):
    submission_doc = {
        "submissionId": f"submission_{i+1}",
        "assignmentId": random.choice(assignment_ids),  #picking an assignment
        "studentId": random.choice(student_ids),        # picking a student user
        "submittedAt": datetime.now(UTC) - timedelta(hours=random.randint(1, 24)),
        "submissionUrl": "https://github.com/my-submission",
        "grade": random.randint(50, 100),
        "feedback": "Great work!"
    }
    submissions_to_insert.append(submission_doc)

submissions_collection.insert_many(submissions_to_insert)
print(f"Inserted {len(submissions_to_insert)} assignment submissions.")

# Import libraries
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta, UTC
import random

# Connection to MongoDB
MONGO_URI = "mongodb://localhost:27017/"
try:
    client = MongoClient(MONGO_URI)
    # The 'ping' command is to check the connection status
    client.admin.command('ping')
    print("Connection to MongoDB successful! You're ready to go.")
except ConnectionFailure as e:
    print(f"Connection failed: {e}")
    print(f"Please ensure your MongoDB server is running and accessible at {MONGO_URI}")
    exit()

# Get the 'eduhub_db' database and collections from the previous part at the initial insertions
db = client['eduhub_db']
users_collection = db['users']
courses_collection = db['courses']
enrollments_collection = db['enrollments']
lessons_collection = db['lessons']
assignments_collection = db['assignments']
submissions_collection = db['submissions']

print("Database 'eduhub_db' and all collections are set up.")
print("********************************************")


# 2.1 Insert 20 users (15 students, 5 instructors) 
print("Inserting 20 users in progress")

# Sample data contianing names of instructors and studeents
name_pairs = [
    ("Tolu", "Akinola"), ("Chukwudi", "Dike"), ("Femi", "Ojo"), ("Chidi", "Okoye"), ("Emeka", "Nwachukwu"),
    ("Ayomide", "Adewale"), ("Ijeoma", "Okafor"), ("Folake", "Ogunleye"), ("Chioma", "Nwankwo"), ("Zainab", "Umar"),
    ("Halima", "Ibrahim"), ("Aisha", "Bello"), ("Musa", "Abdullahi"), ("Abubakar", "Suleiman"), ("Segun", "Adeyemi"),
    ("Obinna", "Adebayo"), ("Tunde", "Yusuf"), ("Ifeyinwa", "Eke"), ("Sani", "Usman"), ("Bode", "Musa")
]

users_to_insert = []
instructor_ids = []
student_ids = []

for i in range(20):
    role = 'instructor' if i < 5 else 'student'
    
    # Get the name pair from the list using the loop index
    first_name, last_name = name_pairs[i]
    
    user_doc = {
        "userId": f"user_{i+1}",
        "email": f"{first_name.lower()}{last_name.lower()}{i+1}@eduhub.com",
        "firstName": first_name,
        "lastName": last_name,
        "role": role,
        "dateJoined": datetime.now(UTC) - timedelta(days=random.randint(1, 365)),
        "profile": {
            "bio": f"A dedicated {role} on EduHub.",
            "avatar": f"https://example.com/avatars/{i+1}.jpg",
            "skills": ["Python", "MongoDB", "Data Analysis"] if role == 'instructor' else ["Learning"]
        },
        "isActive": True
    }
    users_to_insert.append(user_doc)
    if role == 'instructor':
        instructor_ids.append(user_doc['userId'])
    else:
        student_ids.append(user_doc['userId'])

# Inserting sample data into users collection
users_collection.insert_many(users_to_insert)
print(f" Successfully Inserted {len(users_to_insert)} users.")


#2.2 Insert 8 courses
print("Inserting 8 courses in progress")
courses_to_insert = []
course_ids = []
course_categories = ["Programming", "Design", "Business", "Marketing", "Art", "Science"]
course_titles = [
    "Introduction to Python", "Data Science with Pandas", "UI/UX Design Fundamentals",
    "Digital Marketing Strategies", "Foundations of Art History", "Organic Chemistry",
    "Web Development with MongoDB", "Project Management Basics"
]

for i in range(8):
    course_id = f"course_{i+1}"
    instructor_id = random.choice(instructor_ids)
    course_doc = {
        "course_id": course_id,
        "title": course_titles[i],
        "description": f"A comprehensive course on {course_titles[i]}.",
        "instructor": instructor_id,  #picking a user as an instructor
        "category": random.choice(course_categories),
        "level": random.choice(['beginner', 'intermediate', 'advanced']),
        "duration": random.randint(10, 60),
        "price": random.randint(50, 200),
        "tags": ["online", "2025"],
        "createdAt": datetime.now(UTC),
        "updatedAt": datetime.now(UTC),
        "isPublished": True
    }
    courses_to_insert.append(course_doc)
    course_ids.append(course_id)

courses_collection.insert_many(courses_to_insert)
print(f"{len(courses_to_insert)} courses inserted.")

#2.3 Insert 15 enrollments 
print("Inserting 15 enrollments in progrss")
enrollments_to_insert = []
for i in range(15):
    enrollment_doc = {
        "enrollmentId": f"enrollment_{i+1}",
        "studentId": random.choice(student_ids),  # picking a student user
        "": random.choice(course_ids),    # picking a course
        "enrollmentDate": datetime.now(UTC) - timedelta(days=random.randint(1, 100)),
        "progress": random.uniform(0, 100),
        "status": random.choice(['in-progress', 'completed', 'dropped'])
    }
    enrollments_to_insert.append(enrollment_doc)

enrollments_collection.insert_many(enrollments_to_insert)
print(f"Inserted {len(enrollments_to_insert)} enrollments.")

# 2.4 Insert 25 lessons
print("Inserting 25 lessons in progress")
lessons_to_insert = []
for i in range(25):
    lesson_doc = {
        "lessonId": f"lesson_{i+1}",
        "course_id": random.choice(course_ids),  #picking a course
        "title": f"Lesson {i+1} Title",
        "content": f"Content for lesson {i+1}.",
        "videoUrl": "https://example.com/videos/lesson.mp4",
        "durationMinutes": random.randint(5, 30),
        "order": i + 1,
        "createdAt": datetime.now(UTC)
    }
    lessons_to_insert.append(lesson_doc)

lessons_collection.insert_many(lessons_to_insert)
print(f"Inserted {len(lessons_to_insert)} lessons.")

#2.5 Insert 10 assignments
print("Inserting 10 assignments in progress")
assignments_to_insert = []
assignment_ids = []
for i in range(10):
    assignment_id = f"assignment_{i+1}"
    assignment_doc = {
        "assignmentId": assignment_id,
        "course_id": random.choice(course_ids),  #picking a course
        "title": f"Assignment {i+1} Title",
        "description": f"Description for assignment {i+1}.",
        "dueDate": datetime.now(UTC) + timedelta(days=random.randint(7, 30)),
        "maxScore": 100,
        "createdAt": datetime.now(UTC)
    }
    assignments_to_insert.append(assignment_doc)
    assignment_ids.append(assignment_id)

assignments_collection.insert_many(assignments_to_insert)
print(f"Inserted {len(assignments_to_insert)} assignments.")

# 2.6 Insert 12 assignment submissions
print("Inserting 12 assignment submissions in progress")
submissions_to_insert = []
for i in range(12):
    submission_doc = {
        "submissionId": f"submission_{i+1}",
        "assignmentId": random.choice(assignment_ids),  #picking an assignment
        "studentId": random.choice(student_ids),        # picking a student user
        "submittedAt": datetime.now(UTC) - timedelta(hours=random.randint(1, 24)),
        "submissionUrl": "https://github.com/my-submission",
        "grade": random.randint(50, 100),
        "feedback": "Great work!"
    }
    submissions_to_insert.append(submission_doc)

submissions_collection.insert_many(submissions_to_insert)
print(f"Inserted {len(submissions_to_insert)} assignment submissions.")

print("\n All sample data has been successfully inserted with no errors.")


# Import libraries
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta, UTC
import random

# Connection to MongoDB
MONGO_URI = "mongodb://localhost:27017/"
try:
    client = MongoClient(MONGO_URI)
    # The 'ping' command is to check the connection status
    client.admin.command('ping')
    print("Connection to MongoDB successful! You're ready to go.")
except ConnectionFailure as e:
    print(f"Connection failed: {e}")
    print(f"Please ensure your MongoDB server is running and accessible at {MONGO_URI}")
    exit()

# Get the 'eduhub_db' database and collections from the previous part at the initial insertions
db = client['eduhub_db']
users_collection = db['users']
courses_collection = db['courses']
enrollments_collection = db['enrollments']
lessons_collection = db['lessons']
assignments_collection = db['assignments']
submissions_collection = db['submissions']

print("Database 'eduhub_db' and all collections are set up.")
print("********************************************")


# 2.1 Insert 20 users (15 students, 5 instructors) 
print("Inserting 20 users in progress")

# Sample data contianing names of instructors and studeents
name_pairs = [
    ("Tolu", "Akinola"), ("Chukwudi", "Dike"), ("Femi", "Ojo"), ("Chidi", "Okoye"), ("Emeka", "Nwachukwu"),
    ("Ayomide", "Adewale"), ("Ijeoma", "Okafor"), ("Folake", "Ogunleye"), ("Chioma", "Nwankwo"), ("Zainab", "Umar"),
    ("Halima", "Ibrahim"), ("Aisha", "Bello"), ("Musa", "Abdullahi"), ("Abubakar", "Suleiman"), ("Segun", "Adeyemi"),
    ("Obinna", "Adebayo"), ("Tunde", "Yusuf"), ("Ifeyinwa", "Eke"), ("Sani", "Usman"), ("Bode", "Musa")
]

users_to_insert = []
instructor_ids = []
student_ids = []

for i in range(20):
    role = 'instructor' if i < 5 else 'student'
    
    # Get the name pair from the list using the loop index
    first_name, last_name = name_pairs[i]
    
    user_doc = {
        "userId": f"user_{i+1}",
        "email": f"{first_name.lower()}{last_name.lower()}{i+1}@eduhub.com",
        "firstName": first_name,
        "lastName": last_name,
        "role": role,
        "dateJoined": datetime.now(UTC) - timedelta(days=random.randint(1, 365)),
        "profile": {
            "bio": f"A dedicated {role} on EduHub.",
            "avatar": f"https://example.com/avatars/{i+1}.jpg",
            "skills": ["Python", "MongoDB", "Data Analysis"] if role == 'instructor' else ["Learning"]
        },
        "isActive": True
    }
    users_to_insert.append(user_doc)
    if role == 'instructor':
        instructor_ids.append(user_doc['userId'])
    else:
        student_ids.append(user_doc['userId'])

# Inserting sample data into users collection
users_collection.insert_many(users_to_insert)
print(f" Successfully Inserted {len(users_to_insert)} users.")


#2.2 Insert 8 courses
print("Inserting 8 courses in progress")
courses_to_insert = []
course_ids = []
course_categories = ["Programming", "Design", "Business", "Marketing", "Art", "Science"]
course_titles = [
    "Introduction to Python", "Data Science with Pandas", "UI/UX Design Fundamentals",
    "Digital Marketing Strategies", "Foundations of Art History", "Organic Chemistry",
    "Web Development with MongoDB", "Project Management Basics"
]

for i in range(8):
    course_id = f"course_{i+1}"
    instructor_id = random.choice(instructor_ids)
    course_doc = {
        "course_id": course_id,
        "title": course_titles[i],
        "description": f"A comprehensive course on {course_titles[i]}.",
        "instructor": instructor_id,  #picking a user as an instructor
        "category": random.choice(course_categories),
        "level": random.choice(['beginner', 'intermediate', 'advanced']),
        "duration": random.randint(10, 60),
        "price": random.randint(50, 200),
        "tags": ["online", "2025"],
        "createdAt": datetime.now(UTC),
        "updatedAt": datetime.now(UTC),
        "isPublished": True
    }
    courses_to_insert.append(course_doc)
    course_ids.append(course_id)

courses_collection.insert_many(courses_to_insert)
print(f"{len(courses_to_insert)} courses inserted.")

#2.3 Insert 15 enrollments 
print("Inserting 15 enrollments in progrss")
enrollments_to_insert = []
for i in range(15):
    enrollment_doc = {
        "enrollmentId": f"enrollment_{i+1}",
        "studentId": random.choice(student_ids),  # picking a student user
        "": random.choice(course_ids),    # picking a course
        "enrollmentDate": datetime.now(UTC) - timedelta(days=random.randint(1, 100)),
        "progress": random.uniform(0, 100),
        "status": random.choice(['in-progress', 'completed', 'dropped'])
    }
    enrollments_to_insert.append(enrollment_doc)

enrollments_collection.insert_many(enrollments_to_insert)
print(f"Inserted {len(enrollments_to_insert)} enrollments.")

# 2.4 Insert 25 lessons
print("Inserting 25 lessons in progress")
lessons_to_insert = []
for i in range(25):
    lesson_doc = {
        "lessonId": f"lesson_{i+1}",
        "course_id": random.choice(course_ids),  #picking a course
        "title": f"Lesson {i+1} Title",
        "content": f"Content for lesson {i+1}.",
        "videoUrl": "https://example.com/videos/lesson.mp4",
        "durationMinutes": random.randint(5, 30),
        "order": i + 1,
        "createdAt": datetime.now(UTC)
    }
    lessons_to_insert.append(lesson_doc)

lessons_collection.insert_many(lessons_to_insert)
print(f"Inserted {len(lessons_to_insert)} lessons.")

#2.5 Insert 10 assignments
print("Inserting 10 assignments in progress")
assignments_to_insert = []
assignment_ids = []
for i in range(10):
    assignment_id = f"assignment_{i+1}"
    assignment_doc = {
        "assignmentId": assignment_id,
        "course_id": random.choice(course_ids),  #picking a course
        "title": f"Assignment {i+1} Title",
        "description": f"Description for assignment {i+1}.",
        "dueDate": datetime.now(UTC) + timedelta(days=random.randint(7, 30)),
        "maxScore": 100,
        "createdAt": datetime.now(UTC)
    }
    assignments_to_insert.append(assignment_doc)
    assignment_ids.append(assignment_id)

assignments_collection.insert_many(assignments_to_insert)
print(f"Inserted {len(assignments_to_insert)} assignments.")

# 2.6 Insert 12 assignment submissions
print("Inserting 12 assignment submissions in progress")
submissions_to_insert = []
for i in range(12):
    submission_doc = {
        "submissionId": f"submission_{i+1}",
        "assignmentId": random.choice(assignment_ids),  #picking an assignment
        "studentId": random.choice(student_ids),        # picking a student user
        "submittedAt": datetime.now(UTC) - timedelta(hours=random.randint(1, 24)),
        "submissionUrl": "https://github.com/my-submission",
        "grade": random.randint(50, 100),
        "feedback": "Great work!"
    }
    submissions_to_insert.append(submission_doc)

submissions_collection.insert_many(submissions_to_insert)
print(f"Inserted {len(submissions_to_insert)} assignment submissions.")

print("\n All sample data has been successfully inserted with no errors.")

# ---Part 3: CRUD Operations and Queries---
#importing libraries
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

#Configuration Details
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
DATABASE_NAME = "lms_platform"

def get_database():
    """Establishes connection to MongoDB and returns the database object."""
    try:
        client = MongoClient(MONGO_CONNECTION_STRING)
        # Ping the server to check connection
        client.admin.command('ping')
        print(f"Connection successful to database: {DATABASE_NAME}")
        return client[DATABASE_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

#Functions for setting up collctions and inital data

def setup_collections(db):
    """Clears collections and sets up initial dummy data for testing."""
    db.users.drop()
    db.courses.drop()
    db.enrollments.drop()

    print("\n--- Setting up initial data ---")

    #Creating initlal instructor
    instructor_doc = {
        "username": "Dr. Smith",
        "email": "smith@edu.com",
        "role": "instructor",
        "isActive": True,
        "profile": {"office_hours": "Tues/Thurs 1-3 PM"}
    }
    instructor_id = db.users.insert_one(instructor_doc).inserted_id
    print(f"Created Instructor (ID: {instructor_id})")

    #Creaating inital student
    student_doc = {
        "username": "Alice_Initial",
        "email": "alice@student.com",
        "role": "student",
        "isActive": True,
        "profile": {"major": "Computer Science"}
    }
    student_id = db.users.insert_one(student_doc).inserted_id
    print(f"Created Initial Student (ID: {student_id})")

    #Creating initial course
    course_doc = {
        "title": "Introduction to PyMongo",
        "instructorId": instructor_id,
        "category": "Programming",
        "isPublished": False, 
        "lessons": [
            {"lessonId": ObjectId(), "title": "Connecting to MongoDB", "content": "Code for MongoClient."},
            {"lessonId": ObjectId(), "title": "Inserting Documents", "content": "Using insert_one and insert_many."}
        ],
        "tags": ["NoSQL", "Database"]
    }
    course_id = db.courses.insert_one(course_doc).inserted_id
    print(f"Created Initial Course (ID: {course_id})")

    #Creating initial student enrollemrnt
    enrollment_doc = {
        "studentId": student_id,
        "courseId": course_id,
        "grades": [
            {"assignmentName": "Quiz 1", "score": 85},
            {"assignmentName": "Project Draft", "score": 92}
        ]
    }
    enrollment_id = db.enrollments.insert_one(enrollment_doc).inserted_id
    print(f"Created Initial Enrollment (ID: {enrollment_id})\n")

    return instructor_id, student_id, course_id, enrollment_id



#3.1: Create Operations

def add_new_student(db, username, email):
    """Adds a new student user to the 'users' collection."""
    student_doc = {
        "username": username,
        "email": email,
        "role": "student",
        "isActive": True,
        "profile": {}
    }
    result = db.users.insert_one(student_doc)
    print(f"  [CREATE] New student '{username}' added. ID: {result.inserted_id}")
    return result.inserted_id

def create_new_course(db, title, instructor_id, category):
    """Creates a new course in the 'courses' collection."""
    course_doc = {
        "title": title,
        "instructorId": ObjectId(instructor_id),
        "category": category,
        "isPublished": False,
        "lessons": [],
        "tags": []
    }
    result = db.courses.insert_one(course_doc)
    print(f"  [CREATE] New course '{title}' created. ID: {result.inserted_id}")
    return result.inserted_id

def enroll_student_in_course(db, student_id, course_id):
    """Enroll a student in a course by creating a document in 'enrollments'."""
    enrollment_doc = {
        "studentId": ObjectId(student_id),
        "courseId": ObjectId(course_id),
        "grades": []
    }
    # Check for existing course enrollment to prevent duplicates or multiple enrollment by the same student
    if db.enrollments.find_one({"studentId": enrollment_doc["studentId"], "courseId": enrollment_doc["courseId"]}):
        print("  [CREATE] Student already enrolled in this course.")
        return None

    result = db.enrollments.insert_one(enrollment_doc)
    print(f"  [CREATE] Student {student_id} enrolled in course {course_id}. Enrollment ID: {result.inserted_id}")
    return result.inserted_id

def add_lesson_to_course(db, course_id, title, content):
    """Adds a new lesson object to the 'lessons' array of an existing course."""
    lesson_doc = {
        "lessonId": ObjectId(),
        "title": title,
        "content": content
    }
    result = db.courses.update_one(
        {"_id": ObjectId(course_id)},
        {"$push": {"lessons": lesson_doc}}
    )
    if result.modified_count:
        print(f"  [CREATE] Lesson '{title}' added to course {course_id}.")
    else:
        print(f"  [CREATE] Failed to find or update course {course_id}.")

        return result.modified_count


#Task 3.2: Read Operations
def find_active_students(db):
    """Finds all users with role 'student' and isActive set to True."""
    query = {"role": "student", "isActive": True}
    students = list(db.users.find(query, {"username": 1, "email": 1}))
    print(f"  [READ] Found {len(students)} active students.")
    return students

def retrieve_course_with_instructor(db, course_id):
    """Retrieves course details and joins with instructor information using aggregation."""
    pipeline = [
        {"$match": {"_id": ObjectId(course_id)}},
        {"$limit": 1},
        {"$lookup": {
            "from": "users",
            "localField": "instructorId",
            "foreignField": "_id",
            "as": "instructor_info"
        }},
        {"$unwind": {"path": "$instructor_info", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "title": 1,
            "category": 1,
            "isPublished": 1,
            "instructor_name": "$instructor_info.username",
            "instructor_email": "$instructor_info.email"
        }}
    ]
    course = list(db.courses.aggregate(pipeline))
    if course:
        print(f"  [READ] Course '{course[0]['title']}' retrieved with instructor info.")
        return course[0]
    return None

def get_courses_by_category(db, category):
    """Gets all courses belonging to a specific category."""
    query = {"category": category}
    courses = list(db.courses.find(query, {"title": 1, "category": 1}))
    print(f"  [READ] Found {len(courses)} courses in category '{category}'.")
    return courses

def find_students_in_course(db, course_id):
    """Finds all students enrolled in a particular course using a two-step lookup/join."""
    pipeline = [
        {"$match": {"courseId": ObjectId(course_id)}},
        {"$lookup": {
            "from": "users",
            "localField": "studentId",
            "foreignField": "_id",
            "as": "student_details"
        }},
        {"$unwind": "$student_details"},
        {"$project": {
            "_id": "$student_details._id",
            "username": "$student_details.username",
            "email": "$student_details.email"
        }}
    ]
    students = list(db.enrollments.aggregate(pipeline))
    print(f"  [READ] Found {len(students)} students enrolled in course {course_id}.")
    return students

def search_courses_by_title(db, search_term):
    """Searches courses by title (case-insensitive, partial match) using regex."""
    query = {"title": {"$regex": search_term, "$options": "i"}}
    courses = list(db.courses.find(query, {"title": 1, "category": 1}))
    print(f"  [READ] Found {len(courses)} courses matching title search '{search_term}'.")
    return courses


#Task3.3: Update Operations

def update_user_profile(db, user_id, updates):
    """Updates selected fields within a user's profile object."""
    result = db.users.update_one(
        {"_id": ObjectId(user_id)},
        
        # Use $set for nested field updates
        {"$set": {f"profile.{k}": v for k, v in updates.items()}} 
    )
    if result.modified_count:
        print(f"  [UPDATE] User {user_id} profile updated: {updates}")
    else:
        print(f"  [UPDATE] User {user_id} not found or no changes made.")
    return result.modified_count

def mark_course_published(db, course_id):
    """Marks a course as published (sets isPublished to True)."""
    result = db.courses.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": {"isPublished": True}}
    )
    if result.modified_count:
        print(f"  [UPDATE] Course {course_id} marked as published.")
    else:
        print(f"  [UPDATE] Course {course_id} not found or already published.")
    return result.modified_count

def update_assignment_grade(db, enrollment_id, assignment_name, new_score):
    """Updates the score of a specific assignment within an enrollment's grades array."""
    result = db.enrollments.update_one(
        {"_id": ObjectId(enrollment_id), "grades.assignmentName": assignment_name},
        {"$set": {"grades.$.score": new_score}} 
    )
    if result.modified_count:
        print(f"  [UPDATE] Enrollment {enrollment_id}: Grade for '{assignment_name}' updated to {new_score}.")
    else:
        print(f"  [UPDATE] Enrollment {enrollment_id}: Grade for '{assignment_name}' not found or no change made.")
    return result.modified_count

def add_tags_to_course(db, course_id, tags_list):
    """Adds a list of tags to an existing course, ensuring no duplicates."""
    result = db.courses.update_one(
        {"_id": ObjectId(course_id)},
        # $addToSet prevents duplicates
        {"$addToSet": {"tags": {"$each": tags_list}}} 
    )
    if result.modified_count:
        print(f"  [UPDATE] Course {course_id}: Added tags {tags_list}.")
    else:
        print(f"  [UPDATE] Course {course_id} not found or tags already existed.")
    return result.modified_count


# Part 3.4: Delete Operations

def soft_delete_user(db, user_id):
    """Removes a user by soft deleting (setting isActive to false)."""
    result = db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"isActive": False}}
    )
    if result.modified_count:
        print(f"  [DELETE] User {user_id} soft deleted (isActive: False).")
    else:
        print(f"  [DELETE] User {user_id} not found or already inactive.")
    return result.modified_count

def delete_enrollment(db, enrollment_id):
    """Deletes an enrollment document completely."""
    result = db.enrollments.delete_one({"_id": ObjectId(enrollment_id)})
    if result.deleted_count:
        print(f"  [DELETE] Enrollment {enrollment_id} successfully deleted.")
    else:
        print(f"  [DELETE] Enrollment {enrollment_id} not found.")
    return result.deleted_count

def remove_lesson_from_course(db, course_id, lesson_title):
    """Removes a lesson object from the 'lessons' array of a course by title."""
    result = db.courses.update_one(
        {"_id": ObjectId(course_id)},
        #pull removes matching array elements
        {"$pull": {"lessons": {"title": lesson_title}}} 
    )
    if result.modified_count:
        print(f"  [DELETE] Lesson '{lesson_title}' removed from course {course_id}.")
    else:
        print(f"  [DELETE] Lesson '{lesson_title}' not found in course {course_id}.")
    return result.modified_count



# Main Execution Block for Testing

if __name__ == "__main__":
    db = get_database()

    if db is None:
        exit()

    # Create and get initial IDs for testing
    INSTRUCTOR_ID, INITIAL_STUDENT_ID, COURSE_ID, ENROLLMENT_ID = setup_collections(db)


    #Task 3.1: Create Operations 
    print("\n Running Task 3.1: Create Operations")
    NEW_STUDENT_ID = add_new_student(db, "Chinedu_Okafor", "chinedu@student.com")
    NEW_COURSE_ID = create_new_course(db, "Advanced Data Structures", INSTRUCTOR_ID, "Programming")
    NEW_ENROLLMENT_ID = enroll_student_in_course(db, NEW_STUDENT_ID, NEW_COURSE_ID)
    add_lesson_to_course(db, COURSE_ID, "Working with Arrays", "How MongoDB handles arrays of objects.")


    #Task 3.2: Read Operations
    print("\n Running Task 3.2: Read Operations")

    # Find all active students
    active_students = find_active_students(db)
    # print("  Active Students:", [s['username'] for s in active_students])

    # Retrieve course details with instructor information
    course_with_instr = retrieve_course_with_instructor(db, COURSE_ID)
    # print(json.dumps(course_with_instr, indent=2))

    # Get all courses in a specific category (Programming)
    programming_courses = get_courses_by_category(db, "Programming")
    # print("  Programming Course Titles:", [c['title'] for c in programming_courses])

    # Find students enrolled in a particular course (NEW_COURSE_ID)
    enrolled_students = find_students_in_course(db, NEW_COURSE_ID)
    # print("  Students in new course:", [s['username'] for s in enrolled_students])

    # Search courses by title (case-insensitive, partial match)
    search_results = search_courses_by_title(db, "data") 
    # print("  Search results:", [c['title'] for c in search_results])


    #Task 3.3: Update Operations 
    print("\n Running Task 3.3: Update Operations")

    # Update a user’s profile information (INITIAL_STUDENT_ID)
    update_user_profile(db, INITIAL_STUDENT_ID, {"major": "Software Engineering", "year": 2026})
    # Verification (Optional): print(db.users.find_one({"_id": ObjectId(INITIAL_STUDENT_ID)}, {"profile": 1}))

    # Mark a course as published (COURSE_ID)
    mark_course_published(db, COURSE_ID)

    # Update assignment grades (ENROLLMENT_ID for Alice_Initial)
    update_assignment_grade(db, ENROLLMENT_ID, "Quiz 1", 95)
    # Verification (Optional): print(db.enrollments.find_one({"_id": ObjectId(ENROLLMENT_ID)}, {"grades": 1}))

    # Add tags to an existing course (COURSE_ID)
    add_tags_to_course(db, COURSE_ID, ["Arrays", "Advanced", "Database"])


    #Task 3.4: Delete Operations
    print("\nRunning Task 3.4: Delete Operations")

    # Remove a user (soft delete by setting isActive to false) (INITIAL_STUDENT_ID)
    soft_delete_user(db, INITIAL_STUDENT_ID)

    # Delete an enrollment (NEW_ENROLLMENT_ID)
    delete_enrollment(db, NEW_ENROLLMENT_ID)

    # Remove a lesson from a course (COURSE_ID)
    remove_lesson_from_course(db, COURSE_ID, "Connecting to MongoDB")

    print("\n Testing Completed")
    

#--- Part 4: Advanced Queries and Aggregation---
# Importing libraries
from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd

# ensuring that connectio to MongoDb is established
MONGO_URI = "mongodb://localhost:27017/"
try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    print("Connection to MongoDB successful for Part 4!")
except Exception as e:
    print(f"Connection failed: {e}")
    exit()

#Get 'eduhub_db' database and collections
db = client['eduhub_db']
users_collection = db['users']
courses_collection = db['courses']
enrollments_collection = db['enrollments']
assignments_collection = db['assignments']
submissions_collection = db['submissions']


#Task 4.1: Complex Queries
print("\n Task 4.1: Complex Queries (Read Operations)")

# 1. Find courses with price between $50 and $200
# $gte = greater than or equal to and $lte = less than or equal to
price_range_courses = list(courses_collection.find({
    "price": {"$gte": 50, "$lte": 200}
}))
print(f"Found {len(price_range_courses)} courses priced between $50 and $200.")
for course in price_range_courses[:5]: #print first 5 results
    print(f" - {course['title']} (${course['price']})")

# 2. Get users who joined in the last 6 months
# Calculates a cutoff date and uses the $gt (greater than) operator
six_months_ago = datetime.utcnow() - timedelta(days=180)
recent_users = list(users_collection.find({
    "dateJoined": {"$gt": six_months_ago}
}))
print(f"\nFound {len(recent_users)} users who joined in the last 6 months.")
for user in recent_users[:5]: #print first 5 results
    print(f" - {user['firstName']} {user['lastName']} (Joined: {user['dateJoined'].strftime('%Y-%m-%d')})")


# 3. Find courses that have specific tags using $in operator
# Finds documents where the 'tags' array contains at least one of the specified values
tags_to_find = ["online", "2025", "Beginner Friendly"]
tagged_courses = list(courses_collection.find({
 "tags": {"$in": tags_to_find}
}))
print(f"\nFound {len(tagged_courses)} courses matching the generic tags: {', '.join(tags_to_find)}.")
for course in tagged_courses[:5]: #print first 5 results
  print(f" - {course['title']} (Tags: {course['tags']})")


# 4. Retrieve assignments with due dates in the next week
# Uses $gte and $lte to define a date range for the 'dueDate' field
now = datetime.utcnow()
next_week = now + timedelta(days=7)
upcoming_assignments = list(assignments_collection.find({
    "dueDate": {"$gte": now, "$lte": next_week}
}))
print(f"\nFound {len(upcoming_assignments)} assignments due in the next 7 days.")

for assignment in upcoming_assignments[:5]: #print first 5 results
    print(f" - {assignment['title']} (Due: {assignment['dueDate'].strftime('%Y-%m-%d')})")


#Task 4.2: Aggregation Pipeline 
print("\n Task 4.2: Aggregation Pipeline (Analytics)")

# Course Enrollment Statistics

# 1. Count total enrollments per course
enrollment_count_pipeline = [
    {"$group": {"_id": "$courseId", "totalEnrollments": {"$sum": 1}}},
    {"$sort": {"totalEnrollments": -1}},
    # Look up the course title for better reporting
    {"$lookup": {"from": "courses", "localField": "_id", "foreignField": "courseId", "as": "courseDetails"}},
    {"$unwind": "$courseDetails"},
    {"$project": {"_id": 0, "courseTitle": "$courseDetails.title", "totalEnrollments": 1}}
]
enrollment_counts = list(enrollments_collection.aggregate(enrollment_count_pipeline))
print("\n[A] Total enrollments per course:")
print(pd.DataFrame(enrollment_counts))


# 2. Group by course category
category_stats_pipeline = [
    # Join enrollments with courses to get category information
    {"$lookup": {"from": "courses", "localField": "courseId", "foreignField": "courseId", "as": "courseInfo"}},
    {"$unwind": "$courseInfo"},
    # Group by category
    {"$group": {"_id": "$courseInfo.category", "totalEnrollments": {"$sum": 1}, "uniqueCourses": {"$addToSet": "$courseId"}}},
    # Calculate the number of unique courses in that category
    {"$project": {"_id": 0, "category": "$_id", "totalEnrollments": 1, "uniqueCourseCount": {"$size": "$uniqueCourses"}}},
    {"$sort": {"totalEnrollments": -1}}
]
category_stats = list(enrollments_collection.aggregate(category_stats_pipeline))
print("\n[B] Enrollment statistics grouped by course category:")
print(pd.DataFrame(category_stats))


# Student Performance Analysis 

# 3. Average grade per student and Top-performing students using a lookup to get the student's name
student_performance_pipeline = [
    {"$group": {"_id": "$studentId", "averageGrade": {"$avg": "$grade"}, "submissionCount": {"$sum": 1}}},
    {"$sort": {"averageGrade": -1}},
    {"$limit": 10}, # Show top performers
    {"$lookup": {"from": "users", "localField": "_id", "foreignField": "userId", "as": "studentDetails"}},
    {"$unwind": "$studentDetails"},
    {"$project": {"_id": 0, "studentName": {"$concat": ["$studentDetails.firstName", " ", "$studentDetails.lastName"]}, "averageGrade": {"$round": ["$averageGrade", 2]}, "submissionCount": 1}}
]
student_grades = list(submissions_collection.aggregate(student_performance_pipeline))
print("\n[C] Top-performing students (by average grade):")
print(pd.DataFrame(student_grades))


# 4. Completion rate by course (requires 'progress' and 'status' fields from enrollments)
course_completion_pipeline = [
    {"$group": {"_id": "$courseId", "totalEnrollments": {"$sum": 1}, "completedCount": {"$sum": {"$cond": [{"$eq": ["$status", "completed"]}, 1, 0]}}}},
    {"$project": {"_id": 0, "courseId": "$_id", "totalEnrollments": 1, "completedCount": 1, "completionRate": {"$round": [{"$multiply": [{"$divide": ["$completedCount", "$totalEnrollments"]}, 100]}, 2]}}},
    {"$sort": {"completionRate": -1}},
    {"$lookup": {"from": "courses", "localField": "courseId", "foreignField": "courseId", "as": "courseDetails"}},
    {"$unwind": "$courseDetails"},
    {"$project": {"courseTitle": "$courseDetails.title", "totalEnrollments": 1, "completionRate_percent": {"$concat": [{"$toString": "$completionRate"}, "%"]}}}
]
course_completion_rates = list(enrollments_collection.aggregate(course_completion_pipeline))
print("\n[D] Course completion rates:")
print(pd.DataFrame(course_completion_rates))


# Instructor Analytics

# 5.Count of total unique students taught by each instructor
instructor_student_count_pipeline = [
    {"$lookup": {"from": "enrollments", "localField": "courseId", "foreignField": "courseId", "as": "enrollments"}},
    {"$unwind": "$enrollments"},
    {"$group": {"_id": "$instructorId", "allStudents": {"$addToSet": "$enrollments.studentId"}}},
    {"$project": {"_id": 0, "instructorId": "$_id", "uniqueStudentsTaught": {"$size": "$allStudents"}}},
    {"$sort": {"uniqueStudentsTaught": -1}},
    {"$lookup": {"from": "users", "localField": "instructorId", "foreignField": "userId", "as": "instructorDetails"}},
    {"$unwind": "$instructorDetails"},
    {"$project": {"instructorName": {"$concat": ["$instructorDetails.firstName", " ", "$instructorDetails.lastName"]}, "uniqueStudentsTaught": 1}}
]
instructor_student_counts = list(courses_collection.aggregate(instructor_student_count_pipeline))
print("\n[E] Total unique students taught by each instructor:")
print(pd.DataFrame(instructor_student_counts))


#  Advanced Analytics 
print("\n Advanced Analytics (Reporting: Monthly Trends, Popular Categories, Engagement)")


# 1. Monthly enrollment trends
# Extracts year and month from 'enrollmentDate' to track trends over time.
monthly_enrollment_pipeline = [
    {"$group": {"_id": {"year": {"$year": "$enrollmentDate"}, "month": {"$month": "$enrollmentDate"}}, "count": {"$sum": 1}}},
    {"$sort": {"_id.year": 1, "_id.month": 1}},
    {"$project": {"_id": 0, "YearMonth": {"$concat": [{"$toString": "$_id.year"}, "-", {"$toString": "$_id.month"}]}, "enrollmentCount": "$count"}}
]
monthly_trends = list(enrollments_collection.aggregate(monthly_enrollment_pipeline))
print("\n[F] 1. Monthly enrollment trends:")
print(pd.DataFrame(monthly_trends))


# 2. Most popular course categories
# Groups enrollments by course category and counts the total enrollments in each.
most_popular_categories_pipeline = [
    # Join enrollments with courses to get category information
    {"$lookup": {"from": "courses", "localField": "courseId", "foreignField": "courseId", "as": "courseInfo"}},
    {"$unwind": "$courseInfo"},
    # Group by category and count
    {"$group": {"_id": "$courseInfo.category", "totalEnrollments": {"$sum": 1}}},
    {"$sort": {"totalEnrollments": -1}} # Sorts by enrollment count to find the most popular
]
most_popular_categories = list(enrollments_collection.aggregate(most_popular_categories_pipeline))
print("\n[G] 2. Most popular course categories (by enrollment count):")
print(pd.DataFrame(most_popular_categories))


# 3. Student engagement metrics: Average Submissions Per Student
# Calculates the average number of assignments submitted across all students who submitted.
engagement_pipeline = [
    # Count submissions per student
    {"$group": {"_id": "$studentId", "submissionCount": {"$sum": 1}}},
    # Calculate the overall average
    {"$group": {"_id": None, "totalStudentsWithSubmissions": {"$sum": 1}, "totalSubmissions": {"$sum": "$submissionCount"}}},
    {"$project": {"_id": 0, "AverageSubmissionsPerStudent": {"$round": [{"$divide": ["$totalSubmissions", "$totalStudentsWithSubmissions"]}, 2]}}}
]
engagement_metrics = list(submissions_collection.aggregate(engagement_pipeline))
print("\n[H] 3. Student Engagement Metrics (Average Submissions Per Student):")
print(pd.DataFrame(engagement_metrics))


#--- Part 5: Indexing and Performance--
#--- Task 5.1: Index Creation---
#Removing Duplicates and Creating Unique Indexes

from pymongo import MongoClient
from pymongo import ASCENDING

# Use the correct local connection string and database name
client = MongoClient('mongodb://localhost:27017/')
db = client['eduhub_db']

print("Searching for duplicate emails...")

# Aggregate to find all duplicate emails
pipeline = [
    {
        "$group": {
            "_id": "$email",
            "count": {"$sum": 1},
            "docs": {"$push": "$_id"}
        }
    },
    {
        "$match": {
            "count": {"$gt": 1}
        }
    }
]

duplicates = list(db.users.aggregate(pipeline))

if duplicates:
    print(f"Found {len(duplicates)} email addresses with duplicates.")
    for duplicate in duplicates:
        email = duplicate['_id']
        ids_to_delete = duplicate['docs'][1:]  # Keep the first document, delete the rest
        
        print(f"  - Deleting {len(ids_to_delete)} duplicate(s) for email: {email}")
        
        # Delete the duplicate documents
        db.users.delete_many({'_id': {'$in': ids_to_delete}})
        
    print("\nAll duplicate documents have been removed.")
else:
    print("No duplicate emails found. The collection is ready for indexing.")


    from pymongo import MongoClient, ASCENDING

# Establishing exisitng connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['eduhub_db']

# 1. User email lookup
print("Creating index for user email lookup...")
db.users.create_index([('email', ASCENDING)], unique=True)
print("Index created on 'users.email'")

# 2. Course search by title and category
print("Creating compound index for course search...")
db.courses.create_index([('title', ASCENDING), ('category', ASCENDING)])
print("Compound index created on 'courses.title' and 'courses.category'")

# 3. Assignment queries by due date
print("Creating index for assignment due date...")
db.assignments.create_index([('dueDate', ASCENDING)])
print("Index created on 'assignments.dueDate'")

# 4. Enrollment queries by student and course
print("Creating compound index for enrollment queries...")
db.enrollments.create_index([('student_id', ASCENDING), ('course_id', ASCENDING)])
print("Compound index created on 'enrollments.student_id' and 'enrollments.course_id'")

print("\nAll indexes created successfully.")



# ---Task 5.2: Query Optimization---
#Query 1: User Email Lookup
import time
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

# Use the correct local connection string and database name
client = MongoClient('mongodb://localhost:27017/')
db = client['eduhub_db']

# 
email_to_find = 'john.doe@example.com' 

# ----------------- Unindexed Performance Measurement -----------------
print("--- Query 1: User Email Lookup (Before Index) ---")

# Drop the index to simulate an unindexed query
try:
    db.users.drop_index([('email', ASCENDING)])
    print("Dropped 'email' index for unindexed test.")
except CollectionInvalid:
    pass

start_time_unindexed = time.time()
db.users.find_one({'email': email_to_find})
end_time_unindexed = time.time()
unindexed_time = end_time_unindexed - start_time_unindexed
print(f"Unindexed query time: {unindexed_time:.6f} seconds")

# Indexed Performance Measurement 
print("\n--- Query 1: User Email Lookup (After Index) ---")

# Recreate the unique index on 'email'
db.users.create_index([('email', ASCENDING)], unique=True)
print("Recreated 'email' index.")

start_time_indexed = time.time()
db.users.find_one({'email': email_to_find})
end_time_indexed = time.time()
indexed_time = end_time_indexed - start_time_indexed
print(f"Indexed query time: {indexed_time:.6f} seconds")

#Performance Documentation 
print("\n Performance Improvement ")
explain_output = db.users.find({'email': email_to_find}).explain()
print(f"Query Plan Stage: {explain_output['queryPlanner']['winningPlan']['inputStage']['stage']}")

try:
    improvement = unindexed_time / indexed_time
    print(f"Performance improvement: {improvement:.2f}x faster")
except ZeroDivisionError:
    print("Indexed query was too fast to measure improvement accurately. (Time difference is negligible)")


#Query 2: Course Search by Title and Category
import time
from pymongo import MongoClient

# establisihing existing connection to MongoDb
client = MongoClient('mongodb://localhost:27017/')
db = client['eduhub_db']

# searching for existing course in the collection
title_to_find = 'Introduction to Python'
category_to_find = 'Programming'

#  Unindexed Performance Measurement 
print("Query 2: Course Search (Before Compound Index)")

# Drop the compound index to simulate an unindexed query
try:
    db.courses.drop_index([('title', ASCENDING), ('category', ASCENDING)])
    print("Dropped 'title_1_category_1' index for unindexed test.")
except CollectionInvalid:
    pass

start_time_unindexed = time.time()
courses = list(db.courses.find({'title': title_to_find, 'category': category_to_find}))
end_time_unindexed = time.time()
unindexed_time = end_time_unindexed - start_time_unindexed
print(f"Unindexed query time: {unindexed_time:.6f} seconds")

#  Indexed Performance Measurement 
print("\nQuery 2: Course Search (After Compound Index)")

# Recreate the compound index
db.courses.create_index([('title', ASCENDING), ('category', ASCENDING)])
print("Recreated 'title_1_category_1' index.")

start_time_indexed = time.time()
courses = list(db.courses.find({'title': title_to_find, 'category': category_to_find}))
end_time_indexed = time.time()
indexed_time = end_time_indexed - start_time_indexed
print(f"Indexed query time: {indexed_time:.6f} seconds")

#  Performance Documentation 
print("\n Performance Improvement")
explain_output = db.courses.find({'title': title_to_find, 'category': category_to_find}).explain()
print(f"Query Plan Stage: {explain_output['queryPlanner']['winningPlan']['inputStage']['stage']}")

try:
    improvement = unindexed_time / indexed_time
    print(f"Performance improvement: {improvement:.2f}x faster")
except ZeroDivisionError:
    print("Indexed query was fast enough to make impovement accuurately mesurable")

#Document the performance improvements using Python timing functions
#(Query 3: Enrollment Queries)
#imorting libraries
import time
from pymongo import MongoClient
from bson.objectid import ObjectId

# using existing connection to Mongo DB
client = MongoClient('mongodb://localhost:27017/')
db = client['eduhub_db']

student_id = ObjectId('60c72b2f9b1d1f001c9c7199') 
course_id = ObjectId('60c72b2f9b1d1f001c9c719a')

#  Unindexed Performance Measurement 
print("Query 3: Enrollment Lookup (Before Compound Index)")

# Drop the compound index to simulate an unindexed query
try:
    db.enrollments.drop_index([('student_id', ASCENDING), ('course_id', ASCENDING)])
    print("Dropped 'student_id_1_course_id_1' index for unindexed test.")
except CollectionInvalid:
    pass

start_time_unindexed = time.time()
enrollment = db.enrollments.find_one({'student_id': student_id, 'course_id': course_id})
end_time_unindexed = time.time()
unindexed_time = end_time_unindexed - start_time_unindexed
print(f"Unindexed query time: {unindexed_time:.6f} seconds")

#  Indexed Performance Measurement 
print("\n Query 3: Enrollment Lookup (After Compound Index)")

# Recreate the compound index
db.enrollments.create_index([('student_id', ASCENDING), ('course_id', ASCENDING)])
print("Recreated 'student_id_1_course_id_1' index.")

start_time_indexed = time.time()
enrollment = db.enrollments.find_one({'student_id': student_id, 'course_id': course_id})
end_time_indexed = time.time()
indexed_time = end_time_indexed - start_time_indexed
print(f"Indexed query time: {indexed_time:.6f} seconds")

# Performance Documentation 
print("\n Performance Improvement")
explain_output = db.enrollments.find({'student_id': student_id, 'course_id': course_id}).explain()
print(f"Query Plan Stage: {explain_output['queryPlanner']['winningPlan']['inputStage']['stage']}")

try:
    improvement = unindexed_time / indexed_time
    print(f"Performance improvement: {improvement:.2f}x faster")
except ZeroDivisionError:
    print("Indexed query was too fast to measure improvement accurately.")



#---Part 6: Data Validation and Error Handling 
# importing libraries
import pymongo
from pymongo.errors import DuplicateKeyError, ConnectionFailure
import re # Used for email format validation

# Custom Exception for Validation Errors
class ValidationError(Exception):
    """Custom exception used to signal a failure in schema validation."""
    pass

# Configuration details
MONGO_URI = 'mongodb://localhost:27017/'
DATABASE_NAME = 'eduhub_db'
COLLECTION_NAME = 'courses'

# Task 6.1: Define Validation Rules
REQUIRED_FIELDS = ['title', 'price', 'instructorEmail', 'level']
VALID_LEVELS = ['beginner', 'intermediate', 'expert']

def validate_course(data):
    """
    Implements validation rules for Task 6.1 (Required, Data Type, Enum, Email).
    Raises a ValidationError if any rule is violated.
    """
    errors = {}

    # 1. Required fields chec
    for field in REQUIRED_FIELDS:
        # Checks if field is missing OR if its value is null
        if field not in data or data[field] is None:
            errors[field] = f"'{field}' is a required field."

    if errors:
        raise ValidationError(errors)

    # 2. Data type validation and Range checks, title must be a string
    if not isinstance(data.get('title'), str):
        errors['title'] = "Course title must be a string."

    # price must be a postive number
    price = data.get('price')
    if not isinstance(price, (int, float)):
        # Task 6.2: Handles Invalid data type insertions 
        errors['price'] = f"Course price must be a number, not '{type(price).__name__}'."
    elif price < 0:
        errors['price'] = "Price cannot be negative."

    # level must be a string and an enum value
    level = data.get('level')
    if not isinstance(level, str):
        errors['level'] = "Course level must be a string."
    elif level.lower() not in VALID_LEVELS:

        #3. Enum value restrictions check 
        errors['level'] = f"'{level}' is not a supported course level. Must be one of {VALID_LEVELS}."

    # 4. Email format validation (Regex)
    email = data.get('instructorEmail')
    # Basic regex for email format
    email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if not isinstance(email, str):
        errors['instructorEmail'] = "Instructor email must be a string."
    elif not re.match(email_regex, email):
        errors['instructorEmail'] = f"'{email}' is not a valid email format."

    if errors:
        raise ValidationError(errors)

def attempt_save(collection, data, description):
    """
    Attempts to save the course data, handling custom Validation errors and
    PyMongo's DuplicateKeyError (E11000).
    """
    print(f"\n--- Attempting: {description} ---")
    try:
        # 1. Manual Schema Validation (Task 6.1 checks)
        validate_course(data)

        # 2. Database Insertion
        result = collection.insert_one(data)
        print(f"SUCCESS: Document saved. ID: {result.inserted_id}")
        print(f"  -> Title: {data.get('title')}, Email: {data.get('instructorEmail')}")

    except ValidationError as e:

        # Task 6.2: Handling Missing required fields, Invalid data types, Enum, Email format
        print("ERROR (Validation Error): Invalid data provided.")
        for field, message in e.args[0].items():
            print(f"  -> Field '{field}': {message}")

    except DuplicateKeyError as e:
        # Task 6.2: Handles Duplicate key errors 
        print("ERROR (Duplicate Key Error): Cannot save document due to unique constraint violation.")
        # Attempt to parse the duplicate key field from the error message
        error_msg = str(e)
        key_match = re.search(r'dup key: { (\S+): \"?([^\"]+)\"? }', error_msg)
        if key_match:
             # Remove index name suffix ('_1') and print key/value
             key_field = key_match.group(1).split(':')[0].strip().replace('_1', '')
             key_value = key_match.group(2)
             print(f"  -> Field '{key_field}' with value '{key_value}' already exists.")
        else:
             print("  -> A unique constraint was violated on an indexed field.")

    except Exception as e:
        # Handles generic database errors or unexpected issues
        print(f"An unexpected error occurred: {type(e).__name__}: {e}")

def run_part6_demo():
    """Main execution function for Part 6 demo."""
    client = None
    try:
        # Initialize connection
        client = pymongo.MongoClient(MONGO_URI)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        print(f"Connection successful to database '{DATABASE_NAME}'.")

        # Ensure unique index on 'instructorEmail'
        collection.create_index([("instructorEmail", pymongo.ASCENDING)], unique=True)
        print(f"Successfully ensured unique index on '{COLLECTION_NAME}.instructorEmail'.")

        # Clean up collection for repeatable testing
        collection.delete_many({})
        print("🧹 Collection cleared for demo runs.")

        # Test Cases (Task 6.2)

        # 1. SUCCESS Case (Valid data)
        attempt_save(collection,
            { 'title': 'Python Backend Development', 'price': 99.99, 'instructorEmail': 'tunde.a@eduhub.com', 'level': 'beginner', 'isPublished': True },
            '1. Valid Course Insertion'
        )

        # 2. Task 6.2: Missing required fields
        attempt_save(collection,
            { 'price': 50, 'instructorEmail': 'chidi.o@eduhub.com', 'level': 'intermediate' },
            '2. Missing Required Field: "title"'
        )

        # 3. Task 6.2: Duplicate key errors (InstructorEmail ust be unique)
        attempt_save(collection,
            { 'title': 'Data Science with Python', 'price': 199.99, 'instructorEmail': 'tunde.a@eduhub.com', 'level': 'expert' },
            '3. Duplicate Key Error: "instructorEmail"'
        )

        # 4. Task 6.2: Invalid data type insertions ("price" mustbe a number)
        attempt_save(collection,
            { 'title': 'NoSQL Fundamentals', 'price': 'one hundred', 'instructorEmail': 'bola.m@eduhub.com', 'level': 'intermediate' },
            '4. Invalid Data Type Insertion: "price" is a string'
        )

        # 5. Task 6.1: Enum restriction violation
        attempt_save(collection,
            { 'title': 'Advanced Algorithms', 'price': 250, 'instructorEmail': 'kemi.l@eduhub.com', 'level': 'guru' },
            '5. Enum Violation: "level" is invalid'
        )

        # 6. Task 6.1: Email format validation failure
        attempt_save(collection,
            { 'title': 'MongoDB Basics', 'price': 10, 'instructorEmail': 'emeka.at.home', 'level': 'beginner' },
            '6. Email Format Validation: "instructorEmail" is invalid'
        )

    except ConnectionFailure as e:
        print(f"\n Connection Failed: Unable to connect to MongoDB at {MONGO_URI}. Ensure MongoDB server is running.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"\n Connection Failed during TEST SETUP: {type(e).__name__}: {e}")
    finally:
        if client:
            client.close()
            print("\nMongoDB connection closed.")

if __name__ == "__main__":
    run_part6_demo()

