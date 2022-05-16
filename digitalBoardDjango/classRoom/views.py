from __future__ import print_function
from fileinput import filename
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import CreateClassRoom, JoinClassRoom, CreateAssignmentForm, SubmitAssignmentForm, Question, AddVideoForm, AddQuestionsForm

from .models import Classroom, StudentClassroom, TeacherClassroom, ClassCodes, AssignmentCodes, CreateAssignment, SubmitAssignment, VideoLectures, Lectures, VideoCodes, Post, PostIds, Reply
from django.contrib import messages
# for sending email to grant teaccher access
from django.conf import settings
from django.core.mail import send_mail

# for generating the class code
import random
import string

# for sorting to do list
from operator import attrgetter

# for downloading sample excel
from django.http import FileResponse, Http404

# for gpt3
from .key import returnKey
import openai
from .gpt import GPT
from .gpt import Example
import pandas as pd

# helps to generate an alphanumeric classcode of given length
def getClassCode(length):
    # With combination of lower and upper case letters and digits
    characters = string.ascii_letters + string.digits
    classCode = ''.join(random.choice(characters) for i in range(length))
    return classCode

# returns the home page
def index(request):
    return render(request, "index.html")
# returns the about us page
def aboutUs(request):
    return render(request, "aboutUs.html")

# returns the page containing a list of all classes you are part of
def classRoom(request):
    if request.user.is_authenticated:
        # if the person is a teacher
        if request.user.is_staff:
            teacherEMail = request.user.email
            listOfClasses = None # stores classes the teacher teaches
            listOfClassesAsStudents = None # stores the classes the teacher is a part of as a student
            try:
                # fetch all the classrooms the teacher teaches
                obj = TeacherClassroom.objects.get(pk = teacherEMail)
                # print(obj)
                # print(list(obj.classTeacherMail.all()))
                listOfClasses = list(obj.classTeacherMail.all())
            except:
                print("No classrooms exist yet")

            try:
                # fetch all the classrooms the teacher has joined as a student
                obj = StudentClassroom.objects.get(pk = teacherEMail)
                # print(obj)
                # print(list(obj.classTeacherMail.all()))
                listOfClassesAsStudents = list(obj.classTeacherMail.all())
            except:
                print("No classrooms in which you exist as student yet")    

            return render(request, 'classRoom.html', {
                                                    'listOfClasses': listOfClasses,
                                                    'listOfClassesAsStudents' : listOfClassesAsStudents,
                                                    })
        else:
            # this is when the user is a student
            studentEmail = request.user.email
            listOfClasses = None # stores the classes in which the student studies
            try: # fetch all the classes the student studies in
                obj = StudentClassroom.objects.get(pk = studentEmail)
                # print(obj)
                # print(list(obj.classTeacherMail.all()))
                listOfClasses = list(obj.classTeacherMail.all())
            except:
                print("No classrooms exist yet")    

            return render(request, 'classRoom.html', {
                                                    'listOfClasses': listOfClasses,
                                                    })
    else:
        return HttpResponseRedirect('/')

