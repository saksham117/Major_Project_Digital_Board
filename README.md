# Digital Board

We are here to make your digital classroom experience as seamless as possible. Our tools make it simple to manage and submit your assignments, view and share study material and resources, keep a track of your pending tasks and help you make most of your remote learning experience.


  


## Contents ##

- [Features](#features)
- [Key Points](#key-points)
- [Walkthrough](#walkthrough)
  - [Student](#student)
  - [Teacher](#teacher) 
- [Getting Started](#getting-started)
- [Final Comments](#final-comments)
- [Bug Reporting](#bug)
- [Feature Request](#feature-request)



<a id="features"></a>

## 🚀 Features

- Teachers can easily upload assignments, set deadlines, share study materials and assign them to students. The students can view & submit these assignments and add comments, if necessary. 
- Teachers can pin important resources at the very start, so that the students don't find it difficult to navigate to them at the time of need.
- Digital Board offers students a to-do list so that they can easily keep a track of what all tasks have been assigned.
- Teachers can view the submissions made by each student for a particular assignment
- By providing easy login and logout capability via Social Accounts, we have removed the hassle of remembering another set of login credentials.
- Although developed as a desktop-first application, Digital Board is fully responsive and will work on screens of all sizes.

<a id="key-points"></a>

## ⭐ Key Points
- ### Logging In 🚪
  - All users, be it teachers or students(in real life) are granted student access only. This makes them unable to create classes and subsequently assignments. This has been implemented as a security feature to prevent anyone from having teaching access.
- ### Teaching Access 👩‍🏫
  - To get teaching access, click on the Request Teacher Access button. An email will be sent to admin as well as to you, indicating that you have requested for teaching access. If everything checks out well and you indeed are a teacher, the admin will grant you teaching access within 24 hours. You need to log out and log in, for the changes to be visible.
- ### Join a Class 🏛
  - In order to join classes and submit assignments, you need to have class codes. Ask your teacher to share it with you. In the meantime you can join these classes, Class Code: b626R4 (Python), Class Code: 9Mxc1T (C++). Class codes are 6 digit alphanumeric unique strings.
- ### Assignments & Study Material 📚
  - The teacher can upload both assignments as well as study materials. Assignments need to be submitted before the deadline. For resources, there are no submissions required. The deadline associated with resources means that teacher expects you to complete them before that date.



<a id="walkthrough"></a>

## 🚶‍♀️ Walkthrough 

So lets take a look at our application.

### Landing Page
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/home_page.png?raw=true)

### About Us
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/about%20us.png?raw=true)

Now click on Login with Google so that you can login into the application using your email id.

### Logging In
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/sign%20in.png?raw=true)

Depending on whether you are a student or you are a teacher, you get different options and tools. So lets explore them.

<a id="student"></a>

### 👨‍🎓 Student 

#### Student Classroom
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/student%20classroom.png?raw=true)

#### Joining a Class
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/student%20join%20class.png?raw=true)

#### Viewing assignment within a class
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/student%20inside%20class.png?raw=true)

#### Submitting Assignment
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/student%20submit%20assignment.png?raw=true)

#### To Do List
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/student%20to%20do.png?raw=true)

#### Requesting Teacher Access
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/student%20teaching%20access.png?raw=true)

<a id="teacher"></a>

### 👩‍🏫 Teacher 

#### Teacher Classroom
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/teacher%20dashboard.png?raw=true)

#### Create Class
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/teacher%20create%20class.png?raw=true)

#### Viewing assignment within a class
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/teacher%20within%20class.png?raw=true)

#### Creating assignments or study materials
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/teacher%20create%20assignment.png?raw=true)

- Specify the title, add an optional description, add day of submision and an optional attachment.
- Check the Pin item checkbox to Pin item to start
- Check the Resource checkbox to create a resource and not an assignment

#### Viewing submitted assignments 
![](https://github.com/saksham117/digitalBoard/blob/main/Screenshots/teacher%20view%20submissions.png?raw=true)


<a id="getting-started"></a>

## 📦 Getting Started

- Fork this repository and clone it in your local environment.
- Create a virtual environment and install relevant packages.
  
  - Go to the desired directory and run the following command in Commmand Prompt:

  ```bash
  pip install virtualenv
  mkdir python-virtual-environments && cd python-virtual-environments
  python3 -m venv name_of_venv
  name_of_venv\Scripts\activate
  pip -r requirements.txt
  ```

  - Here the folder python-virtual-environments contains your virtual environment. Ideally place this folder in a central location like C:\Users\username. This will then maintain all your virtual environments.
  - name_of_venv can be any thing which you want to set as the name of your virtual environment.
  - Activate that environment and install requirements.txt
  - Then navigate back to the directory where you cloned this repo
  
  
- Go to web/settings.py and make the following changes in these lines of code.

  ```python
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
  }
  ```

  - In NAME field specify the name of the database (create one, if not already present).
  - In user specify which user of MySQL you want to connet with and specify the password for that user.

- You might also have to change the environment variables for setting AWS S3 bucket and email configuration. Follow these links to set environment variables:
  -  [Windows](https://youtu.be/IolxqkL7cD8)
  -  [MacOS/Linux](https://youtu.be/5iWhQWVXosU)

- To set google authentication, follow this resource 
  -  [Set up Google Authentication](https://www.section.io/engineering-education/django-google-oauth/)

- Now after having the virtual environment activated, run the command:
  ```python
   python manage.py runserver
  ```

- To create a superuser to access admin portal, write the following commands:
  ```python
   python manage.py createsuperuser
  ```

<a id="final-comments"></a>
## 🙏 Final Comments

- While implementing the project, it was ensured that the best practices of agile methodolgy were followed.
- While loggin in, you sometimes might get this error **Error 400: redirect_uri_mismatch** . This happens as Heroku and Google OAuth are not always able to communicate. Just go back and try to log in again. The error will disappear.
  
<a id="bug"></a>

## 🐛 Bug Reporting

Feel free to [open an issue](https://github.com/saksham117/Major_Project_Digital_Board/issues) on GitHub if you find any bug.

<a id="feature-request"></a>

## ⭐ Feature Request

- Feel free to [Open an issue](https://github.com/saksham117/Major_Project_Digital_Board/issues) on GitHub to request any additional features you might need for your use case.

  

  
 

  

