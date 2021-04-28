# DATABASE SETTINGS
pg_db_username = 'postgres'
pg_db_password = ''
pg_db_name = 'fscafold'
pg_db_hostname = 'localhost'

# MYSQL
mysql_db_username = 'root'
mysql_db_password = 'ThisTime43'
mysql_db_name = 'itequipdb'
mysql_db_hostname = 'localhost'

DEBUG = True
PORT = 5000
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False
SECRET_KEY = "SOME SECRET"
SQLALCHEMY_TRACK_MODIFICATIONS = True
WHOOSH_BASE = "whoosh"
# PostgreSQL
"""SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=pg_db_username,
                                                                                        DB_PASS=pg_db_password,
                                                                                        DB_ADDR=pg_db_hostname,
                                                                                        DB_NAME=pg_db_name)"""

# MySQL
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=mysql_db_username,
                                                                                        DB_PASS=mysql_db_password,
                                                                                        DB_ADDR=mysql_db_hostname,
                                                                                        DB_NAME=mysql_db_name)
# Email Server Configuration

MAIL_DEFAULT_SENDER = "cpuppe@localhost"

PASSWORD_RESET_EMAIL ="""
    Hi,
      Please click on the link below to reset your password
      <a href="/forgotpassword/{token}> Click here </a>"""