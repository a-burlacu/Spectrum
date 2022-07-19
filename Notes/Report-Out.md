# Report-Out Presentation

**Wednesday, August 3rd                   **

**11:45am-12:00pm**

***10 min presentation - 5 min for Q&A***

### Department:

Video Delivery

---

### Team Overview:

*Who is your manager?*  David Arganoff, ,Sr. Director, Advertising Platforms

*How big is your team?* 11 people

*What do they do?* 

---

### Assigned Project:

*What were you asked to work on during your 10 weeks with Spectrum?*

<u>**POIS**</u> - Placement Opportunity Information System

​	-Developed by 3rd party (Cadent Technologies)

​	-Takes requirements from TV programmer, cross checks signal to see if encoder functions properly

​	-Makes changes (if any) then replaces signal with new signal that reflects changes

​	-Can Create, Replace, Delete

​	-All calls through encoder to POIS is through an API

<u>**AC Blackouts</u>** - Alternative Content/Advertising

​	-Take feed info and programmer requirements (XML,224...)

​	-Change data to reflect ad-insertion 

​	-Create blackouts for regional/subscription-based content

<u>iPOIS</u>- Intelligent POIS

​	-created by Charter/Spectrum 

​	-must be backwards compatible

​			-able to receive different parameters from different clients

​			-allows outdated data to be processed 

​			-using object oriented programming concepts/overloading

---

**-<u>UI Layer:</u>** user interface (very basic, not pretty) allows data manipulation

​		-Presentation: HTML

​		-Business Logic: JavaScript

​		-Data Access: web API

**-<u>Business Layer:</u>** API layer used to create main methods to act between UI & DB layers

​		-"web API"

​		-Presentation: HTTP controllers

​		-Business Logic: Class libraries, functions/methods for each service provided

​		-Data Access: Persistance Layer 

​	-<u>Persistance Layer:</u> aka "Database Access Layer"

​			-Used to isolate read/write/delete logic from Business Layer

**-<u>DB Layer:</u>** Handles database calls/storage of new data/replacing data

​		-Presentation: SQL Database

​		-Business Logic: DB engine

​		-Data Access: Tables/XML

---

**<u>Server Side Functions:</u>**

-methods

-database access

-Python 

​		<u>-config file:</u>

​				-allows modular programming

​				-a Python file that holds all establishing info that can be changed in the future

​				-so we don't have to keep updating main code documents		

-SQL queries 

-use frameworks (Flask) for web API stuff

**<u>Intermediate Communication:</u>**

"How HTML and Python talk" using 'render_template' method

-render_template('file.html', HTML_variable = Python_variable)

-using Flask/webAPI frameworks to 'route' methods to a certain URL

@app.route("/main", methods=["POST"]) 

def main():

​	 make a Python function that handles the actionable items on the main page of site 



**<u>Client Side Functions:</u>**

-UI

-validation of server requests 

​		-JavaScript will check if inputs are correct using methods before making server request (POST, GET, etc.)

-JavaScript, HTML, CSS

​		<u>HTML file:</u>

​				-<head> contains style & script code (JavaScript)

​				-<body> contains forms that take user data & refer to JavaScript methods to validate

-display data from database

---

### Key Takeaways:

*What are some key lessons learned (either functional/technical or interpersonal/professional development) from your 10 weeks with Spectrum?*