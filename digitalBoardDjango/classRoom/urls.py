"""
List of URL definitions
"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('about-us/', views.aboutUs, name='aboutus'),
    path('classroom/', views.classRoom, name='classroom'),
    path('createclass/', views.createClass, name='createclass'),
    path('joinclass/', views.joinClass, name='joinclass'),
    path('todo/', views.to_do_list, name='todo'),
    path('requestaccess/', views.sendEmail, name='requestaccess'),
    path('classroomcontent/<str:classId>/', views.viewClassRoom, name='classroomcontent'),
    path('classroomcontent/<str:classId>/createassignment/', views.createAssignment,
    name='createassignment'),
    path('classroomcontent/<str:classId>/<str:taskCode>/', views.submitAssignment,
    name='submitassignment'),
    path('classroomcontent/<str:classId>/<str:taskCode>/viewsubmissions', views.viewSubmissions,
    name='viewSubmissions'),

    path('classroomcontent/<str:classId>/videoLectures', views.viewVideos, name='viewvideos'),
    path('classroomcontent/<str:classId>/videoLectures/<str:videoId>/', views.video, name='video'),




]
