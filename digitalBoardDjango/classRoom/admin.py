from django.contrib import admin
from .models import Classroom, StudentClassroom, TeacherClassroom, ClassCodes, CreateAssignment, AssignmentCodes, SubmitAssignment, VideoLectures

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


# registering the models so that we can access them in admin panel
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(StudentClassroom, StudentClassroomAdmin)
admin.site.register(TeacherClassroom, TeacherClassroomAdmin )
admin.site.register(ClassCodes, ClassCodesAdmin )
admin.site.register(CreateAssignment, CreateAssignmentAdmin )
admin.site.register(AssignmentCodes, AssignmentCodesAdmin )
admin.site.register(SubmitAssignment, SubmitAssignmentAdmin )

admin.site.register(VideoLectures, VideoAdmin)



