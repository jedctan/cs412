'''
File: models.py
Description: Define data models for Voter Analytics Application.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-04-03
'''

from django.db import models

# Create your models here.

class Voter(models.Model):
    '''
    Store/represent the data for one registered voter in Newton, MA
    Last Name, First Name, Street Number, Street Name, Apartment Number, Zip Code, Date of Birth,
    Date of Registration, Party Affiliation, Precinct Number
    '''

    last_name = models.TextField()
    first_name = models.TextField()
    dob = models.DateField()
    registration_date = models.DateField()
    party = models.CharField(max_length=2)
    precinct_num = models.CharField(max_length=2)
    voter_score = models.IntegerField()

    # residential address
    street_num = models.IntegerField()
    street_name = models.TextField()
    apartment_num = models.TextField() # can have letters, ex: 606E
    zip_code = models.IntegerField()

    # recent elections
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'

def load_data():
    '''Function to load data records from CSV file into the Django database.'''

    filename  = '/Users/jedct/OneDrive/Documents/data/newton_voters.csv'
    f = open(filename, 'r') # open the file for reading

    # discard headers
    f.readline() # do nothing with it   

    Voter.objects.all().delete()
 
    # read entire file
    for line in f:

        try:
            # line = f.readline()
            fields = line.strip().split(',')
            # for i in range(len(fields)):
                # print(f'fields[{i}] = {fields[i]}')

            voter = Voter(
                last_name = fields[1],
                first_name = fields[2],
                street_num = fields[3],
                street_name = fields[4],
                apartment_num = fields[5],
                zip_code = fields[6],
                dob = fields[7],
                registration_date = fields[8],
                party = fields[9],
                precinct_num = fields[10],
                v20state = True if fields[11] == "TRUE" else False,
                v21town = True if fields[12] == "TRUE" else False,
                v21primary = True if fields[13] == "TRUE" else False,
                v22general = True if fields[14] == "TRUE" else False,
                v23town = True if fields[15] == "TRUE" else False,
                voter_score = fields[16]

            )

            voter.save() # commit to the database

            print(f'{voter}')
        except:
            print("Something went wrong!")
            print(f'line={line}')

    print(f'Done. Created {len(Voter.objects.all())} Results.')



        
    