from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String,Float
from sqlalchemy.orm import declarative_base,sessionmaker
engine= create_engine('sqlite:///./mydata.db',echo=True)
base =declarative_base()
class new_person(base):
    __tablename__= "users"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False) 
    Email=Column(String,nullable=False)
    Phone_number=Column(Integer)
    Skills=Column(String)
    Education=Column(String)
    Work_experience=Column(Integer)
    achievements = Column(String,nullable=False)
    job_position=Column(String)

base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)


    



