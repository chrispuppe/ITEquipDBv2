import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BOOLEAN
from sqlalchemy.exc import ProgrammingError


# MySQL
mysql_db_username = 'dbadmin'
mysql_db_password = 'nureniHOIUBENOIPn*7b3bunsd8n4i**G*Vbibjn23#$@we5r'
mysql_db_name = 'itequipdb'
mysql_db_hostname = 'localhost'

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=mysql_db_username,
                                                                                        DB_PASS=mysql_db_password,
                                                                                        DB_ADDR=mysql_db_hostname,
                                                                                        DB_NAME=mysql_db_name)

engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI) # connect to server
# 'mysql+pymysql://dbadmin:nureniHOIUBENOIPn*7b3bunsd8n4i**G*Vbibjn23#$@we5r'

try:
    engine.connect()
    engine.execute("CREATE DATABASE itequipdb") #create db
except ProgrammingError:
    pass

Base = declaractive_base(bind=engine)


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    create_ts = Column(DateTime)
    skill_level = Column(Integer)
    email_address = Column(String(128))
    trade = Column(String(128))

 #   children = relationship("Device")

class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True)
    history = Column(String(255))
    #parent_id = Column(Integer, ForeignKey('employee.id'))

class Ipads(Base):
    __tablename__ = 'ipads'
    serial = Column(String(128), primary_key=True)
    model = Column(String(128))
    storage_capacity = Column(String(128))
    date_purchased = Column(DateTime)
    #parent_id = Column(Integer, ForeignKey('device.id'))

class Fob(Base):
    __tablename__ = 'fob'
    num = Column(Integer, unique=True, primary_key=True)
    serial = Column(String(64))

class Computers(Base):
    __tablename__ = 'computers'
    computer_id = Column(Integer, unique=True, primary_key=True)
    computer_name = Column(String(64))
    brand = Column(String(64))
    model = Column(String(64))
    serial = Column(String(128))
    computer_type = Column(String(64))
    operating_system = Column(String(64))
    notes = Column(String(512))
    retired = Column(BOOLEAN())
    disposed = Column(BOOLEAN())
    disposed_date = Column(Date)
    aquired_date = Column(Date)
    purchase_price = Column(Integer)
    vendor_id = Column(String(64))
    warranty_start = Column(Date)
    warranty_length = Column(Integer)
    warranty_end = Column(Date)
    employee_id = Column(Integer)
    history = Column(String(255))
    
class Printers(Base):
    __tablename__ = 'printers'
    printer_id = Column(String(64), unique=True, primary_key=True)
    brand = Column(String(64))
    model = Column(String(64))
    printer_type = Column(String(64))
    aquired_date = Column(DateTime)
    vendor_id = Column(String(64))

class Phone_Account(Base):
    __tablename__ = 'phone_account'
    phone_number = Column(String(16), unique=True, primary_key=True)
    phone_model = Column(String(16))
    phone_os = Column(String(64))
    notes = Column(String(255))

class Vendors(Base):
    __tablename__ = 'vendors'
    vendor_id = Column(String(64), unique=True, primary_key=True)
    current_rep = Column(String(96))
    phone_number = Column(String(16))
    email_address = Column(String(128))
    
class Printer_Model(Base):
    __tablename__ = 'printer_model'
    printer_model = Column(String(64), unique=True, primary_key=True)
    brand = Column(String(64))
    printer_type = Column(String(64))

class Post(Base):
    __tablename__ = 'example'
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    body = Column(Text)
        
        

if __name__ == "__main__":
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(bind=engine)
