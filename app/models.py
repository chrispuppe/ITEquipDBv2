from app import db
from sqlalchemy.dialects.mysql import BOOLEAN
from sqlalchemy import ForeignKey
import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer,unique=True, primary_key=True)
    name = db.Column(db.String(255))
    create_ts = db.Column(db.DateTime)
    skill_level = db.Column(db.Integer)
    email_address = db.Column(db.String(128))
    trade = db.Column(db.String(128))
    inactive = db.Column(db.BOOLEAN(), default=False, nullable=False)

    def __init__(self, name, skill_level, email_address, trade):
    	self.name = name
    	self.create_ts = datetime.datetime.now()
    	self.skill_level = skill_level
    	self.email_address = email_address
    	self.trade = trade

 
# Super class for all devices so they can all be called at once.
class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    #assigned_to = db.Column(db.Integer, ForeignKey('employee.id'))
    
    __maper_args__ = {'polymorphic_identity':'device'}
    

class Ipads(Device):
    __tablename__ = 'ipads'
    __maper_args__ = {'polymorphic_identity': 'ipads'}

    id = db.Column(db.Integer, ForeignKey('device.id'), primary_key=True)
    serial = db.Column(db.String(128))
    model = db.Column(db.String(128))
    storage_capacity = db.Column(db.String(128))
    date_purchased = db.Column(db.Date)

    def __init__(self, serial, model, storage_capacity, date_purchased, assigned_to):
        self.serial = serial
        self.model = model
        self.storage_capacity = storage_capacity
        self.date_purchased = date_purchased
        self.assigned_to = assigned_to


class Fob(Device):
    __tablename__ = 'fob'
    __maper_args__ = {'polymorphic_identity': 'fob'}

    id = db.Column(db.Integer, ForeignKey('device.id'), primary_key=True)
    fob_number = db.Column(db.Integer)
    fob_serial = db.Column(db.String(64))
    assigned_to = db.Column(db.Integer, ForeignKey('employee.id'), nullable=True)

    def __init__(self, fob_number, fob_serial, assigned_to):
        self.fob_number = fob_number
        self.fob_serial = fob_serial
        self.assigned_to = assigned_to



class Computers(Device):
    __tablename__ = 'computers'
    __maper_args__ = {'polymorphic_identity': 'computers'}

    id = db.Column(db.Integer, ForeignKey('device.id'), primary_key=True)
    computer_name = db.Column(db.String(64))
    brand = db.Column(db.String(64))
    model = db.Column(db.String(64))
    serial = db.Column(db.String(128))
    computer_type = db.Column(db.String(64))
    operating_system = db.Column(db.String(64))
    notes = db.Column(db.String(512))
    retired = db.Column(db.BOOLEAN())
    disposed = db.Column(db.BOOLEAN())
    disposed_date = db.Column(db.Date)
    aquired_date = db.Column(db.Date)
    purchase_price = db.Column(db.Integer)
    vendor_id = db.Column(db.String(64))
    warranty_length = db.Column(db.Integer)
    employee_id = db.Column(db.Integer)
    history = db.Column(db.String(255))
    assigned_to = db.Column(db.Integer, ForeignKey('employee.id'))

    def __init__(
                self, computer_name, brand, model, serial, computer_type, 
                operating_system, notes, aquired_date, purchase_price, 
                vendor_id, warranty_length, assigned_to
                ):

        self.computer_name = computer_name
        self.brand = brand
        self.model = model
        self.serial = serial
        self.computer_type = computer_type
        self.operating_system = operating_system
        self.notes = notes
        self.aquired_date = aquired_date
        self.purchase_price = purchase_price
        self.vendor_id = vendor_id
        self.warranty_length = warranty_length
        self.assigned_to = assigned_to


class Printers(Device):
    __tablename__ = 'printers'
    __maper_args__ = {'polymorphic_identity': 'printers'}

    id = db.Column(db.Integer, ForeignKey('device.id'), primary_key=True)
    brand = db.Column(db.String(64))
    model = db.Column(db.String(64))
    printer_type = db.Column(db.String(64))
    serial = db.Column(db.String(64))
    aquired_date = db.Column(db.DateTime)
    vendor_id = db.Column(db.String(64))
    assigned_to = db.Column(db.Integer, ForeignKey('employee.id'))

    def __init__(
                self, brand, model, printer_type, serial, 
                aquired_date, vendor_id, assigned_to):

        self.brand = brand
        self.model = model
        self.printer_type = printer_type
        self.serial = serial
        self.aquired_date = aquired_date
        self.vendor_id = vendor_id
        self.assigned_to = assigned_to


class Phone_Account(Device):
    __tablename__ = 'phone_account'
    __maper_args__ = {'polymorphic_identity': 'phone_account'}

    id = db.Column(db.Integer, ForeignKey('device.id'), primary_key=True)
    phone_number = db.Column(db.String(16))
    phone_model = db.Column(db.String(16))
    phone_os = db.Column(db.String(64))
    notes = db.Column(db.String(255))
    assigned_to = db.Column(db.Integer, ForeignKey('employee.id'))

    def __init__(self, phone_number, phone_model, phone_os, notes, assigned_to):

        self.phone_number = phone_number
        self.phone_model = phone_model
        self.phone_os = phone_os
        self.notes = notes
        self.assigned_to = assigned_to


class Vendors(db.Model):
    __tablename__ = 'vendors'
    vendor_id = db.Column(db.String(64), unique=True, primary_key=True)
    current_rep = db.Column(db.String(96))
    phone_number = db.Column(db.String(16))
    email_address = db.Column(db.String(128))


class Printer_Model(db.Model):
    __tablename__ = 'printer_model'
    printer_model = db.Column(db.String(64), unique=True, primary_key=True)
    brand = db.Column(db.String(64))
    printer_type = db.Column(db.String(64))
