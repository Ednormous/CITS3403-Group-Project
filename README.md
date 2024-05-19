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


### Future Releases
- Tutor:
  - Access and manage personal timetables. (not yet implemented)
  - Enable permissions to access a students email/phone number.
  - Generate questionares and polls in the message board

- Message Board:
   - Restrict student access to enrolled courses only.
   - Allow pasting of rich text and images.
   - Enable message editing.
   - Enable emoji response to message.
   - Enable tagging users in specific posts.


## Application Architecture

   ### Frontend(Client-Side)
   -   HTML/CSS/JavaScript: Used for web page structure, styling and interactivity.
   -   Flask Templates (jinja2): Allows dynamic interaction with the backend.
   -   WebSocket: Establishes connectivity between client and server.
   -   Message Board: Dom manipulation handled by JS to update UI during user interactions.

   ### Backend(Server-Side)
   -   Flask: Handles HTTP requests and serves HTML templates and provides RESTful APIs for operations.
   -   Flask-SocketIO: Support and enable real-time bi-directional communication between client and server.
   -   Database: SQLAlchemy used to manage database operations.
   -   WebSocket Event Handlers: Process events, listen and emit responses.
     

## Launch Instructions
To run the app, simply enter in the terminal: 
Set secret key via 'export SECRET_KEY='i_love_agile_web_dev'
> python3 run.py
**or**
> python run.py

**Then** to go a modern web browser and enter http://127.0.0.1:5000


## Test Running Instructions

To test the functionalities of the app, run the following code within the terminal.
To run Unit.py
> python -m unittest tests/unit.py
Selenium.py
> python -m unittest tests/selenium.py

## For Project Markers

A temporary administration login has been provided for the assessment. These login details will be removed on completion of marking.
Feel free to register as a student in order to assess the application capabilites as a client of Tuition Talks.

Administrator
 - Username: Marker
 - Passowrd: Marker

## References

This project includes code and implementation generated with the assistance of GitHub Copilot, OpenAI's ChatGPT, and Stack Overflow.

**Citation:**
GitHub Copilot. "AI-Powered Code Suggestions." GitHub Copilot, GitHub, 2024.
ChatGPT, OpenAI. "Flask Application Development Code Assistance." ChatGPT, OpenAI, 2024.
Stack Overflow. "Community-driven Q&A and Code Solutions." Stack Overflow, Stack Exchange Inc., 2024.

