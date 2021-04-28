from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BOOLEAN
import sqlalchemy
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
# 'mysql+pymysql://root:ThisTime43@localhost'

try:
    engine.connect()
    engine.execute("CREATE DATABASE itequipdb") #create db
except ProgrammingError:
    pass

Base = declaractive_base()

if __name__ == "__main__":
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(bind=engine)

