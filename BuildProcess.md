# I've got this python project setup running as in the Readme.md (below):

I want to make the main.py file in several parts:
- basic output
- flask webserver and HTML homepage
- add the status endpoint
- add the weather endpoint

Take me through each of the steps below to make it      
 happen, one  at a time in simple steps.  
I will prompt you for each next step.

------------------------------------------

## CREATE GIT REPO
* I want to create a new remote GIT repository on my
  github account via the web page portal.
* I'll then pull it down locally to a new folder:    
  `C:\DEV\Repositories\GitHub\python-server-rhys`
  
## WRITE PYTHON APP
I then want to replicate the existing Python apps functionality using: 

* **VS Code IDE** _(the Visual Studio app: Code Integrated Development Environment)_
* I have Python installed already and will use **Admin Powershell** to run it.  
	
The python app will:

* Output some basic text output _(then we will throw that away.)_
* Then serve an **HTML** (Hyper Text Markup Language) homepage at the root (/)  
   using Flask _(Pythons Webserver)_
* Then call Open Meteo Weather API from another webpage path ()
 this wll call: https://api.open-meteo.com/v1/forecast?current_weather=true&latitude=53.24&longitude=2.09 and return the result to te web browser as JSON (Java Script Object Notation)

## COMMIT-PUSH TO REMOTE GIT REPO
* I then want to **COMMIT** the code changes into the LOCAL repository.
* I then want to **PUSH** the code changes into the REMOTE repository.

## HOST THE WEB APP
* I then want to connect my existing **Google Cloud Account** and create a new Service:  
called: _python-server-rhys_ to run the web app hosted remotely.