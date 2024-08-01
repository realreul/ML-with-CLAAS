# ML-with-CLAAS
## Starting the application
To start the application, follow the commands below:

### Windows:
1. Copy github repo into a folder of your choice
2. Navigate into the folder where you have copied the file into, e.g. cd C:\Users\...\ML-with-CLAAS
3. From there, naviagte into the flask_app folder: cd flask_app
4. Create a new virtual environment called "venv": python -m venv venv (make sure in the pyvenv.cfg file the python version 3.9.18 is stated)
5. Allow virtual environments to be started from your current user account: Set-ExecutionPolicy RemoteSigned
6. Hint: You might need to execute point 5. from a terminal (e.g. Windows PowerShell) executed as admin
7. Activate the virtual environment with the following comand in the .../ML-with-CLAAS/flask_app folder: .\venv\Scripts\activate
8. Then install the requirements in the virtual environment with this comand in the same folder: pip install -r requirements.txt
9. Start the application with: python run.py
You should now be able to access the application under: http://127.0.0.1:5000 . Exit the application with CTRL + C in the terminal.
