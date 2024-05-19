# 2024 Semester 1 CITS3403 Agile Web Development Project

## Members
| UWA Student ID | Name           | GitHub Username |
|--------|----------------|-----------------|
| 23405978 | Edward Wang       | Ednormous         |
| 23434755 | Wesley Dutton     | wdATuwa           |
| 23401014 | Lucca Sidey    |  Lucca-Sidey     |
| 23661719 | Joshua Trainer  |  Josh-Trainer    |

## Application Overview

Run before running the app.py:

> pip install -r requirements.txt
**or**
> pip3 install -r requirements.txt

The Class Allocation System is a web-based application designed for a tuition center to streamline the process of class management and communication between administrators, tutors, parents, and students. Built using a modern technology stack that includes HTML, CSS, Flask, AJAX, jQuery, and SQLite, the system offers a responsive, secure, and user-friendly platform.

The core functionality of this app is to allow public users to gain an overview of the enterprise and allows registered users to communicate with their dedicated tutors in regards to in-class problems or any homework issues which may arise. 

**Each user role:**
- Administrator 
- Tutor
- Student
has access to a tailored dashboard that presents relevant functionalities and information, ensuring an intuitive and efficient user experience.
   
## Design and Functionality

The app has three dashboards for the different user roles:
- Public users
- Registered users
- Administrator

The public dashboard displays enterprise informations, allowing unregistered users to gain an insight on the services offered at Tuition Talks. Users are able to interact with the navigation bar to access different aspects of the dashboard, including the Homepage, About, Contacts, Login and Register pages. 

The private dashboard offers a tailored experience for every user. Including displaying different user and forum information for each registered users. They have access to the forums based on their enrollment status. It allows for user - user interactions and past interactions are saved in the database in case users would like to refer back to their previous interactions.

The Administrator dashboard is specific to the administrator from the enterprise. The dashboard allows the administrator view **all** forum pages, **delete** any messages, **create** and **delete** user accounts as well as enrolling students in their respective units (not yet implemented). 

### Administrator

- **Permissions**: Full system access with capabilities to manage users, classes, and schedules.
- **Functions**:
  - User management: View, create and delete user accounts.
  - Class management: Add, edit, delete classes; manage enrollments. (not yet implemented)
  - Timetable management: Oversee and adjust the master timetable. (not yet implemented)

### Tutor

- **Permissions**: Access to class-related functionalities and communication with students.
- **Functions**:
  - Provide student feedback
  


### Student

- **Permissions**: Access to personal academic information and communication channels.
- **Functions**:
  - View personal class timetable.
  - Receive feedback and grades from tutors.
  - Communicate with tutors for academic inquiries 


### Future Release
- Tutor:
  - Access and manage personal timetables. (not yet implemented)

- Message Board:
   - Restrict student access to enrolled courses only.
   - Allow pasting of rich text and images.
   - Enable message editing.
   - Enable emoji response to message.
   - Enable tagging users in specific posts.


## Application Architecture




## Launch Instructions
To run the app, simply enter in the terminal: 
> python3 run.py
**or**
> python run.py

**Then** to go a modern web browser and enter http://127.0.0.1:5000


## Test Running Instructions

To test the functionalities of the app, 

## For Project Markers

A temporary administration login has been hardcoded into the database enabling assessment of Administrator functions. These login details will be removed on completion of marking.
 - Username: Marker
 - Passowrd: Marker
 - Email: Marker@Marker.com