# function responsible for creating a class
# can only be used by the teacher
def createClass(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            fm = CreateClassRoom(request.POST)
            if fm.is_valid():

                # filtering out the data received from the form
                className = fm.cleaned_data['class_Name']
                courseID = fm.cleaned_data['course_ID']
                teacher = request.user.email # getting the mail id of user which is attached to the request
                primaryKey = className + "_" + teacher # creating the primary key using mailid of teacher and name of class
                classCode = getClassCode(6) # generating the classcode of length 6

                # checking if classCode generated is unique or not
                # keep on generating a new classcode till we get a unique classcode
                try:
                    classCode = ClassCodes.objects.get(classCode = classCode)
                    try:
                        while(ClassCodes.objects.get(classCode = classCode)):
                            classCode = getClassCode(6)
                    except:
                        print("Yayy, we got a unique class code")
                except:
                    print("Yayy, we got a unique class code")

                # saving it to the classCodes database
                classCodeObj = ClassCodes(classCode = classCode)
                classCodeObj.save()
                
                # making an entry into the database of classrooms
                classRoomObj = Classroom(className = className,
                                  courseID = courseID,
                                  classCode = classCode,
                                  teacher = teacher,
                                  classTeacherMail = primaryKey)
                classRoomObj.save()

                # adding this particular classroom to the list of classrooms taught by that particular teacher
                # whose session is currently active
                teacherObj = TeacherClassroom(teacherEmail = teacher)
                teacherObj.save()
                teacherObj.classTeacherMail.add(classRoomObj)
                teacherObj.save()

                return HttpResponseRedirect('/classroom/')
        else: # when the request is get request
            fm = CreateClassRoom()
            return render(request, 'createClass.html', {'form': fm,})
    else: # when user is unauthenticated or not staff
        return HttpResponseRedirect('/')


# function responsible for joining a class
# can be used by both teacher and student
def joinClass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = JoinClassRoom(request.POST)
            if fm.is_valid():

                # filtering out the data received from the form
                classCode = fm.cleaned_data['class_Code']
                strClassCode = classCode # maintaing a copy of classCode in string format to be used later
                studentEmail = request.user.email

                try: # checking is class code is a valid class code
                    classCode = ClassCodes.objects.get(classCode = classCode) # getting the classcode object means its a valid class code
                    # creating and saving a student object having that particular mail id
                    studentObj = StudentClassroom(studentEmail = studentEmail)
                    studentObj.save() 
                    # fetching the classroom from Classroom db having that particular class code
                    classRoomObj = Classroom.objects.get(classCode = strClassCode)
                    # adding the classroom to the list of classes in which the student/teacher studies in
                    studentObj.classTeacherMail.add(classRoomObj)
                    studentObj.save()
                    return HttpResponseRedirect('/classroom/')
                except: # if we get an invalid class code
                    messages.warning(request, 'Please enter a correct classcode')
                    return HttpResponseRedirect('/joinclass/')
        else:
            fm = JoinClassRoom()
            return render(request, 'joinClass.html', {'form': fm,})
    else:
        return HttpResponseRedirect('/')

# function resoponsible for sending email to user that their request has been received
def sendEmail(request):
    if request.user.is_authenticated and not(request.user.is_staff):
        subject = 'Greetings from Digital Board'
        user = request.user
        message = f'Hi {user.username}, thank you for being a part of the Digital Board Community.\nWe have processed your request and we will grant you teacher access if everything checks out fine.\n\nThank You. \nRegards\nTeam DigitalBoard'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, 'sakshamb117@gmail.com' ]
        send_mail( subject, message, email_from, recipient_list )
        return render(request, 'emailSend.html')
    else:
        return HttpResponseRedirect('/')


# returns the page containing a list of all assignments that have been assigned
def viewClassRoom(request, classId):
    if request.user.is_authenticated:
        
            # print(classId)
            # print(type(classId))
            classroom = Classroom.objects.get(classTeacherMail = classId)
            
            listOfAssignments = None #stores a list of all the assignments
            try:
                # fetch all the classrooms the teacher teaches
                assignments = classroom.createassignment_set.all()
                # print(assignments)
                listOfAssignments = list(assignments)
            except:
                print("No assignments exist yet")
            
            context = {
                'class' : classroom,
                'assignments' : listOfAssignments,
            }
            return render(request, 'classroom/classroomContent.html', context)
        
    else:
        return HttpResponseRedirect('/')

