## 1. Create new GitHub Repo and connect it to Google Cloud

* Create new GitHub repo:
  https://github.com/wizzard262/python-server-ryhs

* Login to Google Cloud Console:
  https://console.cloud.google.com/ (Project: Development)

* Go to:
  Cloud Run → Create Service → Deploy from source

* Choose:
  "Continuously deploy from a repository"

* Connect GitHub via Developer Connect (in Google Cloud):
  - Authorise GitHub
  - Select the "python-server-rhys" repo

* Build Type:
  "Go, Node.js, Python, Java, .NET Core, Ruby or PHP via Google Cloud's buildpacks"

  **Note:** Buildpacks automatically create a container image.  
  This means the Python code must run a real web server itself.  
  We use **Flask**, a lightweight Python web framework.

* Runtime:
  Select **Python** (this is for Buildpacks, not Cloud Run Functions)

* Service name:
  python-server-rhys

* Allow public access

* Deployment URLs (ryhs:todo: repalce with the new URLS)
  - https://python-server-git-576465670226.europe-west1.run.app/ (homepage)
  - https://python-server-git-576465670226.europe-west1.run.app/status

## 2. Python web server code (Flask)

Inside the GitHub repo, create these two files in the repo root:

* **main.py**  
This file contains the Flask application that Cloud Run will run.  
Flask listens on the $PORT environment variable provided by Cloud Run.  
_(See main.py in this repo for the actual server code.)_

* **requirements.txt**  
This file lists Python dependencies.  
Because Buildpacks generate the container automatically, you only need:  
```flask```  
_(Add any other packages here if needed.)_

## 3. Automatic redeploy

Every push to the GitHub branch triggers Cloud Build:
  - Cloud Build rebuilds the container using Buildpacks
  - Cloud Run redeploys the updated service automatically

No Dockerfile required.  
No manual container configuration needed.

## 4. Run it locally (Windows)
1. Download Python from https://www.python.org/downloads/
      Run the installer.  
      _(typically installs to C:\Users\jones\AppData\Local\Python\)_
      IMPORTANT: Tick “Add Python to PATH”.  (so it runs from any filepath)
      Open Command Prompt (Powershell as Admin) and check it works:  ```python --version```  

Open a terminal (Powershell as Admin): 

2. Install Flask:	 
  Change to the local project folder: ```cd C:\DEV\Repositories\GitHub\python-server```  
    Run ```pip install -r requirements.txt```  
	_(reads what is needed from the requirements file and installs all the Python packages listed in the file )_  
  PIP is Python’s official package installer and dependency manager.

3. Run the server locally:
   ```python main.py```

4. Open in browser, it tell us it is running at both:  
 - Running on http://127.0.0.1:8080  
 - Running on http://192.168.1.177:8080  
 
and also for status:  
- Running on http://127.0.0.1:8080/status  
- Running on http://192.168.1.177:8080/status  