from django.contrib import admin
from .models import Classroom, StudentClassroom, TeacherClassroom, ClassCodes, CreateAssignment, AssignmentCodes, SubmitAssignment, VideoLectures, VideoTest, Lectures, VideoCodes, Post, Reply, PostIds, CreateQuiz, QuizCodes


# Register your models here.
# basically registering and showing all of our models on the admin portal
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('className', 'courseID', 'teacher', 'classTeacherMail', 'classCode')

class StudentClassroomAdmin(admin.ModelAdmin):
    list_display = ('studentEmail',)

class TeacherClassroomAdmin(admin.ModelAdmin):
    list_display = ('teacherEmail',)

class ClassCodesAdmin(admin.ModelAdmin):
    list_display = ('classCode',)

class CreateAssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'submissionDate', 'assignmentCode', 'attachments', 'classroom', 'pinned', 'resource')

class AssignmentCodesAdmin(admin.ModelAdmin):
    list_display = ('assignmentCode',)

class SubmitAssignmentAdmin(admin.ModelAdmin):
    list_display = ('studentEmail', 'attachments', 'assignment', 'submissionDate', 'comment', 'studentEmailAssignmentCode')


class VideoAdmin(admin.ModelAdmin):
    """
    Model storing all classes
    """
    list_display = ('title', 'description', 'videoCode',
                    'link', 'classroom', 'video',)


class VideoTestAdmin(admin.ModelAdmin):
    """
    Model storing all classes
    """
    list_display = ('name', 'videofile',)


class LecturesAdmin(admin.ModelAdmin):
    """
    Model storing all classes
    """
    list_display = ('title', 'description', 'videoCode', 'videoFile', 'classroom', 'excelFile', 'excelFilePath')

class VideoCodesAdmin(admin.ModelAdmin):
    list_display = ('videoCode',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('user1','post_id','post_content','timestamp','classroom',)


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user','reply_id','reply_content','post','timestamp','classroom',)

class PostIdsAdmin(admin.ModelAdmin):
    list_display = ('post_id',)

class CreateQuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'quizDate', 'quizCode', 'quiz', 'classroom', 'pinned',)

class QuizCodesAdmin(admin.ModelAdmin):
    list_display = ('quizCode',)



# registering the models so that we can access them in admin panel
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(StudentClassroom, StudentClassroomAdmin)
admin.site.register(TeacherClassroom, TeacherClassroomAdmin )
admin.site.register(ClassCodes, ClassCodesAdmin )
admin.site.register(CreateAssignment, CreateAssignmentAdmin )
admin.site.register(AssignmentCodes, AssignmentCodesAdmin )
admin.site.register(SubmitAssignment, SubmitAssignmentAdmin )

admin.site.register(VideoLectures, VideoAdmin)
admin.site.register(VideoTest, VideoTestAdmin)
admin.site.register(Lectures, LecturesAdmin)
admin.site.register(VideoCodes, VideoCodesAdmin)


admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(PostIds, PostIdsAdmin)

admin.site.register(CreateQuiz, CreateQuizAdmin)
admin.site.register(QuizCodes, QuizCodesAdmin)









