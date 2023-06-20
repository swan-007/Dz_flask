import os
from atexit import register

from dotenv import load_dotenv
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

load_dotenv()


pg_dns = f"postgresql://{os.getenv('db_user')}:{os.getenv('db_password')}@{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_name')}"
engine = create_engine(pg_dns)
register(engine.dispose)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    password = Column(String(60), nullable=False)
    time = Column(DateTime, server_default=func.now())


class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    heading = Column(String(20), nullable=False)
    description = Column(Text)
    date_of_creation = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", backref="advertisements")


# Base.metadata.create_all(bind=engine)

# with Session() as s:
#     # u = User(name='ivan', password='123')
#     # s.add(u)
#     # s.commit()
#     u = s.get(Advertisement, 10)
#     print(u.id)
