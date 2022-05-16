"""
List of Models
"""

from datetime import date
from django.db import models
from  embed_video.fields  import  EmbedVideoField

# for forum
from django.contrib.auth.models import User
from django.utils.timezone import now


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



# here by using upload_to='videos/' creates a subdirectory in aws bucket
# this is very very helpful
class VideoTest(models.Model):
    name= models.CharField(max_length=500)
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.videofile)


class Lectures(models.Model):
    """ List of Assignments """
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    videoCode = models.CharField(max_length=10)
    videoFile= models.FileField(upload_to='videos/', null=True, verbose_name="")
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)
    excelFile = models.FileField(max_length=200, null = True)
    excelFilePath = models.CharField(max_length = 700, null = True)

class VideoCodes(models.Model):
    """ List of Assignmnet Codes used so far"""
    videoCode = models.CharField(max_length=10, unique=True)


#discussion forum classes
class Post(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post_id = models.CharField(max_length=10)
    post_content = models.CharField(max_length=5000)
    timestamp= models.DateTimeField(default=now)
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)
    
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    reply_id = models.AutoField
    reply_content = models.CharField(max_length=5000) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default='')
    timestamp= models.DateTimeField(default=now)
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)

class PostIds(models.Model):
    """ List of Assignmnet Codes used so far"""
    post_id = models.CharField(max_length=10, unique=True)
    