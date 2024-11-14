import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create Base class for declarative models
Base = declarative_base()

# Student Model
class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    
    # Relationships
    homeworks = relationship('Homework', back_populates='student')
    quizzes = relationship('Quiz', back_populates='student')
    projects = relationship('Project', back_populates='student')

# Homework Model
class Homework(Base):
    __tablename__ = 'homeworks'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    homework_number = Column(Integer)
    score = Column(Float)
    
    student = relationship('Student', back_populates='homeworks')

# Quiz Model
class Quiz(Base):
    __tablename__ = 'quizzes'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    quiz_number = Column(Integer)
    score = Column(Float)
    
    student = relationship('Student', back_populates='quizzes')

# Project Model
class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    project_number = Column(Integer)
    score = Column(Float)
    
    student = relationship('Student', back_populates='projects')

# Database Setup Function
def setup_database(db_path='grades24.db'):
    # Create engine
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create a session factory
    Session = sessionmaker(bind=engine)
    
    return Session()

# Example Usage Function
def populate_sample_data(session):
    # Create a sample student
    student1 = Student(name='John Doe', email='john.doe@example.com')
    session.add(student1)
    
    # Add sample homeworks
    for hw_num in range(1, 7):
        homework = Homework(student=student1, homework_number=hw_num, score=0.0)
        session.add(homework)
    
    # Add sample quizzes
    for quiz_num in range(1, 11):
        quiz = Quiz(student=student1, quiz_number=quiz_num, score=0.0)
        session.add(quiz)
    
    # Add sample projects
    for proj_num in range(1, 9):
        project = Project(student=student1, project_number=proj_num, score=0.0)
        session.add(project)
    
    # Commit the changes
    session.commit()

# Main execution
if __name__ == '__main__':
    # Setup the database
    session = setup_database()
    
    # Populate with sample data
    populate_sample_data(session)
    
    print("Database 'grades24.db' created successfully with sample data.")