# MongoDB EduHub Project

This repository contains a complete database backend system for **EduHub**, a fictional online e-learning platform. The project demonstrates a comprehensive understanding of MongoDB database concepts, from data modeling and CRUD operations to advanced querying, aggregation, and performance optimization. It is built using Python with the **PyMongo** library and showcases best practices for building a scalable and efficient NoSQL database solution.

## Table of Contents

- #project-overview
- #project-features
- #project-objectives
- #repository-structure
- #setup-and-installation
- #how-to-use
- #database-schema
- #performance-analysis
- #challenges-and-solutions
- #deliverables
- #license

## Project Overview

The project simulates the data management challenges of a modern e-learning application. The primary goal is to design, implement, and optimize a robust MongoDB database for "EduHub" where students can enroll in courses, instructors can create content, and the system can track student progress and performance.

---

## Project Features

The database system is designed to support the following functional requirements:

* **User Management:** Registration, authentication, and profile management for both students and instructors.
* **Course Management:** Creation, publishing, categorization, and content organization for courses.
* **Enrollment System:** Student enrollment, progress tracking, and completion status.
* **Assessment System:** Creation of assignments, handling submissions, and managing grades.
* **Analytics and Reporting:** Generating key performance metrics, enrollment statistics, and revenue reports using aggregation pipelines.
* **Search and Discovery:** Efficient course search functionality with filtering and sorting capabilities.

---

## Project Objectives

By completing this project, the following proficiencies are demonstrated:

* Database and collection creation with schema validation.
* Document insertion and data modeling.
* CRUD operations (Create, Read, Update, Delete).
* Query optimization and indexing.
* Using the Aggregation Framework for complex analytics.
* Data validation and error handling to ensure data integrity.


## Database Schema
The text-based representation of the data model clearly shows the collections, their key fields, and how they relate to each other. Here is the textual representation of your EduHub data model:

+-------------------+       +-------------------+       +-------------------+
|     users         |<-----|    courses        |<------|    enrollments    |
|-------------------|       |-------------------|       |-------------------|
| _id (ObjectId)    |       | _id (ObjectId)    |       | _id (ObjectId)    |
| userId (string)   |       | courseId (string) |       | enrollmentId (str)|
| email (string)    |       | title (string)    |       | studentId (string)| <-- references users.userId
| firstName (string)|       | description (str) |       | courseId (string) | <-- references courses.courseId
| lastName (string) |       | instructorId (str)|<--+   | enrollmentDate (dt)|
| role (enum)       |       | category (string) |   |   | progress (number) |
| dateJoined (dt)   |       | level (enum)      |   |   | completionDate (dt)|
| profile (obj)     |       | duration (number) |   |   | status (enum)     |
| isActive (boolean)|       | price (number)    |   |   |                   |
+-------------------+       | tags ([string])   |   |   +-------------------+
                            | createdAt (datetime)|   |
                            | updatedAt (datetime)|   |
                            | isPublished (boolean)|   |
                            +-------------------+   |
                                                    |
                                                    |
+-------------------+       +-------------------+   |   +-------------------+
|     lessons       |<------|   assignments     |<--+   |   submissions     |
|-------------------|       |-------------------|       |-------------------|
| _id (ObjectId)    |       | _id (ObjectId)    |       | _id (ObjectId)    |
| lessonId (string) |       | assignmentId (str)|       | submissionId (str)|
| courseId (string) |<--+   | courseId (string) |<--+   | studentId (string)| <-- references users.userId
| title (string)    |   |   | title (string)    |   |   | assignmentId (str)| <-- references assignments.assignmentId
| content (string)  |   |   | description (str) |   |   | courseId (string) | <-- references courses.courseId
| order (number)    |   |   | dueDate (datetime)|   |   | submissionDate (dt)|
| createdAt (dt)    |   |   | maxScore (number) |   |   | grade (number)    |
| updatedAt (dt)    |   |   +-------------------+   |   | feedback (string) |
+-------------------+   |                           |   | submittedFile (str)|
                        |                           |   +-------------------+
                        +---------------------------+