# used by teacher to create assignments
def createAssignment(request, classId):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            fm = CreateAssignmentForm(request.POST, request.FILES)
            if fm.is_valid():
                # print(fm)

                # filtering out the data received from the form
                title = fm.cleaned_data['title']
                description = fm.cleaned_data['description']
                submissionDate = fm.cleaned_data['submission_date']
                attachment = fm.cleaned_data['attachments']
                pinned = fm.cleaned_data['pin_item']
                resource = fm.cleaned_data['resource']
                classroom = Classroom.objects.get(classTeacherMail = classId)
                assignmentCode = getClassCode(8)

                if request.user.email != classroom.teacher:
                    messages.error(request, 'You do not have the right permissions. You are a student in this class.')
                    return redirect('classroomcontent', classId=classId)

                
                
                # checking if classCode generated is unique or not
                # keep on generating a new classcode till we get a unique classcode
                try:
                    assignmentCode = AssignmentCodes.objects.get(assignmentCode = assignmentCode)
                    try:
                        while(AssignmentCodes.objects.get(assignmentCode = assignmentCode)):
                            assignmentCode = getClassCode(8)
                    except:
                        print("Yayy, we got a unique class code")
                except:
                    print("Yayy, we got a unique class code")

                # saving it to the classCodes database
                assignmentCodesObj = AssignmentCodes(assignmentCode = assignmentCode)
                assignmentCodesObj.save()
                
                # making an entry into the database of classrooms
                createAssignmentObj = CreateAssignment(
                                  title = title,
                                  description = description,
                                  submissionDate = submissionDate,
                                  attachments = attachment,
                                  assignmentCode = assignmentCode,
                                  classroom = classroom,
                                  pinned = pinned,
                                  resource = resource,
                                  )
                createAssignmentObj.save()
                messages.success(request, 'Assignment Created')
                return redirect('classroomcontent', classId=classId)
            
        else: # when the request is get request
            # print(classId)
            # print(type(classId))
            classroom = Classroom.objects.get(classTeacherMail = classId)
            fm = CreateAssignmentForm()
            context = {
                'class' : classroom,
                'form' : fm,
            }
            return render(request, 'classroom/createAssignment.html', context)
    else: # when user is unauthenticated or not staff
        return HttpResponseRedirect('/')


# used by students to submit the assignment
def submitAssignment(request,classId, taskCode):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = SubmitAssignmentForm(request.POST, request.FILES)
            if fm.is_valid():
                # print(fm)

                # filtering out the data received from the form
                attachment = fm.cleaned_data['attachments']
                comment = fm.cleaned_data['comment']
                assignment = CreateAssignment.objects.get(assignmentCode = taskCode)
                studentEmail =  request.user.email
                studentEmailAssignmentCode = studentEmail + taskCode

                if comment == "":
                    comment = "None"
                
                # making an entry into the database of classrooms
                submitAssignmentObj = SubmitAssignment(
                                  studentEmail = studentEmail,
                                  attachments = attachment,
                                  comment = comment,
                                  assignment = assignment,
                                  studentEmailAssignmentCode = studentEmailAssignmentCode,
                                  )
                submitAssignmentObj.save()

                messages.success(request, 'Your assignment has been submitted. To submit another file, just attach the new file and click on submit again.')
                return redirect('submitassignment', classId = classId, taskCode=taskCode)
            else:
                messages.error(request, 'The submitted file is empty. Please enter another file.')
                return redirect('submitassignment', classId = classId, taskCode=taskCode)


            
        else: # when the request is get request
            classroom = Classroom.objects.get(classTeacherMail = classId)
            assignment = CreateAssignment.objects.get(assignmentCode = taskCode)
            submission = None
            try:
                submission = assignment.submitassignment_set.filter(studentEmail = request.user.email)
                submission = list(submission)
                submission = submission[0]
                # print(submission.attachments.url)
                # print(submission)
            except:
                print("No attachment so far!")
            
            fm = SubmitAssignmentForm()

            context = {
                'assignment' : assignment,
                'class' : classroom,
                'form' : fm,
                'submission' : submission,

            }
            return render(request, 'classroom/submitAssignment.html', context)
    else: # when user is unauthenticated or not staff
        return HttpResponseRedirect('/')

# used by teachers to view submissions made by students
def viewSubmissions(request,classId, taskCode):
    if request.user.is_authenticated and request.user.is_staff:

        listOfSubmissions = None 
#         get the classroom we are in
        classroom = Classroom.objects.get(classTeacherMail = classId)


        try: # try fetching the assignments for that classroom and using many to one relation checking 
#             which assignmens have een submitted
            assignment = CreateAssignment.objects.get(assignmentCode = taskCode)
            submissions = assignment.submitassignment_set.all()
            listOfSubmissions = list(submissions)
        except:
            print("There are no submissions so far!!")


        context = {
            'submissions' : listOfSubmissions,
            'class' : classroom,
        }

        return render(request, 'classroom/viewSubmissions.html', context)
    else: # when user is unauthenticated or not staff
        return HttpResponseRedirect('/')


