from app import db
from app import models
import csv

# commandline in python works
# computer2 = models.Computers('RMLT17','Dell','Latitude D830','7RMTMG2','Laptop','XP Pro','Keep XP','2008-06-25',999,'',3,1)
# db.session.add(computer2)
# db.session.commit()
# db.session.close()

import_fob = './migration/ImportFob.csv'

# open CSV file 
with open(import_fob, 'rb') as open_file:
    reader = csv.reader(open_file)
    # extract all info from CSV in a two dimensional list
    list_of_fob_atributes = list(reader)

list_of_fob_objects = []

for i in list_of_fob_atributes:
    if 'computer_name' in i[0]:
        pass
    else:
        # fob = "'{0}'".format("','".join(i))
        # print fob
        fob1 = models.Fob(i[0], i[1], i[2])
        list_of_fob_objects.append(fob1)
    # else:
    #     pass

for fob in list_of_fob_objects:
    db.session.add(fob)
    db.session.commit()


# create empty list to house computer objects to be inserted into db

# for list of rows in two dimensional list:
    # for attributes in rows:
        # find employee_id from employee.name in assigned_to column
        # create computer object from row attributes
        # add computer object to the "empty list to house computer objects"

# for computer_object in "full list to house computer objects":
    # db.session.add(computer_object)
    # db.session.commit()

db.session.close()

print "Completed Successfully!"