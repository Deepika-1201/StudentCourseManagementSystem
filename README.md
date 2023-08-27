# StudentCourseManagementSystem
Student Course Management System

Overview
This project aims to develop a Student Course Management System (SCMS) to streamline student data management and course selection

Objectives and Scope
The primary objectives are to automate student registration, course enrollment, and improve administrative efficiency.

StakeHolders
This document is intended for developers, testers, and stakeholders involved in the development and deployment of the Student Course Registration System.

Requirements
Authenticated SignUp and SignIn Page
Choosing courses amongst the existing courses based upon year
Displaying the selected course

DataBase Design

Student Entity
	- Attributes:
    - `id` (Primary Key, Integer): Unique identifier for each student.
    - `username` (String): Student's username for authentication.
    - `password hash` (String): Hashed password for security.
    - `year_of_study` (Integer): Indicates the current year of study.

EnrolledCourse Entity
- Attributes:
    - `id` (Primary Key, Integer): Unique identifier for each enrolled course.
    - `student_id` (Foreign Key, Integer): References the `id` of the associated student.
    - `course_name` (String): Name of the enrolled course.

User Interfaces
Authentication Page
- Create a Streamlit page with the following components:
    - Username and password input fields.
    - Radio button for selecting between login and sign-up.
    - Buttons for login and sign-up actions.
- Implement logic to capture user input and handle interactions.

Course Selection Page
- Develop a Streamlit page for course selection with the following elements:
    - Display the student's year of study.
    - Retrieve predefined courses based on the year.
    - Allow students to select courses using checkboxes.
    - Provide a "Save" button to save course selections.

Course Display Page
- Design a Streamlit page to display enrolled courses for the student.
- Retrieve and display a list of enrolled courses.

Navigation
- Sidebar navigation allows users to switch between pages.
- Unauthorized users are prevented from accessing certain pages.

Functional Flow
Sign Up
- Capture user input for sign-up, including `username`, `password`, and `year_of_study`.
- Hash the password using `pbkdf2_sha256`.
- Store user data in the `students` table.

Login
- Verify user credentials by checking the hashed password against the stored hash.
- Generate a JWT token upon successful login.
- Store the token in the session state.

Course Selection
- Fetch predefined courses based on the student's year of study.
- Enable students to select courses and save their choices in the `enrolled_courses` table.

Course Display
- Retrieve the list of enrolled courses for the student from the database.
- Display the list on the Course Display Page.

Authentication System
JWT Token Generation
- Use the `jwt` library to generate JWT tokens.
- Include the student's `username` and an expiration time in the token payload.

Password Hashing
- Implement password hashing using `passlib`'s `pbkdf2_sha256` for secure storage.

Security
Secret Key Management: The JWT secret key is securely stored.
Token Security: JWT tokens are used with an expiration time.
Password Hashing: Passwords are securely hashed before storage.

Session State Management
Store the JWT token in the Streamlit session state after successful login.
Access the token when necessary for authentication.

Testing
     Unit testing is performed for individual components.

Error Handling
Implement custom exception classes:
    - `AuthenticationError`: For authentication-related errors.
    - `CourseSelectionError`: For course selection errors.
    - `CourseDisplayError`: For course display errors.
Provide informative error messages and graceful error handling throughout the application.

Deployment and Scaling
The project has been deployed to github.

Performance Optimization:
LRU Caching: Implement caching for frequently accessed data.: 
Database Indexing: Optimize database queries.

Risks and Mitigations
Risks: Data breaches, server downtime.
Mitigations: Strong encryption, regular backups.

Future Enhancements
API Creation
Cookies 
NoSQL Database ( for scaling)
