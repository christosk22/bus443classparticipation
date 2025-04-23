from django.db import models

# Create your models here.

# create table facultydetails (
#   facultyid int primary key,
#   facultyname varchar(100),
#   facultyage int,
#   facultyresearch text);

# If a class does not have a primary key field, Django will create a new column/field named id and make
# that the default primary key column/field

class Facultydetails(models.Model):
    facultyid = models.IntegerField(primary_key=True)
    facultyname = models.CharField(max_length=100)
    facultyage = models.IntegerField()
    facultyresearch = models.TextField()

class Awarddetails(models.Model):
    awardtype = models.CharField(max_length=100)

class Nominationdetails(models.Model):
    facultyname = models.CharField(max_length=100)
    awardtype = models.CharField(max_length=100)
