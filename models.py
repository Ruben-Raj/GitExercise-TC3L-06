from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.ext.declarative import as_declarative

# Define the base class for our models
Base = declarative_base()

# Define the User model 
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False) 
    requests = relationship('Request', back_populates='user')
    offers = relationship('Offer', back_populates='tutor')
    chats = relationship('Chat', back_populates='sender')

# Define the Request model
class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subject = Column(String, nullable=False)
    details = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    user = relationship('User', back_populates='requests')

# Define the Offer model
class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey('users.id'))
    request_id = Column(Integer, ForeignKey('requests.id'))
    offer_details = Column(Text, nullable=False)
    tutor = relationship('User', back_populates='offers')
    request = relationship('Request')

# Define the Chat model
class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    sender = relationship('User', back_populates='chats')

# Create an SQLite database and tables
engine = create_engine('sqlite:///student_hub.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
