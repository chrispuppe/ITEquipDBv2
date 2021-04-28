from app import db
from app import models
import csv

# commandline in python works
# computer2 = models.Computers('RMLT17','Dell','Latitude D830','7RMTMG2','Laptop','XP Pro','Keep XP','2008-06-25',999,'',3,1)
# db.session.add(computer2)
# db.session.commit()
# db.session.close()

import_computers = './migration/ImportComputers.csv'

# open CSV file 
with open(import_computers, 'rb') as open_file:
	reader = csv.reader(open_file)
	# extract all info from CSV in a two dimensional list
	list_of_computers_atributes = list(reader)

list_of_computer_objects = []

for i in list_of_computers_atributes:
	if 'computer_name' in i[0]:
		pass
	elif 'HQLT11' in i[0]:
		comp = "'{0}'".format("','".join(i))
		print comp
		computerH = models.Computers(comp)
		# list_of_computer_objects.append(computerH)
	else:
		pass

# for computer in list_of_computer_objects:
# 	print computer


# create empty list to house computer objects to be inserted into db

# for list of rows in two dimensional list:
	# for attributes in rows:
		# find employee_id from employee.name in assigned_to column
		# create computer object from row attributes
		# add computer object to the "empty list to house computer objects"

# for computer_object in "full list to house computer objects":
	# db.session.add(computer_object)
	# db.session.commit()

# db.session.close()

# print "completed successfully!"