def to_do_list(request):
    """ Shows a list of all pending assignments """
    if request.user.is_authenticated and not(request.user.is_staff):
        # if the person is a student
        studentEmail = request.user.email
        listOfClasses = None # stores the classes in which the student studies
        listOfAssignments = None # stores all the assignments in each of the classes he studies in
        listOfTasks = None # stores list of pending assignments

        try: # fetch all the classes the student studies in
            obj = StudentClassroom.objects.get(pk = studentEmail)
            listOfClasses = list(obj.classTeacherMail.all())
        except:
            print("No classrooms exist yet")

        try: # fetch all assignments he was assigned
            listOfAssignments = []
            for classes in listOfClasses:
                assignments = classes.createassignment_set.all()
                assignments = list(assignments)
                for task in assignments:
                    listOfAssignments.append(task)
        except:
            listOfAssignments = None
            print("No assignments exist yet")

        try: # keep only those assignments that have not been submitted
            listOfTasks = []
            
            for assignment in listOfAssignments:
                if( assignment.submitassignment_set.filter(studentEmail = request.user.email) ):
                    continue
                else:
                    # print(assignment)
                    listOfTasks.append(assignment)

            # print(listOfTasks)
            listOfTasks.sort(key=lambda r: r.submissionDate) # sort them according to day of submission 
        except:
            listOfTasks = None
            print("We ran into error while populating unsubmitted assignments")


        context = {
            'assignments' : listOfTasks,
        }

        return render(request, 'todoList.html', context)
    else:
        return HttpResponseRedirect('/')




# for video file
from .models import VideoTest
from .forms import VideoForm

def showvideo(request):

    lastvideo= VideoTest.objects.last()

    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    
    context= {'video': lastvideo,
              'form': form
              }
    
      
    return render(request, 'classroom/videotest.html', context)


# used by teacher to create assignments
def addVideo(request, classId):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            fm = AddVideoForm(request.POST, request.FILES)
            if fm.is_valid():
                # print(fm)

                # filtering out the data received from the form
                title = fm.cleaned_data['title']
                description = fm.cleaned_data['description']
                classroom = Classroom.objects.get(classTeacherMail = classId)
                videoCode = getClassCode(10)
                videoFile = fm.cleaned_data['videoFile']


                if request.user.email != classroom.teacher:
                    messages.error(request, 'You do not have the right permissions. You are a student in this class.')
                    return redirect('classroomcontent', classId=classId)

                
                
                # checking if classCode generated is unique or not
                # keep on generating a new classcode till we get a unique classcode
                try:
                    videoCode = VideoCodes.objects.get(videoCode = videoCode)
                    try:
                        while(VideoCodes.objects.get(videoCode = videoCode)):
                            videoCode = getClassCode(10)
                    except:
                        print("Yayy, we got a unique class code")
                except:
                    print("Yayy, we got a unique class code")

                # saving it to the classCodes database
                videoCodesObj = VideoCodes(videoCode = videoCode)
                videoCodesObj.save()
                
                # making an entry into the database of classrooms
                addVideoObj = Lectures(
                                  title = title,
                                  description = description,
                                  videoCode = videoCode,
                                  classroom = classroom,
                                  videoFile = videoFile,
                                  excelFile = None,
                                  excelFilePath = None,
                                  )
                addVideoObj.save()
                messages.success(request, 'Video Uploaded')
                # needs to be updated
                return redirect('viewvideos', classId=classId) 
            
        else: # when the request is get request
            # print(classId)
            # print(type(classId))
            classroom = Classroom.objects.get(classTeacherMail = classId)
            fm = AddVideoForm()
            context = {
                'class' : classroom,
                'form' : fm,
            }
            return render(request, 'classroom/addVideo.html', context)
    else: # when user is unauthenticated or not staff
        return HttpResponseRedirect('/')

# displaying all the video lectures
def viewVideos(request, classId):
    """
        returns the page containing a list of all assignments that have been assigned
    """
    if request.user.is_authenticated:
        classroom = Classroom.objects.get(classTeacherMail = classId)
        listOfVideos = None #stores a list of all the assignments
        try:
            # fetch all the classrooms the teacher teaches
            videos = classroom.lectures_set.all()
            # print(videos)
            listOfVideos = list(videos)
        except:
            print("No video lectures exist yet")

        context = {
            'class' : classroom,
            'videos' : listOfVideos,
        }
        return render(request, 'classroom/classroomVideo.html', context)
    else:
        return HttpResponseRedirect('/')


