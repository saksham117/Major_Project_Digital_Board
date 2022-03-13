"""
List of Models
"""

from datetime import date
from django.db import models
from  embed_video.fields  import  EmbedVideoField


# the field classTeacherMail is a primary key and is formed by concatenating className with
# email id of teacher who created it
class Classroom(models.Model):
    """ List of Classes """
    className = models.CharField(max_length=100)
    courseID = models.CharField(max_length=50)
    teacher =  models.EmailField(max_length=100)
    classTeacherMail = models.CharField(max_length=254, primary_key=True)
    classCode = models.CharField(max_length=10, unique=True)

# classTeacherMail is a foreign key connecting it with the Classroom table
class StudentClassroom(models.Model):
    """ Reacord of Studnets enrolled in a class """
    studentEmail =  models.EmailField(max_length=254, primary_key=True)
    classTeacherMail = models.ManyToManyField(Classroom)


# classTeacherMail is a foreign key connecting it with the Classroom table
class TeacherClassroom(models.Model):
    """ Record of Teachers teaching a class """
    teacherEmail =  models.EmailField(max_length=254, primary_key=True)
    classTeacherMail = models.ManyToManyField(Classroom)


class ClassCodes(models.Model):
    """ List of Classcodes used as of now """
    classCode = models.CharField(max_length=10, unique=True)

# model to store all the assignment uploaded as of now
# linked with classroom model via many to one relationship
class CreateAssignment(models.Model):
    """ List of Assignments """
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    submissionDate = models.DateField()
    assignmentCode = models.CharField(max_length=10)
    attachments = models.FileField(max_length=200, blank=True)
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)
    pinned = models.BooleanField(default=False, blank = True)
    resource = models.BooleanField(default=False, blank = True)

class AssignmentCodes(models.Model):
    """ List of Assignmnet Codes used so far"""
    assignmentCode = models.CharField(max_length=10, unique=True)


# each submission is associated with a particular assignment
# each assignment is further associated with a particular class via Many to One relationships
class SubmitAssignment(models.Model):
    """ List of Assignments submitted by students """
    studentEmail =  models.EmailField()
    attachments = models.FileField(max_length=200)
    assignment = models.ForeignKey(CreateAssignment, null=True, on_delete=models.SET_NULL)
    submissionDate = models.DateField(default=date.today)
    comment = models.CharField(null=True, max_length=254)
    studentEmailAssignmentCode = models.CharField(max_length=254, primary_key=True)


# model to store all the videos uploaded as of now
class VideoLectures(models.Model):
    """ List of Videos """
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    videoCode = models.CharField(max_length=10)
    link = models.URLField()
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)
    video = EmbedVideoField()
