import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.hash import pbkdf2_sha256
import jwt
import datetime

Base = declarative_base()

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class AuthenticationError(Exception):
    pass

class CourseSelectionError(Exception):
    pass

class CourseDisplayError(Exception):
    pass

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    year_of_study = Column(Integer)
    enrolled_courses = relationship("EnrolledCourse", back_populates="student")

class EnrolledCourse(Base):
    __tablename__ = 'enrolled_courses'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_name = Column(String)
    student = relationship("Student", back_populates="enrolled_courses")

engine = create_engine('sqlite:///student_database.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

# Predefined set of courses
predefined_courses = {
    1: ["Math", "Physics", "Chemistry"],
    2: ["Biology", "Geography", "History"],
    3: ["Literature", "Economics", "Political Science"],
    4: ["Computer Science", "Psychology", "Sociology"]
}

# Define a secret key for JWT encoding and decoding. Keep this secret.
SECRET_KEY = "deepikaKey"

def authentication_page():
    try:
        st.title("Authentication")
        session = Session()

        login_signup = st.radio("Login/Sign Up", ["Login", "Sign Up"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if login_signup == "Sign Up":
            year_of_study = st.number_input("Year of Study", min_value=1, max_value=4)
            if st.button("Sign Up"):
                password_hash = pbkdf2_sha256.hash(password)
                new_student = Student(username=username, password_hash=password_hash, year_of_study=year_of_study)
                session.add(new_student)
                session.commit()
                st.success("Sign up successful!")

        elif login_signup == "Login":
            if st.button("Login"):
                student = session.query(Student).filter_by(username=username).first()
                if student and pbkdf2_sha256.verify(password, student.password_hash):
                    # Generate a JWT token upon successful login
                    token_payload = {
                        "username": username,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
                    }
                    token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
                    st.session_state.token = token  # Store the token in the session
                    st.success("Login successful!")
                else:
                    raise AuthenticationError("Invalid credentials")

    except AuthenticationError as e:
        st.error(str(e))

def course_selection_page():
    try:
        st.title("Course Selection")
        session = Session()

        student = session.query(Student).filter_by(username=jwt.decode(st.session_state.token, SECRET_KEY, algorithms=["HS256"])["username"]).first()
        year = student.year_of_study

        # Get the predefined courses for the student's year
        available_courses = predefined_courses.get(year, [])
        chosen_courses = st.multiselect("Select your courses", available_courses)
        if st.button("Save"):
            session.query(EnrolledCourse).filter_by(student_id=student.id).delete()
            for course_name in chosen_courses:
                enrolled_course = EnrolledCourse(student_id=student.id, course_name=course_name)
                session.add(enrolled_course)
            session.commit()
            st.success("Courses saved!")

    except CourseSelectionError as e:
        st.error(str(e))

def course_display_page():
    try:
        st.title("Course Display")
        session = Session()

        student = session.query(Student).filter_by(username=jwt.decode(st.session_state.token, SECRET_KEY, algorithms=["HS256"])["username"]).first()
        st.write("Chosen Courses:")
        for enrolled_course in student.enrolled_courses:
            st.write(enrolled_course.course_name)

    except CourseDisplayError as e:
        st.error(str(e))

def main():
    st.sidebar.title("Navigation")
    pages = ["Authentication", "Course Selection", "Course Display"]
    page = st.sidebar.radio("Go to", pages)

    try:
        if page == "Authentication":
            authentication_page()
        elif page == "Course Selection":
            if not hasattr(st.session_state, 'token') or not verify_token(st.session_state.token):
                raise AuthenticationError("Please log in to continue")
            else:
                course_selection_page()
        elif page == "Course Display":
            if not hasattr(st.session_state, 'token') or not verify_token(st.session_state.token):
                raise AuthenticationError("Please log in to continue")
            else:
                course_display_page()

    except (AuthenticationError, CourseSelectionError, CourseDisplayError) as e:
        st.error(str(e))

# Helper function to verify JWT token
def verify_token(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired. Please log in again.")
    except jwt.DecodeError:
        raise AuthenticationError("Invalid token. Please log in again.")

if __name__ == '__main__':
    main()