# function for downloading excel file

def download_sample_file(request):

    if request.user.is_authenticated:
        try:
            
            filename = 'classRoom/databases/sample.csv'
            file =  FileResponse(open(filename, 'rb'), content_type='text/csv', as_attachment= True)
            filename = 'sample.csv'
            file.set_headers(filename)
            return file
        except FileNotFoundError:
            raise Http404()
    else:
        return HttpResponseRedirect('/')

import boto3, os # for downloading csv from s3 bucket
def download_aws(fileName, videoId):
    s3 = boto3.client('s3', 
                       aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'), 
                       aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'))

    currentDir = os.getcwd()
    csvFilename = f"csv_{videoId}.csv"
    currentFileCSV = currentDir +"//" + "databases" + "//" + csvFilename

    print(currentFileCSV)
    print(fileName)


    s3.download_file(os.environ.get('AWS_STORAGE_BUCKET_NAME') , fileName , currentFileCSV)

    videoLecture = Lectures.objects.get(videoCode = videoId)
    videoLecture.excelFilePath = currentFileCSV
    videoLecture.save()



# used by students to submit the assignment


def addQuestions(request, classId, videoId):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = AddQuestionsForm(request.POST, request.FILES)
            if fm.is_valid():
                # print(fm)

                # filtering out the data received from the form
                excelFile = fm.cleaned_data['excel_File']

                print(excelFile)
                print(type(excelFile))
                print()
                
                videoLecture = Lectures.objects.get(videoCode = videoId)
                videoLecture.excelFile = excelFile
                videoLecture.save()

                print(videoLecture.excelFile)
                print(type(videoLecture.excelFile))

                # by specifying filename here, I am able to get the updated filename
                # by default django creates a new version if file with same name is uploaded
                # s3 bucket does not do that

                # so what was happening was that if I defined filename before saving the object, then the filename at that point
                # would be test.csv only(taking example of test,csv)
                # but iw touwld get uploaded as test-some-random-nos.csv to s3 as django would create a new version
                # this was causing problems when I was downloading it back for gpt3
                # so now I defined filename after saving the db object
                # noe it works fine
                fileName = videoLecture.excelFile.name 
                print()
                print(fileName)

                # downnload the file that user just uploaded
                download_aws(fileName, videoId)

                messages.success(request, 'Your questions have been submitted. To submit another file, just attach the new file and click on submit again.')
                return redirect('addquestions', classId = classId, videoId=videoId)
            else:
                messages.error(request, 'The submitted file is empty. Please enter another file.')
                return redirect('addquestions', classId = classId, videoId=videoId)


            
        else: # when the request is get request
            
            fm = AddQuestionsForm()
            videoLecture = Lectures.objects.get(videoCode = videoId)
            classroom = Classroom.objects.get(classTeacherMail = classId)
            # classroom needs to be sent
            # cox using this we are taking out classid
            # which is used to create dynamic url for many of the options inside the header class
            context = {
                'class' : classroom,
                'form' : fm,
                'videoLecture': videoLecture,
            }
            return render(request, 'classroom/addQuestions.html', context)
    else: # when user is unauthenticated or not staff
        return HttpResponseRedirect('/')



# displaying particular video and chatbot
def video(request, classId, videoId):

    if request.method == 'POST':
        
        gpt = gpt_getter(videoId)

        fm = Question(request.POST)
        if fm.is_valid():
            prompt = fm.cleaned_data['question']
            output = gpt.get_top_reply(prompt)
            messages.success(request, output)
            return redirect('video', classId = classId, videoId = videoId)
    else:
        classroom = Classroom.objects.get(classTeacherMail = classId)
        lecture = Lectures.objects.get(videoCode = videoId)

        fm = Question()
        context = {
            'class' : classroom,
            'lecture' : lecture,
            'form' : fm,
        }

        return render(request, 'classroom/video.html', context)




# adding functionality of chatbot(neoBot)

def gpt_getter(videoId):
    openai.api_key = returnKey()
    gpt = GPT(engine="davinci",
            temperature=0.8,
            output_prefix="",
            max_tokens=400)

    # add some code examples
    """This is where our database will be inserted """

    currentDir = os.getcwd()
    csvFilename = f"csv_{videoId}.csv"
    currentFileCSV = currentDir +"//" + "databases" + "//" + csvFilename

    df = pd.read_csv(currentFileCSV)
    print(df.columns)
    # print("Given Dataframe :\n", df)

    # print("\nIterating over rows using index attribute :\n")
    
    # iterate through each row and select 
    # 'Name' and 'Stream' column respectively.
    for ind in df.index:
        #  print(df['Question'][ind], df['Answer'][ind]) #for testing
        question = str(df['Question'][ind])
        answer = str(df['Answer'][ind])
        gpt.add_example(Example(question, answer))

    # returns all the examples that we have fed to the gpt3 model
    # all_examples = gpt.get_all_examples()
    # print(all_examples)
    # print('Science function called')
    return gpt 



# discussion portal

def forum(request, classId):
    #classroom = Classroom.objects.get(classTeacherMail = classId)
    if request.user.is_authenticated:
        classroom = Classroom.objects.get(classTeacherMail = classId)
        if request.method=="POST":   
            try:    
                user = request.user
                content = request.POST.get('content','')
                classroom = Classroom.objects.get(classTeacherMail = classId)
                post_id = getClassCode(10)

                try:
                    post_id = PostIds.objects.get(post_id = post_id)
                    try:
                        while(PostIds.objects.get(post_id = post_id)):
                            post_id = getClassCode(10)
                    except:
                        print("Yayy, we got a unique class code")
                except:
                    print("Yayy, we got a unique class code")

                
                post_idObj = PostIds(post_id = post_id)
                post_idObj.save()
                
                # making an entry into the database of classrooms
                postObj = Post(
                                  user1 = user,
                                  post_id = post_id,
                                  post_content = content,
                                  classroom = classroom,
                                  )
                postObj.save()


                

                posts = Post.objects.filter(classroom = classroom).order_by('-timestamp')

                # posts = classroom.post_set.all()
                # print(assignments)
                # listOfPosts = list(posts)
                alert = True
                context = {
                    'posts' : posts,
                    'class' : classroom,
                    'alert':alert
                }
                
                return render(request, "classroom/forum.html", context)

            except:
                print("No discussions yet")
                context = {
                    'class' : classroom,
                    'alert':alert
                }
                
                return render(request, "classroom/forum.html", context)

           
        else:
            posts = Post.objects.filter(classroom = classroom).order_by('-timestamp')
            context = {
                    'class' : classroom,
                    'posts':posts,
            }
            
            return render(request, "classroom/forum.html", context)
    else:
        return HttpResponseRedirect('/')

def discussion(request, classId, postId):
    classroom = Classroom.objects.get(classTeacherMail = classId)
    post = Post.objects.get(post_id = postId)
    

    listOfReplies = None #stores a list of all the assignments
    try:
        # fetch all the classrooms the teacher teaches
        replies = post.reply_set.all()
        # print(videos)
        listOfReplies = list(replies)
        listOfReplies.sort(key=lambda x: x.timestamp, reverse=True)
    except:
        print("No replies exist yet")



    if request.method=="POST":
        user = request.user
        desc = request.POST.get('desc','')
        post_id =request.POST.get('post_id','')
        reply = Reply(user = user, reply_content = desc, post=post)
        reply.save()
        alert = True
    
        listOfReplies = None #stores a list of all the assignments
        try:
            # fetch all the classrooms the teacher teaches
            replies = post.reply_set.all()
            # print(videos)
            listOfReplies = list(replies)
            listOfReplies.sort(key=lambda x: x.timestamp, reverse=True)
        except:
            print("No replies exist yet")

        context = {
            'alert':alert,
            'class' : classroom,
            'post' : post,
            'replies' : listOfReplies,
        }

        return render(request, "classroom/discussion.html", context)
    else:

        context = {
            'class' : classroom,
            'post' : post,
            'replies' : listOfReplies,
            }

        return render(request, "classroom/discussion.html", context)