#How to interpret this diragram:

-Boxes: Each box represents a MongoDB collection (e.g., users, courses).

-Inside Boxes: Lists the main fields within each document in that collection, along with their data types (e.g., _id (ObjectId), email (string)).

-Arrows (<-----): Indicate a reference from one collection to another. The arrow points from the collection that contains the reference ID to the collection it refers to. For example, instructorId (str) in courses has an arrow pointing to users, meaning instructorId holds the userId of a document in the users collection.

-The comments like <-- references users.userId explicitly state which field is being referenced.

## Repository Structure

The project files are organized in the following directory structure to maintain clarity and adhere to submission guidelines:
mongodb-eduhub-project/
├── README.md
├── notebooks/
│   └── eduhub_mongodb_project.ipynb
├── src/
│   └── eduhub_queries.py
├── data/
│   ├── sample_data.json
│   └── schema_validation.json
├── docs/
│   ├── performance_analysis.md
│   └── presentation.pptx
└── .gitignore

---

## Setup and Installation

### 1. Prerequisites

* **MongoDB:** Ensure you have MongoDB Community Server and MongoDB Compass (GUI) installed and running locally on `mongodb://localhost:27017/`.
* **Python:** This project requires Python 3.8 or higher.

### 2. Environment Setup

It is highly recommended to use a virtual environment to manage project dependencies.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/lewikeezy/mongodb-eduhub-project.git
    cd mongodb-eduhub-project
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # For macOS/Linux
    source venv/bin/activate
    # For Windows
    venv\Scripts\activate
    ```
3.  **Install required libraries:**
    ```bash
    pip install pymongo pandas jupyter
    ```

---

## How to Use

All project operations are demonstrated within a single Jupyter Notebook. To run the project:

1.  Make sure your MongoDB server is running.
2.  Activate your virtual environment.
3.  Navigate to the project's root directory.
4.  Launch the Jupyter Notebook:
    ```bash
    jupyter notebook notebooks/eduhub_mongodb_project.ipynb
    ```
5.  Run each cell sequentially to see the database creation, data population, CRUD operations, advanced queries, and performance analysis results.

---

## Database Schema

The database is composed of six main collections, with relationships maintained through document referencing.

* **`users`**: Manages user profiles for both `students` and `instructors`.
* **`courses`**: Stores course details, referencing the `instructorId` from the `users` collection.
* **`enrollments`**: Links `students` to `courses`, tracking progress and completion.
* **`lessons`**: Contains individual lessons, each linked to a parent `course`.
* **`assignments`**: Holds details for course assignments, linked to a parent `course`.
* **`submissions`**: Manages student submissions for assignments, referencing the `studentId` and `assignmentId`.

---

## Performance Analysis

To ensure efficient data retrieval, **indexing** was applied to key fields used in frequent queries. The performance improvements are documented in detail in the `docs/performance_analysis.md` file, which includes:

* **Query Explanations:** A breakdown of how each query works.
* **Before/After Comparisons:** Analysis of query execution time using the `explain()` method to show the dramatic performance gains after index creation.

---

## Challenges and Solutions

A primary challenge was designing the **document schema** to balance data integrity and flexibility. The solution was to use **manual referencing** for most one-to-many and many-to-many relationships, which avoids data duplication and simplifies updates. Another challenge involved creating **complex aggregation pipelines** for analytics, which was solved by carefully structuring the pipeline stages (`$match`, `$group`, `$lookup`, etc.) to process data efficiently.

---

## Deliverables

The final project includes the following files, committed to this repository:

* `notebooks/eduhub_mongodb_project.ipynb` (Interactive Jupyter Notebook)
* `src/eduhub_queries.py` (Backup Python script)
* `data/sample_data.json` (Exported sample data)
* `docs/performance_analysis.md` (Detailed performance report)
* `docs/presentation.pptx` (Brief design presentation)

---

## License

This project is licensed under the MIT License.
