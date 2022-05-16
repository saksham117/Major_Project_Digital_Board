"""
List of URL definitions
"""
from django.urls import path
from . import views

# dynamic urls should always be at the end
# otherwise they cause errors
# also the more dynamic it, the lower it should be placed
urlpatterns = [
    path('', views.index, name = 'index'),
    path('about-us/', views.aboutUs, name='aboutus'),
    path('classroom/', views.classRoom, name='classroom'),
    path('createclass/', views.createClass, name='createclass'),
    path('joinclass/', views.joinClass, name='joinclass'),
    path('todo/', views.to_do_list, name='todo'),
    path('requestaccess/', views.sendEmail, name='requestaccess'),
    path('downloadSample/', views.download_sample_file, name='downloadsample'),


    path('classroomcontent/<str:classId>/', views.viewClassRoom, name='classroomcontent'),
    path('classroomcontent/<str:classId>/createassignment/', views.createAssignment,
    name='createassignment'),

    path('classroomcontent/<str:classId>/videoLectures', views.viewVideos, name='viewvideos'),
    path('classroomcontent/<str:classId>/videoLectures/addVideo/', views.addVideo,
    name='addvideo'),

    # for forum
    path('classroomcontent/<str:classId>/forum/', views.forum, name='forum'),




    path('classroomcontent/<str:classId>/<str:taskCode>/', views.submitAssignment,
    name='submitassignment'),
    path('classroomcontent/<str:classId>/<str:taskCode>/viewsubmissions', views.viewSubmissions,
    name='viewSubmissions'),

    path('classroomcontent/<str:classId>/videoLectures/<str:videoId>/', views.video, name='video'),
    path('classroomcontent/<str:classId>/addQuestions/<str:videoId>/', views.addQuestions,
    name='addquestions'),

    # for discussion
    path('classroomcontent/<str:classId>/discussion/<str:postId>/', views.discussion, name='discussion'),


    path('videotest/', views.showvideo, name='videotest'),





]
