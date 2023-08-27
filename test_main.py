import pytest
from main import (
    get_student,
    get_student_courses,
    verify_token,
    Student,
    EnrolledCourse,
    Base,
    engine,
    Session,
    pbkdf2_sha256,
    jwt,
    SECRET_KEY,
    predefined_courses,
    AuthenticationError,
    CourseSelectionError,
    CourseDisplayError,
)

@pytest.fixture
def session():
    session = Session()
    yield session
    session.close()

@pytest.fixture
def database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_get_student(session, database):
    # Create a test student
    test_student = Student(username="testuser", password_hash="testhash", year_of_study=1)
    session.add(test_student)
    session.commit()

    # Retrieve the student
    student = get_student("testuser")
    assert student is not None
    assert student.username == "testuser"

def test_authentication_error():
    with pytest.raises(AuthenticationError):
        raise AuthenticationError("Test Authentication Error")

def test_course_selection_error():
    with pytest.raises(CourseSelectionError):
        raise CourseSelectionError("Test Course Selection Error")

def test_course_display_error():
    with pytest.raises(CourseDisplayError):
        raise CourseDisplayError("Test Course Display Error")
