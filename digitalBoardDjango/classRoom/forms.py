from django import forms
from django.forms.widgets import NumberInput # for displaying calendar

from .models import VideoTest

# form for creating class using form api
class CreateClassRoom(forms.Form):
    class_Name = forms.CharField(max_length=100, required=True)
    course_ID = forms.CharField(max_length=50, required=True)

# form for joining class using form api
class JoinClassRoom(forms.Form):
    class_Code = forms.CharField(max_length=6, required=True)

# form for creating assignment using Forms api
class CreateAssignmentForm(forms.Form):
    title = forms.CharField(max_length=254, widget=forms.TextInput(
        attrs={
        'class':'form-control',
        }
    ))
    description = forms.CharField(max_length=400, required=False,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            }
    ))
    submission_date = forms.DateField(widget=NumberInput(
        attrs={
            'type': 'date',
            'class':'form-control',
            }
    ))
    attachments = forms.FileField(max_length=200, required=False, widget=forms.ClearableFileInput(
        attrs={
        'class':'form-control-file',
        }
    ))

    pin_item = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    resource = forms.BooleanField(required=False, widget=forms.CheckboxInput())

# form for submitting assignment using Forms api
class SubmitAssignmentForm(forms.Form):
    attachments = forms.FileField(max_length=200, required=True, widget=forms.ClearableFileInput(
        attrs={
        'class':'form-control-file',
        }
    ))

    comment = forms.CharField(max_length=254, required=False,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            }
    ))


# for gpt3

class Question(forms.Form):
    """
        # form for creating class using form api
    """
    question = forms.CharField(max_length=300, required=True, 
                                widget=forms.TextInput(attrs={'placeholder': 'Ask Me Anything',
                                                               'class': 'form-control'}))


# for video upload


class VideoForm(forms.ModelForm):
    class Meta:
        model= VideoTest
        fields= ["name", "videofile"]



# form for creating assignment using Forms api
class AddVideoForm(forms.Form):
    title = forms.CharField(max_length=254, widget=forms.TextInput(
        attrs={
        'class':'form-control',
        }
    ))
    description = forms.CharField(max_length=400, required=False,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            }
    ))
    
    videoFile = forms.FileField(max_length=200, widget=forms.ClearableFileInput(
        attrs={
        'class':'form-control-file',
        }
    ))

class AddQuestionsForm(forms.Form):
    excel_File = forms.FileField(max_length=200, required=True, widget=forms.ClearableFileInput(
        attrs={
        'class':'form-control-file',
        }
    ))

class CreateQuizForm(forms.Form):
    title = forms.CharField(max_length=254, widget=forms.TextInput(
        attrs={
        'class':'form-control',
        }
    ))
    date_of_quiz = forms.DateField(widget=NumberInput(
        attrs={
            'type': 'date',
            'class':'form-control',
            }
    ))
    quiz = forms.URLField(widget=forms.URLInput(
        attrs={
        'class':'form-control',
        }
    ))

    pin_item = forms.BooleanField(required=False, widget=forms.CheckboxInput())
