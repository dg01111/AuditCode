'''
Author: Danielle Gorman
Date: 21 Nov 2022
Purpose: This is a Python file which will be provisional for the web-app dependencies to include routes to web pages, functions of database storages, retrievals, deletions of data and display of data throughout the web-app.
'''
'''
#Importations of dependencies to be used throughout the Python code as required.
'''
#Import flask dependencies.
from flask import Flask, render_template, request, redirect, url_for, session

#Import database dependencies (sqlite3).
import sqlite3

#Import to get date and time.
from datetime import datetime

#POST data requests.
import requests

#Flask dependency to run Flask app.
app = Flask(__name__)

#Session variables require secret_key.
app.secret_key = '4jsk6SRCRjls7'

'''
Purpose: The "adminlogin()" function returns the login web-page for administrative users of the ALS-API web-app system. Login credentials have been provided in the sqlite3 database "alsDB.db" located in the "adminLogin" table.
'''
@app.route('/admin/', methods=['GET', 'POST']) 
@app.route('/admin/login', methods=['GET', 'POST'])
def adminlogin():
    
    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database 
    cursor = mydb.cursor()
    
    '''
    Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
    '''

    #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
    sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
    
    #Execute the "sqlQ" query.
    cursor.execute(sqlQ)

    #Access the current datetime. 
    logDate = datetime.now()
    
    #Provide a log message upon accessing the route with information of the specific action taken on the route.
    logMessage = "Accessed /admin/login route. "
    
    #Provide a category for the ability to search based on action of the log.
    logCategory = "Admin login web-page accessed.."
    
    #Provide which section of the web-app was accessed.
    logUser = "User Unknown - Not Logged In"
    
    #Provide the location where the log was entered.
    logLocation = "/admin/login"
    
    #Insert the log data into the "messageLogs" database.
    cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
    
    #Commit the log to the "alsDB.db" database.
    mydb.commit()
    
    #Render the "admin/login.html" web-page to provide a login form for the administrative user to access the administrative user part of the web-app system.
    return render_template('admin/login.html')

'''
Purpose: The adminhome() function retrieves the login credentials provided from the admin/login.html web-page form. If proper credentials have been provided by the admin user then access is given to the admin user and the admin/loggedin/home.html page is rendered. If incorrect login credentials are provided on the admin/login.html web-page then appropriate messages are provided on the admin/login.html web-page. Login credentials have been provided in the sqlite3 database "alsDB.db" located in the "adminLogin" table.
'''
@app.route('/admin/loggedin/home', methods=['GET', 'POST']) 
def adminhome():

    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
    cursor = mydb.cursor()
    
    '''
    Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
    '''

    #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
    sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
    
    #Execute the "sqlQ" query.
    cursor.execute(sqlQ)

    #Access the current datetime. 
    logDate = datetime.now()
    
    #Provide a log message upon accessing the route with information of the specific action taken on the route.
    logMessage = "Connected to database. Attempted to access /admin/loggedin/home route."
    
    #Provide a category for the ability to search based on action of the log.
    logCategory = "Database"
    
    #Provide which section of the web-app was accessed.
    logUser = "User Unknown - Not Logged In"
    
    #Provide the location where the log was entered.
    logLocation = "/admin/loggedin/home"
    
    #Insert the log data into the "messageLogs" database.
    cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
    
    #Commit the log to the "alsDB.db" database.
    mydb.commit()
    
    #If the requested "loginForm" on the "admin/login.html" web-page has been submitted then check for correct credentials within the databases adminLogin table, otherwise the user will be redirected to the "admin/login.html" web-page. 
    if request.args.get('f') == 'adminLogin':
        
        #Store the username from admin/login.html web-page adminLogin form in adminUsername variable.
        adminUsername = request.form['adminUsername']
        
        #Store the password from admin/login.html web-page adminLogin form in adminPassword variable.
        adminPassword = request.form['adminPassword']
        
        #Provide a SELECT query on the adminLogin table to check if credentials provided on the adminLogin form are present within the adminLogin table to provide access to the "admin/loggedin/home.html" web-page if matching credentials are found from the username and password inputs provided by the user from the "admin/login.html" web-page.
        sqlQ = "SELECT * FROM adminLogin WHERE username = ? AND password = ?"
        
        #Execute the "sqlQ" query with the provided "adminUsername" and "adminPassword" variables and if found in the databses then provide access for that admin user to the "admin/loggedin/home.html" web-page.
        cursor.execute(sqlQ,(adminUsername, adminPassword,))
        
        #The "rows" variable uses the "len" module to provide how many rows of data were found when the sqlQ query was executed so that the user can be provided either access to the "admin/loggedin/home.html" if the proper credentials have been provided on the adminLogin form from the variables of the admin username and password provided by hte user on the "admin/login.html" web-page. 
        rows = len(cursor.fetchall())
        
        #Render the "admin/loggedin/home.html" web-page to the administrator if credentials matching the credentials provided are found using the executed "sqlQ" query.
        if rows > 0:
        
            #Create a session variable to retain the administrator username while the administrator is navigating within the "admin/loggedin/" section of the web-app system.
            session['adminUsername'] = adminUsername
            
            #Create a session variable "session['adminLoggedIn']" initialised to True to check if the administrative user is logged in to allow access to each web-page of the system which requires the administrative user to be logged in.
            session['adminLoggedIn'] = True
                        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database 
            cursor = mydb.cursor()
            
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''

            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            ##Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "Administrator with the username " + adminUsername + " successfully logged in. Access granted to /admin/loggedin/home."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "Admin Login"
            
            #Provide which section of the web-app was accessed.
            logUser = session['adminUsername']
            
            #Provide the location where the log was entered.
            logLocation = "/admin/loggedin/home"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
    
            #Commit the log to the "alsDB.db" database.
            mydb.commit()

            #Allow the administrator access to the "admin/loggedin/home.html" web-page.
            return render_template('admin/loggedin/home.html', _adminUsername = session['adminUsername'])
            
        #If no admin username and password matching the username and password provided on the adminLogin form from the "admin/login.html" web-page then provide an error message regarding the incorrect details on the "admin/login.html" web-page.
        elif rows == 0:
            
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''

            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "Incorrect administrative username/password entered. Redirected to /admin/login route."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "Incorrect administrator credentials entered."
            
            #Provide which section of the web-app was accessed.
            logUser = session['adminUsername']
            
            #Provide the location where the log was entered.
            logLocation = "/admin/loggedin/home"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()
            
            #Create a custom message to inform the user that the username and/or password entered were incorrect and to try enter another set of credentials on the "admin/login.html" web-page.
            adminLoginErrorMsg = "Incorrect credentials. Please try again!"
            
            #Render the "admin/login.html" web-page with the "adminLoginErrorMsg" to be displayed.
            return render_template('admin/login.html', _adminLoginErrorMsg = adminLoginErrorMsg)
    
    #Check if the "session['adminLoggedIn']" variable is set to "True" to allow access to the "/templates/admin/loggedin/home.html" web-page.
    if session['adminLoggedIn'] == True:
    
        #Check if the form "addsystemuser" was submitted and if so then collect and store the data of the new system user details.
        if request.args.get('f') == 'addsystemuser':
        
            #Store the datetime of when the new system user details are added
            systemDate = datetime.now()
            
            #Store the new system users name to the variable "systemUsersName" which was the data taken from the "admin/loggedin/addsystemuser" route to add a new system user credentials.
            systemUsersName = request.form['sName']

            #Store the new system users username to the variable "systemUsersUsername" which was the data taken from the "admin/loggedin/addsystemuser" route to add a new system user credentials.
            systemUsersUsername = request.form['sUsername']
            
            #Store the new system users name to the variable "systemUsersPassword" which was the data taken from the "admin/loggedin/addsystemuser" route to add a new system user credentials.
            systemUsersPassword = request.form['sPassword']
            
            #Create a new table if the systemUserLogin table is not already created in the "alsDB.db" database to store the new system users credentials for use on the system user part of the web-app routed at "/user/login" and also at "/user/".
            sqlQ = "CREATE TABLE IF NOT EXISTS systemUserLogin(sysUserID INT PRIMARY KEY, systemUserCreatedDate VARCHAR(255), name VARCHAR(255), username VARCHAR(255), password VARCHAR(255), createdByAdmin VARCHAR(255))"
            
            #Execute the sqlQ query to add the table to the "alsDB.db" database.
            cursor.execute(sqlQ)
            
            #Get the last entered "sysUserID" from the "systemUserLogin" table  to create the next usable "sysUserID" for the new system users credentials to be added to the "systemUserLogin" table.
            sqlQ = "SELECT sysUserID FROM systemUserLogin ORDER BY sysUserID DESC LIMIT 1"

            #Execute the sqlQ query to store the last sysUserID.
            cursor.execute(sqlQ)
            
            #Initialise the systemUserID variable to "0".
            systemUserID = 0
            
            #Loop using a for loop through the "sysUserID" that was found from the sqlQ query.
            for a in cursor.fetchall():
            
                #Store the found "sysUserID" to the "systemUserID" variable which is found at the first index of "a" within the cursor.
                systemUserID = int(a[0])
                    
            #Produce a check to compare if the "sysUserID" is the first "sysUserID".
            #If the "sysUserID" has a value of greateer or equal to 1, then the new "sysUserID" will be incremented by one and can be stored as the next usable "sysUserID".
            if systemUserID >= 1:
                systemUserID = systemUserID + 1
                
            #If the "sysUserID" is not greater than or equal to 1, then the new "sysUserID" will be initialised and stored at "1".
            else:
                systemUserID = 1
            
            #Allow the "adminUsername" variable to contain the username of the logged in admin from the session variable.
            adminUsername = session['adminUsername']

            #Input the data into the "systemUserLogin" table within the "alsDB.db" database for retrieval when the new system user will be able to login at "/user/login" route with the credentials added to the "systemUserLogin" table.
            cursor.execute("INSERT INTO systemUserLogin(sysUserID, systemUserCreatedDate, name, username, password, createdByAdmin) VALUES(?,?,?,?,?,?)",(systemUserID, systemDate, systemUsersName, systemUsersUsername, systemUsersPassword, adminUsername))
            
            #Commit the new system user login details to the database
            mydb.commit()
            
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''

            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "Administrator created a new system user with the credentials " + systemUsersUsername + " as the system users username and " + systemUsersPassword + " as the system users password."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "New system user login credentials added."
            
            #Provide which section of the web-app was accessed.
            logUser = session['adminUsername']
            
            #Provide the location where the log was entered.
            logLocation = "/admin/loggedin/home"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()

            #Create a message for the admin to be shown on the "admin/loggedin/home.html" web-page to confirm that the new system user login details have been added to the database and the new system user can login with the credentials provided.
            newSystemUserMsg = session['adminUsername'] + " has successfully added new system user details to the database. The system user can now log in to the system."
            
            #Render the "admin/loggedin/home.html" web-page with the "newSystemUserMsg" to be shown.
            return render_template('admin/loggedin/home.html', _newSystemUserMsg = newSystemUserMsg, _adminUsername = session['adminUsername'])
    
    #If the "session['adminLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/admin/login.html" web-page.
    elif session['adminLoggedIn'] != True:
        
        #Create a "notLoggedInAdminMsg" variable to send to the "/templates/admin/login.html" web-page if the administrative user is not logged in.
        notLoggedInAdminMsg = "You are not logged in. Log in to continue to Admin - ALS API."
        
        #Render the "/templates/admin/login.html" web-page when accessed with the system user is not logged in and the session variable "session['adminLoggedIn']" is not set.
        return render_template('admin/login.html', _notLoggedInAdminMsg = notLoggedInAdminMsg)

    #Check if the "session['adminLoggedIn']" variable is set to "True" to allow access to the "/templates/admin/loggedin/home.html" web-page.
    if session['adminLoggedIn'] == True:
    
        #Check if the "updatesystemuser" form was submitted on "/admin/loggedin/updateuser" route and if was then update the system users details on the "systemUserLogin" table in the "alsDB.db" database.
        if request.args.get('f') == 'updatesystemuser':
            
            #Allow the "adminUsername" variable to contain the username of the logged in admin from the session variable.
            adminUsername = session['adminUsername']

            #Get the "sysUserID" from the submitted form "updatesystemuser" and store in "sysUserID" variable to find that system user details with that "sysUserID".
            sysUserID = request.form['sysUserID']
            
            #"Get the sysUsersName from the form "updatesystemuser" submitted to update the "sysUsersName" in the "alsDB.db" database on the "systemUserLogin" table.
            sysUsersName = request.form['sysUsersName']
            
            #"Get the sysUsersUsername from the form "updatesystemuser" submitted to update the "sysUsersUsername" in the "alsDB.db" database on the "systemUserLogin" table.        
            sysUsersUsername = request.form['sysUsersUsername']
            
            #"Get the sysUsersPassword from the form "updatesystemuser" submitted to update the "sysUsersPassword" in the "alsDB.db" database on the "systemUserLogin" table.        
            sysUsersPassword = request.form['sysUsersPassword']
        
            #Execute the sqlQ query to update the "systemUserLogin" table in the "alsDB.db" database wiith the changes made by the admin user.
            cursor.execute("UPDATE systemUserLogin SET name = ?, username = ?, password = ?, createdByAdmin = ? WHERE sysUserID = ?", (sysUsersName, sysUsersUsername, sysUsersPassword, adminUsername, sysUserID))
            
            #Commit the changes to the "alsDB.db" database.
            mydb.commit()
            
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''

            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "Administrator updated the system user details wiith  " + sysUsersUsername + " as the system users username and " + sysUsersPassword + " as the system users password."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "Update of system user login credentials."
            
            #Provide which section of the web-app was accessed.
            logUser = session['adminUsername']
            
            #Provide the location where the log was entered.
            logLocation = "/admin/loggedin/home"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()

            #Create a message to inform the administrative user that the system user details had been updated succesfully. The message will be shown on the "admin/loggedin/home.html" web-page.
            updatedSystemUserMsg = session['adminUsername'] + " sucessfully updated the system user " + sysUsersUsername + "."
            
            #Render the "admin/loggedin/home.html" web-page to the administrative user sending the "updatedSystemUserMsg" to the web-page to inform succesfully updating the system users details.
            return render_template('admin/loggedin/home.html', _updatedSystemUserMsg = updatedSystemUserMsg, _adminUsername = session['adminUsername'])
            
        #If the user tries to access the "admin/loggedin/home.html" web-page without entering any credentials on the "admin/login.html" web-page then provide the "admin/login.html" web-page displayed to the user.
        else:
            return render_template('admin/loggedin/home.html', _adminUsername = session['adminUsername'])
        
    #If the "session['adminLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/admin/login.html" web-page.
    elif session['adminLoggedIn'] != True:
        
        #Create a "notLoggedInAdminMsg" variable to send to the "/templates/admin/login.html" web-page if the administrative user is not logged in.
        notLoggedInAdminMsg = "You are not logged in. Log in to continue to Admin - ALS API."
        
        #Render the "/templates/admin/login.html" web-page when accessed with the system admin user is not logged in and the session variable "session['adminLoggedIn']" is not set.
        return render_template('admin/login.html', _notLoggedInAdminMsg = notLoggedInAdminMsg)

'''
Purpose: The addsystemuser() function renders the "admin/loggedin/addsystemuser.html" web-page to be displayed to the administrative user to allow the insertion of new system users details to be able to login to the user ppart of the system at "/user/login" route.
'''
@app.route('/admin/loggedin/addsystemuser', methods=['GET', 'POST'])
def addsystemuser():

    #Check if the "session['adminLoggedIn']" variable is set to "True" to allow access to the "/templates/admin/loggedin/addsystemuser.html" web-page.
    if session['adminLoggedIn'] == True:

        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''

        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "Administrative user accessed /admin/loggedin/addsystemuser."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "Access of /admin/loggedin/updatesystemuser."
        
        #Provide which section of the web-app was accessed.
        logUser = session['adminUsername']
        
        #Provide the location where the log was entered.
        logLocation = "/admin/loggedin/addsystemuser"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()

        return render_template('admin/loggedin/addsystemuser.html',_adminUsername = session['adminUsername'])
    
    #If the "session['adminLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/admin/login.html" web-page.
    elif session['adminLoggedIn'] != True:
        
        #Create a "notLoggedInAdminMsg" variable to send to the "/templates/admin/login.html" web-page if the administrative user is not logged in.
        notLoggedInAdminMsg = "You are not logged in. Log in to continue to Admin - ALS API."
        
        #Render the "/templates/admin/login.html" web-page when accessed with the system admin user is not logged in and the session variable "session['adminLoggedIn']" is not set.
        return render_template('admin/login.html', _notLoggedInAdminMsg = notLoggedInAdminMsg)

'''
Purpose: The viewsystemuser() function renders the "admin/loggedin/viewsystemuser.html" web-page to be displayed to the administrative user to provide details of all the system users.
'''
@app.route('/admin/loggedin/viewsystemusers', methods=['GET', 'POST'])
def viewsystemuser():

    #Check if the "session['adminLoggedIn']" variable is set to "True" to allow access to the "/templates/admin/loggedin/viewsystemusers.html" web-page.
    if session['adminLoggedIn'] == True:

        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''

        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "Administrative user accessed /admin/loggedin/viewsystemusers."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/admin/loggedin/viewsystemusers route accessed.."
        
        #Provide which section of the web-app was accessed.
        logUser = session['adminUsername']
        
        #Provide the location where the log was entered.
        logLocation = "/admin/loggedin/viewsystemusers"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()

        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        #Create a new table if the systemUserLogin table is not already created in the "alsDB.db" database to store the new system users credentials for use on the system user part of the web-app routed at "/user/login" and also at "/user/".
        sqlQ = "CREATE TABLE IF NOT EXISTS systemUserLogin(sysUserID INT PRIMARY KEY, systemUserCreatedDate VARCHAR(255), name VARCHAR(255), username VARCHAR(255), password VARCHAR(255), createdByAdmin VARCHAR(255))"
        
        #Execute the sqlQ query to add the table to the "alsDB.db" database.
        cursor.execute(sqlQ)
        
        #Get all the system user login credentials to be viewed on the "admin/loggedin/viewsystemusers.html" web-page by the administrative user.
        sqlQ = "SELECT * FROM systemUserLogin"
        
        #Execute and get the data into the cursor object from the "systemUserLogin" table in the "alsDB.db" database.
        cursor.execute(sqlQ)
        
        #Store the found user login details from the "systemUserLogin" table "alsDB.db" to be sent to the "admin/loggedin/viewsystemusers.html" web-page.
        systemUserDetails = cursor.fetchall()
        
        #Render the "admin/loggedin/viewsystemusers.html" web-page for the administrative user to view the system user details.
        return render_template('admin/loggedin/viewsystemusers.html',_adminUsername = session['adminUsername'], _systemUserDetails = systemUserDetails)
    
    #If the "session['adminLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/admin/login.html" web-page.
    elif session['adminLoggedIn'] != True:
        
        #Create a "notLoggedInAdminMsg" variable to send to the "/templates/admin/login.html" web-page if the administrative user is not logged in.
        notLoggedInAdminMsg = "You are not logged in. Log in to continue to Admin - ALS API."
        
        #Render the "/templates/admin/login.html" web-page when accessed with the system admin user is not logged in and the session variable "session['adminLoggedIn']" is not set.
        return render_template('admin/login.html', _notLoggedInAdminMsg = notLoggedInAdminMsg)
'''
Purpose: The updatesystemuser() function renders the "admin/loggedin/updatesystemuser.html" web-page to be displayed to the administrative user to allow updates of current system users details.
'''
@app.route('/admin/loggedin/updatesystemuser', methods=['GET', 'POST'])
def updatesystemuser():

    #Check if the "session['adminLoggedIn']" variable is set to "True" to allow access to the "/templates/admin/loggedin/updatesystemuser.html" web-page.
    if session['adminLoggedIn'] == True:

        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''

        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "Administrative user accessed /admin/loggedin/updatesystemuser.."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/admin/loggedin/updatesystemuser route accessed."
        
        #Provide which section of the web-app was accessed.
        logUser = session['adminUsername']
        
        #Provide the location where the log was entered.
        logLocation = "/admin/loggedin/updatesystemuser"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()

        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()

        #Obtain all data of system user details from the "systemUserLogin" table in the "alsDB.db" database.
        sqlQ = "SELECT * FROM systemUserLogin"

        #Execute the sqlQ query to retrieve the data.
        cursor.execute(sqlQ)
        
        #Store the found details from the sqlQ query to the "userDetails" variable to be obtainable on the "admin/loggedin/updatesystemuser.html" web-page.
        userDetails = cursor.fetchall()
        
        #Render the "admin/loggedin/updatesystemuser.html" web-page to the administrative user and transfer the "userDetails" to the "admin/loggedin/updatesystemuser.html" web-page.
        return render_template('admin/loggedin/updatesystemuser.html',_adminUsername = session['adminUsername'], _userDetails = userDetails)
    
    #If the "session['adminLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/admin/login.html" web-page.
    elif session['adminLoggedIn'] != True:
        
        #Create a "notLoggedInAdminMsg" variable to send to the "/templates/admin/login.html" web-page if the administrative user is not logged in.
        notLoggedInAdminMsg = "You are not logged in. Log in to continue to Admin - ALS API."
        
        #Render the "/templates/admin/login.html" web-page when accessed with the system admin user is not logged in and the session variable "session['adminLoggedIn']" is not set.
        return render_template('admin/login.html', _notLoggedInAdminMsg = notLoggedInAdminMsg)
'''
Purpose: The updatesystemuser() function renders the "admin/loggedin/updateuser.html" web-page to be displayed to the administrative user to allow updates of current system users details.
'''
@app.route('/admin/loggedin/updateuser', methods=['GET', 'POST'])
def updatesysuser():

    #Check if the "session['adminLoggedIn']" variable is set to "True" to allow access to the "/templates/admin/loggedin/updateuser.html" web-page.
    if session['adminLoggedIn'] == True:

        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()

        #Retrieve the system user ID from the "admin/loggedin/updatesystemuser.html" web-page to find that system users details so the details can be updated on the "admin/loggedin/updateuser.html" web-page.
        sysUserID = request.form['sysUserID']
        
        #Obtain all data of system user details from the "systemUserLogin" table in the "alsDB.db" database where the sysUserID matches the details of the user that is to be updated.
        sqlQ = "SELECT * FROM systemUserLogin WHERE sysUserID = ?"

        #Execute the sqlQ query to retrieve the data.
        cursor.execute(sqlQ, (sysUserID,))
        
        #Store the found details from the sqlQ query to the "userDetails" variable to be obtainable on the "admin/loggedin/updatesystemuser.html" web-page.
        userDetails = cursor.fetchall()
            
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''

        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "Administrative user selected system user with." + sysUserID + " ID for update of system user details."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/admin/loggedin/updateuser route accessed ."
        
        #Provide which section of the web-app was accessed.
        logUser = session['adminUsername']
        
        #Provide the location where the log was entered.
        logLocation = "/admin/loggedin/home"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()

        #Render the "admin/loggedin/updatesystemuser.html" web-page to the administrative user and transfer the "userDetails" to the "admin/loggedin/updatesystemuser.html" web-page.
        return render_template('admin/loggedin/updateuser.html', _adminUsername = session['adminUsername'], _userDetails = userDetails)
    
    #If the "session['adminLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/admin/login.html" web-page.
    elif session['adminLoggedIn'] != True:
        
        #Create a "notLoggedInAdminMsg" variable to send to the "/templates/admin/login.html" web-page if the administrative user is not logged in.
        notLoggedInAdminMsg = "You are not logged in. Log in to continue to Admin - ALS API."
        
        #Render the "/templates/admin/login.html" web-page when accessed with the system admin user is not logged in and the session variable "session['adminLoggedIn']" is not set.
        return render_template('admin/login.html', _notLoggedInAdminMsg = notLoggedInAdminMsg)
        
'''
Purpose: The deletesystemuser() function renders the "admin/loggedin/deletesystemuser.html" web-page to be displayed to the administrative user to allow the deletion of system user details.
'''
@app.route('/admin/loggedin/deletesystemuser', methods=['GET', 'POST'])
def deletesystemuser():

    #Check if the "session['adminLoggedIn']" variable is set to "True" to allow access to the "/templates/admin/loggedin/deletesystemuser.html" web-page.
    if session['adminLoggedIn'] == True:

        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
       
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''

        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "Administrative user accessed /admin/loggedin/deletesystemuser."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/admin/loggedin/deletesystemuser route accessed ."
        
        #Provide which section of the web-app was accessed.
        logUser = session['adminUsername']
        
        #Provide the location where the log was entered.
        logLocation = "/admin/loggedin/deletesystemuser"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()
        
        #Get all system user details from the "systemUserLogin" table in the "alsDb.db" to be sent to the "admin/loggedin/deletesystemuser.html" web-page.
        sqlQ = "SELECT * FROM systemUserLogin"

        #Execute the "sqlQ" query to retrieve the data.
        cursor.execute(sqlQ)

        #Store the "sqlQ" query into the "userDetails" variable to be sent to the "admin/loggedin/deletesystemuser.html" web-page.
        userDetails = cursor.fetchall()

        #Checik if the "deletesystemuser" form has been submitted by the "DELETE" button on the form so the deletion query on the "systemUserLogin" table in the "alsDB.db" database. 
        if request.args.get('f') == 'deletesystemuser':
        
            #Get the "sysUserID" from the "deletesystemuser" form on the "admin/loggedin/deletesystemuser.html" web-page when the "DELETE" button has been submitted.
            sysUserID = request.form['sysUserID']
            
            #Provide a query to delete the system user details that matches the "sysUserID" on the "systemUserLogin" table in the "alsDB.db" database.
            sqlQ = "DELETE FROM systemUserLogin WHERE sysUserID = ?"
            
            #Execute the "sqlQ" delete query.
            cursor.execute(sqlQ, (sysUserID,))
            
            #Commit the deletion changes to the "alsDB.db" database.
            mydb.commit()
            
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''

            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "Administrative user deleted system user with." + sysUserID + " ID."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "Deleted system user. ."
            
            #Provide which section of the web-app was accessed.
            logUser = session['adminUsername']
        
            #Provide the location where the log was entered.
            logLocation = "/admin/loggedin/deletesystemuser"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()
            
            #Get all system user details from the "systemUserLogin" table in the "alsDb.db" to be sent to the "admin/loggedin/deletesystemuser.html" web-page.
            sqlQ = "SELECT * FROM systemUserLogin"

            #Execute the "sqlQ" query to retrieve the data.
            cursor.execute(sqlQ)

            #Store the "sqlQ" query into the "userDetails" variable to be sent to the "admin/loggedin/deletesystemuser.html" web-page.
            userDetails = cursor.fetchall()
            
            #Store the session variable of the adminUsername to the variable "adminUsername"
            adminUsername = session['adminUsername']
            
            #Create a message to inform the administrative user that the system user details have been deleted.
            deletedSystemUserMsg = adminUsername + " successfully deleted the user with ID " + sysUserID + "."
            
            #Render the "admin/loggedin/deletesystemuser.html" web-page sending the system user details to the web-page.
            return render_template('admin/loggedin/deletesystemuser.html',_deletedSystemUserMsg = deletedSystemUserMsg, _adminUsername = adminUsername, _userDetails = userDetails)

    #If the "session['adminLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/admin/login.html" web-page.
    elif session['adminLoggedIn'] != True:
        
        #Create a "notLoggedInAdminMsg" variable to send to the "/templates/admin/login.html" web-page if the administrative user is not logged in.
        notLoggedInAdminMsg = "You are not logged in. Log in to continue to Admin - ALS API."
        
        #Render the "/templates/admin/login.html" web-page when accessed with the system admin user is not logged in and the session variable "session['adminLoggedIn']" is not set.
        return render_template('admin/login.html', _notLoggedInAdminMsg = notLoggedInAdminMsg)
    
    #Render the "admin/loggedin/deletesystemuser.html" web-page sending the system user details to the web-page.
    return render_template('admin/loggedin/deletesystemuser.html',  _adminUsername = session['adminUsername'], _userDetails = userDetails)

'''
The "viewlogs()" function provides the rendering of the "admin/loggedin/viewlogs.html" web-page and will provide the details of the logs to be displayed to the administrative user when they access the "/admin/loggedin/viewlogs" route of the web-app system.
'''
@app.route('/admin/loggedin/viewlogs', methods=['GET', 'POST'])
def viewlogs():

    #Check if the "session['adminLoggedIn']" variable is set to "True" to allow access to the "/templates/admin/loggedin/viewlogs.html" web-page.
    if session['adminLoggedIn'] == True:

        #Store the administrators username in the variable "adminUsername"with the sessions username for that administrative user.
        adminUsername = session['adminUsername']
        
        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()

        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''

        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "Administrative user accessed /admin/loggedin/viewlogs."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/admin/loggedin/viewlogs route accessed ."
        
        #Provide which section of the web-app was accessed.
        logUser = session['adminUsername']
        
        #Provide the location where the log was entered.
        logLocation = "/admin/loggedin/viewlogs"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()

        #Retrieve all the data from the "messageLogs" table in the "alsDB.db" database for displaying all the logs on the "admin/loggedin/viewlogs.html" web-page.
        sqlQ = "SELECT * FROM messageLogs ORDER BY logDate DESC"
        
        #Execute the "sqlQ" select statement.
        cursor.execute(sqlQ)
        
        #Store all the logs from the "sqlQ" select statement in the "logDetails" variable to send to the "admin/loggedin/viewlogs.html" web-page.
        logDetails = cursor.fetchall()
        
        #Render the "admin/loggedin/viewlogs.html" web-page to display all the logs information to the administrative user. 
        return render_template('admin/loggedin/viewlogs.html', _logDetails = logDetails, _adminUsername = adminUsername)

    #If the "session['adminLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/admin/login.html" web-page.
    elif session['adminLoggedIn'] != True:
        
        #Create a "notLoggedInAdminMsg" variable to send to the "/templates/admin/login.html" web-page if the administrative user is not logged in.
        notLoggedInAdminMsg = "You are not logged in. Log in to continue to Admin - ALS API."
        
        #Render the "/templates/admin/login.html" web-page when accessed with the system admin user is not logged in and the session variable "session['adminLoggedIn']" is not set.
        return render_template('admin/login.html', _notLoggedInAdminMsg = notLoggedInAdminMsg)
        
'''
"usersignup()" function returns the default URL for the /templates/user/usersignup.html file to provide the signup form to be displayed so the user of the system can provide details to be allowed access to the user part of the system. I provided this certain provision of the web system as a starting point on the basis that essential information/data can be provided and stored to indicate and differentiate the users who will use the web-app system. 
'''
@app.route('/user/', methods=['GET', 'POST']) 
@app.route('/user/login', methods=['GET', 'POST'])
def userlogin():

    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
    cursor = mydb.cursor()

    '''
    Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
    '''

    #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
    sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
    
    #Execute the "sqlQ" query.
    cursor.execute(sqlQ)

    #Access the current datetime. 
    logDate = datetime.now()
    
    #Provide a log message upon accessing the route with information of the specific action taken on the route.
    logMessage = "Accessed /user/login route."
    
    #Provide a category for the ability to search based on action of the log.
    logCategory = "/user/login route accessed."
    
    #Provide which section of the web-app was accessed.
    logUser = "User not logged in"
    
    #Provide the location where the log was entered.
    logLocation = "/user/login"
    
    #Insert the log data into the "messageLogs" database.
    cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
    
    #Commit the log to the "alsDB.db" database.
    mydb.commit()

    #Render the "/user/login.html" web-page when the "/user/login" route is accessed.
    return render_template('user/login.html')
    
'''
"renderhome()" function allows the system user to access the "/templates/user/loggedin/home.html" web-page when the user has logged in on the "/templates/customer/login.html" web-page. The "/templates/user/loggedin/home.html" route is also accessed when the system user adds a customer account on the "/templates/user/loggedin/addcustomer.html" web-page, and when the system user has updated customer account details on the "/templates/user/loggedin/updatecustomers.html" web-page.
'''
@app.route('/user/loggedin/home', methods=['GET', 'POST'])
def renderhome():

    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
    cursor = mydb.cursor()

    #Check if the "addCustomer" form from the "templates/user/loggedin/addcustomer.html" has been submitted, then collect and store the values from the "addCustomer" form in the "customerDetails" table of the "alsDb.db" database.
    if request.args.get('f') == 'addCustomer':
        
        #Check if the user is logged in with the session['luserLoggedIn'] variable set when the correct credentials were entered on the "/templates/user/login.html" web-page to access the "/user/loggedin/home" route.
        if session['userLoggedIn'] == True:

            #Store the date and time in the "addCustomerDate" variable of when the customer's data will be added to the "customerDetails" table in the "alsDB.db" 
            addCustomerDate = datetime.now()
            
            #Convert and store the "addCustomerDate" variable as a string valued variable named "addCustomerDate".
            addCustDate = str(addCustomerDate)
            
            #Collect and store the customer's first name in the "addCustomerFirstName" variable collected from the "addCustomer" form on the "/templates/user/loggedin/addcustomer.html" web-page from the input named "customerFirstName".
            addCustomerFirstName = request.form['customerFirstName']
            
            #Collect and store the customer's last name in the "addCustomerLastName" variable collected from the "addCustomer" form on the "/templates/user/loggedin/addcustomer.html" web-page from the input named "customerLastName".
            addCustomerLastName = request.form['customerLastName']

            #Collect and store the customer's date of birth in the "addCustomerDateOfBirth" variable collected from the "addCustomer" form on the "/templates/user/loggedin/addcustomer.html" web-page from the input named "customerDateOfBirth".
            addCustomerDateOfBirth = request.form['customerDateOfBirth']
            
            #Collect and store the customer's residential address details in the "addCustomerResidentialAddress" variable collected from the "addCustomer" form on the "/templates/user/loggedin/addcustomer.html" web-page from the input named "addCustomerResidentialAddress".
            addCustomerResidentialAddress = request.form['customerResidentialAddress']
            
            #Collect and store the customer's date of residential move in in the "addCustomerDateOfMoveIn" variable collected from the "addCustomer" form on the "/templates/user/loggedin/addcustomer.html" web-page from the input named "customerDateOfMoveIn".
            addCustomerDateOfMoveIn = request.form['customerResidentialMoveInDate']
            
            #Collect and store the customer's email address in the "addCustomerEmailAddress" variable collected from the "addCustomer" form on the "/templates/user/loggedin/addcustomer.html" web-page from the input named "customerEmailAddress".
            addCustomerEmailAddress = request.form['customerEmailAddress']
            
            #Collect and store the customer's phone number in the "addCustomerPhoneNumber" variable collected from the "addCustomer" form on the "/templates/user/loggedin/addcustomer.html" web-page from the input named "customerPhoneNumber".
            addCustomerPhoneNumber = request.form['customerPhoneNumber']
            
            #Collect and store the customer's employment status in the "addCustomerEmploymentStatus" variable collected from the "addCustomer" form on the "/templates/user/loggedin/addcustomer.html" web-page from the input named "customerEmploymentStatus".
            addCustomerEmploymentStatus = request.form['customerEmploymentStatus']
            
            #Collect and store the customer's username in the "addCustomerUsername" variable collected from the "addCustomer" form on the "/templates/user/loggedin/addcustomer.html" web-page from the input named "customerUsername".
            addCustomerUsername = request.form['customerUsername']
            
            #Collect and store the customer's password in the "addCustomerPassword" variable collected from the "addCustomer" form on the "/templates/user/loggedin/addcustomer.html" web-page from the input named "customerPassword".
            addCustomerPassword = request.form['customerPassword']
            
            #Check if the employment status of the customer from the "customerEmploymentStatus" select box on the "addCustomer" form on the "/templates/user/loggedin/addcustomer,html" web-page is "Employed", collect the details of the form within the variables below and initialise any other employment status' as empty strings.
            if addCustomerEmploymentStatus == 'Employed':
                
                #Collect the "customerDateEmploymentCommenced" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerDateEmploymentCommenced" variable.
                addCustomerDateEmploymentCommenced = request.form['customerDateEmploymentCommenced']

                #Collect the "customerEmployerName" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerEmployerName" variable.
                addCustomerEmployerName = request.form['customerEmployerName']

                #Collect the "customerEmployerAddress" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerEmployerAddress" variable.
                addCustomerEmployerAddress = request.form['customerEmployerAddress']

                #Collect the "customerEmployerContactNumber" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerEmployerContactNumber" variable.
                addCustomerEmployerContactNumber = request.form['customerEmployerContactNumber']
                
                #Initialise the "addCustomerLengthOfTimeAsSelfEmployment" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerLengthOfTimeAsSelfEmployed = ""

                #Initialise the "addCustomerCustomerName" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerCompanyName = ""

                #Initialise the "addCustomerCompanyAddress" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerCompanyAddress = ""
                
                #Initialise the "addCustomerGovernmentBenefitsDescription" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerGovernmentBenefitsDescription = ""
                
            #Check if the employment status of the customer from the "customerEmploymentStatus" select box on the "addCustomer" form on the "/templates/user/loggedin/addcustomer,html" web-page is "Self Employed", collect the details of the form within the variables below and initialise any other employment status' as empty strings.
            elif addCustomerEmploymentStatus == 'Self Employed':
            
                #Collect the "customerLengthOfTimeAsSelfEmployment" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerEmployerContactNumber" variable.
                addCustomerLengthOfTimeAsSelfEmployed= request.form['customerLengthOfTimeAsSelfEmployed']
                
                #Collect the "customerCompanyName" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerCompanyName" variable.
                addCustomerCompanyName = request.form['customerCompanyName']
                
                #Collect the "customerCompanyName" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerCompanyName" variable.
                addCustomerCompanyAddress = request.form['customerCompanyAddress']
                
                #Initialise the "addCustomerDateEmploymentCommenced" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerDateEmploymentCommenced = ""
                
                #Initialise the "addCustomerEmployerName" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerEmployerName = ""                       
                
                #Initialise the "addCustomerEmployerAddress" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerEmployerAddress = ""
                
                #Initialise the "addCustomerEmployerContactNumber" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerEmployerContactNumber = ""
                
                #Initialise the "addCustomerGovernmentBenefitsDescription" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerGovernmentBenefitsDescription = ""
                
            #Check if the employment status of the customer from the "customerEmploymentStatus" select box on the "addCustomer" form on the "/templates/user/loggedin/addcustomer,html" web-page is "Government Benefits", collect the details of the form within the variables below and initialise any other employment status' as empty strings.
            elif empStatus == 'Government Benefits':
            
                #Collect the "customerGovernmentBenefitsDescription" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerGovernmentBenefitsDescription" variable.
                addCustomerGovernmentBenefitsDescription = request.form['customerGovernmentBenefitsDescription']

                #Initialise the "addCustomerLengthOfTimeAsSelfEmployment" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerLengthOfTimeAsSelfEmployed = ""
                
                #Initialise the "addCustomerCompanyName" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerCompanyName = ""
                
                #Initialise the "addCustomerCompanyDetails" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerCompanyAddress = ""
                
                #Initialise the "addCustomerDateEmploymentCommenced" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerDateEmploymentCommenced = ""
                
                #Initialise the "addCustomerEmployerName" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.
                addCustomerEmployerName = ""       

                #Initialise the "addCustomerEmployerAddress" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.            
                addCustomerEmployerAddress = ""
                
                #Initialise the "addCustomerEmployerContactNumber" variable as an empty string to store within the "customerDetails" table in the "alsDB.db" database.            
                addCustomerEmployerContactNumber = ""

            #Collect the "customerGrossMonthlyIncome" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerGrossMonthlyIncome" variable.
            addCustomerGrossMonthlyIncome = request.form['customerGrossMonthlyIncome']
            
            #Collect the "customerYearlyIncomeAfterTax" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerYearlyIncomeAfterTax" variable.
            addCustomerYearlyIncomeAfterTax = request.form['customerYearlyIncomeAfterTax']
            
            #Collect the "customerMotorCostsDescription" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerMotorCostsDescription" variable.        
            addCustomerMotorCostsDescription = request.form['customerMotorCostsDescription']

            #Collect the "customerFoodExpensesDescription" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerFoodExpensesDescription" variable.
            addCustomerFoodExpensesDescription = request.form['customerFoodExpensesDescription']
            
            #Collect the "customerClothingCostsDescription" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerClothingCostsDescription" variable.
            addCustomerClothingCostsDescription = request.form['customerClothingExpensesDescription']
            
            #Collect the "customerChildcareCostsDescription" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerChildcareCostsDescription" variable.
            addCustomerChildcareCostsDescription = request.form['customerChildcareCostsDescription']
            
            #Collect the "customerHousingExpensesDescription" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerHousingExpensesDescription" variable.
            addCustomerHousingExpensesDescription = request.form['customerHousingExpensesDescription']
            
            #Collect the "customerHomeRentalCostsDescription" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerHomeRentalCostsDescription" variable.
            addCustomerHomeRentalCostsDescription = request.form['customerHomeRentalCostsDescription']
            
            #Collect the "customerMortgageRepaymentsDescription" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerMortgageRepaymentsDescription" variable.
            addCustomerMortgageRepaymentsDescription = request.form['customerMortgageRepaymentsDescription']
            
            #Collect the "customerUtilityCostsDescription" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerUtilityCostsDescription" variable.
            addCustomerUtilityCostsDescription = request.form['customerUtilityCostsDescription']

            #Collect the "customerPhoneExpensesDescription" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerPhoneExpensesDescription" variable.
            addCustomerPhoneExpensesDescription = request.form['customerPhoneExpensesDescription']
            
            #Collect the "customerOtherExpensesDescription" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerOtherExpensesDescription" variable.
            addCustomerOtherExpensesDescription = request.form['customerOtherExpensesDescription']
            
            #Collect the "customerMotorCostsAmount" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerMotorCostsAmount" variable.
            addCustomerMotorCostsAmount = request.form['customerMotorCostsAmount']
            
            #Collect the "customerFoodExpensesAmount" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerFoodExpensesAmount" variable.
            addCustomerFoodExpensesAmount = request.form['customerFoodExpensesAmount']
            
            #Collect the "customerClothingCostsAmount" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerClothingCostsAmount" variable.
            addCustomerClothingCostsAmount = request.form['customerClothingExpensesAmount']
            
            #Collect the "customerChildcareCostsAmount" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerChildcareCostsAmount" variable.
            addCustomerChildcareCostsAmount = request.form['customerChildcareCostsAmount']
            
            #Collect the "customerHousingExpensesAmount" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerHousingExpensesAmount" variable.
            addCustomerHousingExpensesAmount = request.form['customerHousingExpensesAmount']
            
            #Collect the "customerHomeRentalCostsAmount" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerHomeRentalCostsAmount" variable.
            addCustomerHomeRentalCostsAmount = request.form['customerHomeRentalCostsAmount']
            
            #Collect the "customerMortgageRepaymentsAmount" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerMortgageRepaymentsAmount" variable.
            addCustomerMortgageRepaymentsAmount = request.form['customerMortgageRepaymentsAmount']
            
            #Collect the "customerUtilityCostsAmount" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerUtilityCostsAmount" variable.
            addCustomerUtilityCostsAmount = request.form['customerUtilityCostsAmount']
            
            #Collect the "customerPhoneExpensesAmount" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerPhoneExpensesAmount" variable.
            addCustomerPhoneExpensesAmount = request.form['customerPhoneExpensesAmount']
            
            #Collect the "customerOtherExpensesAmount" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerPhoneExpensesAmount" variable.
            addCustomerOtherExpensesAmount = request.form['customerOtherExpensesAmount']
            
            #Collect the "customerTotalExpensesAmount" input from the "/templates/user/loggedin/addcustomer.html" web-page and store in the "addCustomerTotalExpensesAmount" variable.
            addCustomerTotalExpensesAmount = request.form['customerTotalExpensesAmount']

            #Create a table if non-existent for the inputted customer details to be added to this table "customerAccounts" within the "alsDB.db" database to include the data submitted from the "addCustomer" form on the "/templates/user/loggedin/addcustomer.html" web-page.
            sqlQ = "CREATE TABLE IF NOT EXISTS customerAccounts(customerAccountID INT PRIMARY KEY, customerAccountCreatedDate VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), customerDateOfBirth VARCHAR(255), customerResidentialStatus VARCHAR(255), customerDateOfMoveIn VARCHAR(255), customerPhoneNumber VARCHAR(255), customerEmailAddress VARCHAR(255), customerEmploymentStatus VARCHAR(255), customerDateEmploymentCommenced VARCHAR(255), customerEmployerName VARCHAR(255), customerEmployerAddress VARCHAR(255), customerEmployerContactNumber VARCHAR(255), customerLengthOfTimeAsSelfEmployed VARCHAR(255), customerCompanyName VARCHAR(255), customerCompanyAddress VARCHAR(255), customerGovernmentBenefitsDescription VARCHAR(255), customerGrossMonthlyIncome VARCHAR(255), customerYearlyIncomeAfterTax VARCHAR(255), customerMotorCostsDescription VARCHAR(255), customerMotorCostsAmount VARCHAR(255), customerFoodExpensesDescription VARCHAR(255), customerFoodExpensesAmount VARCHAR(255), customerClothingExpensesDescription VARCHAR(255), customerClothingExpensesAmount VARCHAR(255), customerChildcareCostsDescription VARCHAR(255), customerChildcareCostsAmount VARCHAR(255), customerHousingCostsDescription VARCHAR(255), customerHousingCostsAmount VARCHAR(255), customerHomeRentalCostsDescription VARCHAR(255), customerHomeRentalCostsAmount VARCHAR(255), customerMortgageRepaymentsDescription VARCHAR(255), customerMortgageRepaymentsAmount VARCHAR(255), customerUtilityCostsDescription VARCHAR(255), customerUtilityCostsAmount VARCHAR(255), customerPhoneExpensesDescription VARCHAR(255), customerPhoneExpensesAmount VARCHAR(255), customerOtherExpensesDescription VARCHAR(255), customerOtherExpensesAmount VARCHAR(255), customerTotalExpensesAmount VARCHAR(255), customerAccountUsername VARCHAR(255), customerAccountPassword VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
            
            #Get the last entered "customerAccountID" from the "customerAccounts" table in the "alsDB.db" database to create the next customer account ID to be inserted to the "customerAccounts" table in the "alsDB.db" database. 
            sqlQ = ("SELECT customerAccountID FROM customerAccounts ORDER BY customerAccountID DESC LIMIT 1")
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
            
            #Initialise the "addCustomerAccountID" variable to "0" to store the last entered "customerAccountID" when looped through.
            lastCustomerAccountID = 0
            
            #Loop through the results of the "sqlQ" query to find and store the last entered "customerAccountID" from the "customerAccounts" table in the "alsDB.db" database in the "addCustomerAccountID" variable.
            for custAccountID in cursor.fetchall():
            
                #Store the last entered "customerAccountID" from the "customerAccounts" table in the "alsDB.db" databse to the "addCustomerAccountID" variable.
                lastCustomerAccountID = int(custAccountID[0])

            #If a "customerAccountID" was found in the "customerAccounts" table in the "alsDB.db" database then create and store the next "customerAccountID" by incrementing by one the found last entered "customerAccountID" from the "lastCustomerAccountID" in the "addCustomerAccountID" variable.
            if lastCustomerAccountID > 0: 
                
                #Store and increment by one the "lastCustomerAccountID" in the "addCustomerAccountID" variable to insert in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerAccountID = lastCustomerAccountID + 1
                
            #If there was no "customerAccountID" found in the loop of the "sqlQ" query results then create the first ID to be stored in the "customerAccounts" table in the "alsDB.db" database with the value of "0".
            else:
            
                #Create the first "customerAccountID" to be stored in the "customerAccounts" table in the "alsDB.db" as the "addCustomerAccountID" variable.
                addCustomerAccountID = "10001"
            
            #Insert into the "customerAccounts" 
            cursor.execute("INSERT INTO customerAccounts(customerAccountID, customerAccountCreatedDate, customerFirstName, customerLastName,customerDateOfBirth, customerResidentialStatus, customerDateOfMoveIn, customerPhoneNumber, customerEmailAddress, customerEmploymentStatus, customerDateEmploymentCommenced, customerEmployerName, customerEmployerAddress, customerEmployerContactNumber, customerLengthOfTimeAsSelfEmployed, customerCompanyName, customerCompanyAddress, customerGovernmentBenefitsDescription, customerGrossMonthlyIncome, customerYearlyIncomeAfterTax, customerMotorCostsDescription, customerMotorCostsAmount, customerFoodExpensesDescription, customerFoodExpensesAmount, customerClothingExpensesDescription, customerClothingExpensesAmount, customerChildcareCostsDescription, customerChildcareCostsAmount, customerHousingCostsDescription, customerHousingCostsAmount, customerHomeRentalCostsDescription, customerHomeRentalCostsAmount, customerMortgageRepaymentsDescription, customerMortgageRepaymentsAmount, customerUtilityCostsDescription, customerUtilityCostsAmount, customerPhoneExpensesDescription, customerPhoneExpensesAmount, customerOtherExpensesDescription, customerOtherExpensesAmount, customerTotalExpensesAmount, customerAccountUsername, customerAccountPassword) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(addCustomerAccountID, addCustomerDate, addCustomerFirstName, addCustomerLastName, addCustomerDateOfBirth, addCustomerResidentialAddress, addCustomerDateOfMoveIn, addCustomerPhoneNumber, addCustomerEmailAddress, addCustomerEmploymentStatus, addCustomerDateEmploymentCommenced, addCustomerEmployerName, addCustomerEmployerAddress, addCustomerEmployerContactNumber, addCustomerLengthOfTimeAsSelfEmployed, addCustomerCompanyName, addCustomerCompanyAddress, addCustomerGovernmentBenefitsDescription, addCustomerGrossMonthlyIncome, addCustomerYearlyIncomeAfterTax, addCustomerMotorCostsDescription, addCustomerMotorCostsAmount, addCustomerFoodExpensesDescription, addCustomerFoodExpensesAmount, addCustomerClothingCostsDescription, addCustomerClothingCostsAmount, addCustomerChildcareCostsDescription, addCustomerChildcareCostsAmount, addCustomerHousingExpensesDescription, addCustomerHousingExpensesAmount, addCustomerHomeRentalCostsDescription, addCustomerHomeRentalCostsAmount, addCustomerMortgageRepaymentsDescription, addCustomerMortgageRepaymentsAmount, addCustomerUtilityCostsDescription, addCustomerUtilityCostsAmount, addCustomerPhoneExpensesDescription, addCustomerPhoneExpensesAmount, addCustomerOtherExpensesDescription, addCustomerOtherExpensesAmount, addCustomerTotalExpensesAmount, addCustomerUsername, addCustomerPassword))
            
            #Commit the entry to the "customerAccounts" table in the "alsDB.db" database.
            mydb.commit()

            #Create a table "customerAccountLogin" if non-existent to add the customer login credentials for the ability to enter credentials on the "/customer/login" route of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS customerAccountLogin(customerLoginID INT PRIMARY KEY, customerUsername VARCHAR(255), customerPassword VARCHAR(255), customerID VARCHAR(255))"
            
            #Execute the "sqlQ query.
            cursor.execute(sqlQ)

            #Initialise the variable "customerLoginID" to "0".
            customerLoginID = 0
            
            #Select the last entered "customerLoginID" from the "customerAccountLogin" table in the "alsDB.db" database so the next "customerLoginID" to enter in the "customerAccountLogin" table can be created.
            sqlQ = "SELECT customerLoginID FROM customerAccountLogin ORDER BY customerLoginID DESC LIMIT 1"
            
            #Execute the "sqlQ query.
            cursor.execute(sqlQ)

            #Loop through the "sqlQ" query results to get the last entered "customerLoginID".
            for customerID in cursor.fetchall():
                
                #Store the found last entered "customerLoginID" as a numerical value in the "customerLoginID" variable. 
                customerLoginID = int(customerID[0])
                        
            #If there was a result of a "customerLoginID" then increment the found "customerLoginID" by one and store in the "addCustomerLoginID".
            if customerLoginID >= 1:
                
                #Increment the found "customerLoginID" by one and store in the "addCustomerLoginID"  variable.
                addCustomerLoginID = customerLoginID + 1
                
            #If a "customerLoginID" was not found in the "customerLogins" table in the "alsDB.db" database then assign the "addCustomerLoginID" variable to "1" to store in the "customerLogins" table " as the "customerLoginID". 
            else:
                
                #Assign the "addCustomerLoginID" the value "1" to store in the "customerAccountLogin" table in the "alsDB.db" database.
                addCustomerLoginID = 1

            #Enter into the "customerAccountLogin" table in the "alsDb.db" database the "customerLoginID", "customerUsername", "customerPassword" and the "customerAccountID" variables.
            cursor.execute("INSERT INTO customerAccountLogin(customerLoginID, customerUsername, customerPassword, customerID) VALUES(?,?,?,?)",(addCustomerLoginID, addCustomerUsername, addCustomerPassword, addCustomerAccountID))
            
            #Commit the entry to the "customerAccountLogin" table in the "alsDB.db" database.
            mydb.commit()
            
            #Create a customer message variable "customerAddedMsg" with a message to be passed to the "/user/loggedin/home.html" web-page and displayed with Jinja2.
            customerAddedMsg = "You succesfully added a new customer!"
            
            #Render the "/templates/user/loggedin/home.html" web-page when the system user has added a customer account sending the "customerAddedMsg" to the web-page to display using Jinja2.
            return render_template('user/loggedin/home.html', _customerAddedMsg = customerAddedMsg)
    
        #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
        elif session['userLoggedIn'] != True:

            #Render the "/templates/user/login.html" web-page when accessed with the system user is not logged in and the session variable "session['userLoggedIn']" is not set.
            return render_template('user/login.html')
    
    #Check if the "loginForm" from the "/user/login.html" web-page was submitted to allow access to the "/templates/user/loggedin/home.html" web-page".
    if request.args.get('f') == 'loginForm':
    
        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()

        #Get the users username from the "loginForm" and store in the "userUsername" variable.
        userUsername = request.form['userUsername']
        
        #Get the users password from the "loginForm" and store in the "userPassword" variable.
        userPassword = request.form['userPassword']
        
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''

        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "System user entered " + userUsername + " and " + userPassword + " as the credentials on /user/login route."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/user/login route accessed with attempt to login to /user/loggedin/home route."
        
        #Provide which section of the web-app was accessed.
        logUser = "Unknown User - Not Logged Into System"
        
        #Provide the location where the log was entered.
        logLocation = "/user/login"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()

        #Create a customer login table if not already exists to store the login details for the customer for each login "systemUserLogins" table within the "alsDB.db" database.
        sqlQ = ("CREATE TABLE IF NOT EXISTS systemUserLogins(userLoginID INT PRIMARY KEY, loginDate VARCHAR(255), username VARCHAR(255))")
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)
        
        #Try to select the details from the attemped login credentials on the "/templates/user/login.html" web-page.
        sqlQ = ("SELECT username, password FROM systemUserLogin WHERE username = ? AND password = ?")
        
        #Execute the "sqlQ" statement with the "userUsername" and "userPassword" variables collected from the "loginForm" on the "/templates/user/login.html" web-page.
        cursor.execute(sqlQ, (userUsername, userPassword,))
        
        #Count the number of rows within the "sqlQ" query.
        rows = len(cursor.fetchall())
        
        #If there is no credentials found in the "sqlQ" query, then provide a "loginFailMsg" to the user and return to the ".user/login.html" web-page.
        if rows == 0:
        
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''

            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "System user entered " + userUsername + " and " + userPassword + " as the wrong credentials on /user/login route."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "Failed login attempt on /user/loggedin/home route."
            
            #Provide which section of the web-app was accessed.
            logUser = "Unknown User - Not Logged Into System"
            
            #Provide the location where the log was entered.
            logLocation = "/user/login"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()

            #Provide a failed login message for the user to inform the user that the username and/or password credentials that was input was incorrect. 
            loginFailMsg  = "The username or password that you entered was incorrect. Please try again!"
            
            #Render the "/user/login.html" web-page sending the "loginFailMsg" message to the "/user/login/html" web-page upon failed login attempt.
            return render_template('/user/login.html', _loginFailMsg = loginFailMsg)

        #If the correct username and password credentials have been found in the "systemUserLogin" table within the "alsDB.db" then provide access to the "/user/loggedin/home.html" web-page.
        elif rows == 1:
        
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''

            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "System user entered " + userUsername + " and " + userPassword + " as the credentials on /user/home and was given access to /user/loggedin/home route."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "Login authorised to /user/loggedin/home route."
            
            #Provide which section of the web-app was accessed.
            logUser = userUsername
            
            #Provide the location where the log was entered.
            logLocation = "/user/login"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()

            #Store the current date and time of the system user login.
            loginDate = datetime.now()

            #Retrieve the "userLoginID" from the "systemUserLogins" table to find the last entered "userLoginID".
            sqlQ = "SELECT userLoginID FROM systemUserLogins ORDER BY userLoginID DESC LIMIT 1"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Initialise the "userLoginID" vairable to "0".
            userLoginID = 0
            #Loop through all the results from the "sqlQ" query.
            for loginID in cursor.fetchall():
                
                #Store the found "loginID" in the variable "userLoginID".
                userLoginID = loginID[0]
            
            #Increment the last found "userLoginID" from the "systemUserLogins" table in the "alsDB.db" database to get the new userLoginID to be stored for this login.
            userLoginID = userLoginID + 1
            
            #Insert into the "systemUserLogins" table in the "alsDB.db" the "userLoginID", "loginDate" and "userUsername" variables.
            cursor.execute("INSERT INTO systemUserLogins(userLoginID, loginDate, username) VALUES(?,?,?)",(userLoginID, loginDate,userUsername))
            
            #Commit the entry to the "alsDB.db" database.
            mydb.commit()
            
            #Retrieve the "sysUserID" from the "systemUserLogin" table within the "alsDB.db"
            sqlQ = "SELECT sysUserID FROM systemUserLogin WHERE username = ? AND password = ?"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ, (userUsername, userPassword))
            
            #loop through the cursor object to find the system users ID.
            for userID in cursor.fetchall():
                
                #Store the system users ID within the "sysUserID" variable.
                sysUserID = int(userID[0])
            
            #Store the "userUsername" variable within a session variable.
            session['userUsername'] = userUsername
            
            #Store the system users ID in a session variable.
            session['systemUserID'] = sysUserID

            #Store the system users ID in a session variable.
            session['userLoggedIn'] = True
            
            #Render the "/user/loggedin/home.html" file with the "session['userUsername']" variable sent to be displayed by Jinja2.
            return render_template('user/loggedin/home.html', _userUsername = session['userUsername'])

    #Check if the "updateAccountForm" was sumitted to collect the data from the form and update the customer account details with the submitted information on the "/templates/user/loggedin/updatecustomerdetails.html" web-page.
    if request.args.get('f') == 'updateAccountForm':
        
        #Check if the user is logged in with the session['loggedIn'] variable set when the correct credentials were entered on the "/templates/user/login.html" web-page to access the "/user/loggedin/home" route.
        if session['userLoggedIn'] == True:

            #Get the "customerIDDetails" from the "updateAccountForm" so the "customerAccount" table in the "alsDB.db" database can be updated with the form data for that customer with the retrieved "customerIDDetails".
            customerAccountID = request.form['customerIDDetails']
            
            #Get the "customerFirstName" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerFirstName" variable.
            addCustomerFirstName = request.form['customerFirstName']

            #Get the "customerLastName" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerLastName" variable.
            addCustomerLastName = request.form['customerLastName']

            #Get the "customerDateOfBirth" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerDateOfBirth" variable.
            addCustomerDateOfBirth = request.form['customerDateOfBirth']
            
            #Get the "customerResidentialAddress" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerResidentialAddress" variable.
            addCustomerResidentialAddress = request.form['customerResidentialAddress']
            
            #Get the "customerDateOfMoveIn" data from the "updateAccountForm" and store for updating the customer account details in the "customerDateOfMoveIn" variable.
            addCustomerDateOfMoveIn = request.form['customerDateOfMoveIn']
            
            #Get the "customerEmailAddress" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerEmailAddress" variable.
            addCustomerEmailAddress = request.form['customerEmailAddress']

            #Get the "customerPhoneNumber" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerPhoneNumber" variable.
            addCustomerPhoneNumber = request.form['customerPhoneNumber']
            
            #Get the "customerEmploymentStatus" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerEmploymentStatus" variable.
            addCustomerEmploymentStatus = request.form['customerEmploymentStatus']
            
            #Check if the "customerEmploymentStatus" select option from the "updateAccountForm" was submitted with the "Employed" options and details to be retrieved and updated in the "customerAccounts" table in the "alsDB.db" database, and any other employment options will be set as empty strings.
            if addCustomerEmploymentStatus == 'Employed':
                
                #Get the "customerDateEmploymentCommenced" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerDateEmploymentCommenced" variable.
                addCustomerDateEmploymentCommenced = request.form['customerDateEmploymentCommenced']

                #Get the "customerEmployerName" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerEmployerName" variable.
                addCustomerEmployerName = request.form['customerEmployerName']           

                #Get the "customerEmployerName" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerEmployerName" variable.
                addCustomerEmployerAddress = request.form['customerEmployerAddress']
                
                #Get the "customerEmployerContactNumber" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerEmployerContactNumber" variable.
                addCustomerEmployerContactNumber = request.form['customerEmployerContactNumber']

                #Initialse the "addCustomerLengthOfTimeAsSelfEmployed" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerLengthOfTimeAsSelfEmployed = ""

                #Initialse the "addCustomerCompanyName" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerCompanyName = ""
                
                #Initialse the "addCustomerCompanyAddress" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerCompanyAddress = ""
                
                #Initialse the "addCustomerGovernmentBenefitsDescription" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerGovernmentBenefitsDescription = ""

            #Check if the "customerEmploymentStatus" select option from the "updateAccountForm" was submitted with the "Self Employed" options and details to be retrieved and updated in the "customerAccounts" table in the "alsDB.db" database, and any other employment options will be set as empty strings.
            elif addCustomerEmploymentStatus == 'Self Employed':
            
                #Get the "customerLengthOfTimeAsSelfEmployed" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerLengthOfTimeAsSelfEmployed" variable.
                addCustomerLengthOfTimeAsSelfEmployed = request.form['customerLengthOfTimeAsSelfEmployed']

                #Get the "customerCompanyName" data from the "updateAccountForm" and store for updating the customer account details in the "customerCompanyName" variable.
                addCustomerCompanyName = request.form['customerCompanyName']
                
                #Get the "customerCompanyAddress" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerCompanyAddress" variable.
                addCustomerCompanyAddress = request.form['customerCompanyAddress']
                
                #Initialse the "addCustomerDateEmploymentCommenced" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerDateEmploymentCommenced = ""
                
                #Initialse the "addCustomerEmployerName" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerEmployerName = ""       

                #Initialse the "addCustomerEmployerName" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerEmployerAddress = ""
                
                #Initialse the "addCustomerEmployerContactNumber" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerEmployerContactNumber = ""

                #Initialse the "addCustomerGovernmentBenefitsDescription" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerGovernmentBenefitsDescription = ""
                
            #Check if the "customerEmploymentStatus" select option from the "updateAccountForm" was submitted with the "Government Benefits" options and details to be retrieved and updated in the "customerAccounts" table in the "alsDB.db" database, and any other employment options will be set as empty strings.
            elif customerEmploymentStatus == 'Government Benefits':
            
                #Get the "customerGovernmentBenefitsDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerGovernmentBenefitsDescription" variable.
                addCustomerGovernmentBenefitsDescription = request.form['customerGovernmentBenefits']
                
                #Initialse the "addCustomerLengthOfTimeAsSelfEmployed" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerLengthOfTimeAsSelfEmployed = ""

                #Initialse the "addCustomerCompanyName" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerCompanyName = ""
                
                #Initialse the "addCustomerCompanyAddress" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerCompanyAddress = ""
                
                #Initialse the "addCustomerDateEmploymentCommenced" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerDateEmploymentCommenced = ""
                
                #Initialse the "addCustomerEmployerName" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerEmployerName = ""                       
                
                #Initialse the "addCustomerEmployerAddress" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerEmployerAddress = ""
                
                #Initialse the "addCustomerEmployerContactNumber" as an empty string to update in the "customerAccounts" table in the "alsDB.db" database.
                addCustomerEmployerContactNumber = ""
            
            #Get the "customerGrossMonthlyIncome" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerGrossMonthlyIncome" variable.
            addCustomerGrossMonthlyIncome = request.form['customerGrossMonthlyIncome']
            
            #Get the "customerYearlyIncomeAfterTax" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerYearlyIncomeAfterTax" variable.
            addCustomerYearlyIncomeAfterTax= request.form['customerYearlyIncomeAfterTax']
            
            #Get the "customerMotorCostsDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerMotorCostsDescription" variable.
            addCustomerMotorCostsDescription = request.form['customerMotorCostsDescription']
            
            #Get the "customerFoodExpensesDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerFoodExpensesDescription" variable.
            addCustomerFoodExpensesDescription = request.form['customerFoodExpensesDescription']

            #Get the "customerClothingCostsDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerClothingCostsDescription" variable.
            addCustomerClothingExpensesDescription = request.form['customerClothingExpensesDescription']

            #Get the "customerChildcareCostsDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerChildcareCostsDescription" variable.
            addCustomerChildcareCostsDescription = request.form['customerChildcareCostsDescription']
            
            #Get the "customerHousingExpensesDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerHousingExpensesDescription" variable.
            addCustomerHousingExpensesDescription = request.form['customerHousingExpensesDescription']
            
            #Get the "customerHomeRentalCostsDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerHomeRentalCostsDescription" variable.
            addCustomerHomeRentalCostsDescription = request.form['customerHomeRentalCostsDescription']

            #Get the "customerMortgageRepaaymentsDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerMortgageRepaymentsDescription" variable.
            addCustomerMortgageRepaymentsDescription = request.form['customerMortgageRepaymentsDescription']

            #Get the "customerUtilityCostsDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerUtilityCostsDescription" variable.
            addCustomerUtilityCostsDescription = request.form['customerUtilityCostsDescription']

            #Get the "customerPhoneExpensesDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerPhoneExpensesDescription" variable.
            addCustomerPhoneExpensesDescription = request.form['customerPhoneExpensesDescription']
            
            #Get the "customerOtherExpensesDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerOtherExpensesDescription" variable.        
            addCustomerOtherExpensesDescription = request.form['customerOtherExpensesDescription']

            #Get the "customerOtherExpensesDescription" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerMotorCostsAmount" variable.        
            addCustomerMotorCostsAmount = request.form['customerMotorCostsAmount']
            
            #Get the "customerFoodExpensesAmount" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerFoodExpensesAmount" variable.        
            addCustomerFoodExpensesAmount = request.form['customerFoodExpensesAmount']
            
            #Get the "customerClothingCostsAmount" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerClothingCostsAmount" variable.                
            addCustomerClothingExpensesAmount = request.form['customerClothingExpensesAmount']
            
            #Get the "customerChildcareCostsAmount" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerChildcareCostsAmount" variable.                
            addCustomerChildcareCostsAmount = request.form['customerChildcareCostsAmount']

            #Get the "customerHousingExpensesAmount" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerHousingExpensesAmount" variable.                
            addCustomerHousingExpensesAmount = request.form['customerHousingExpensesAmount']
            
            #Get the "customerHomeRentalCostsAmount" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerHomeRentalCostsAmount" variable.                
            addCustomerHomeRentalCostsAmount = request.form['customerHomeRentalCostsAmount']
            
            #Get the "customerMortgageRepaymentsAmount" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerMortgageRepaymentsAmount" variable.                
            addCustomerMortgageRepaymentsAmount = request.form['customerMortgageRepaymentsAmount']
            
            #Get the "customerUtilityCostsAmount" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerUtilityCostsAmount" variable.                        
            addCustomerUtilityCostsAmount = request.form['customerUtilityCostsAmount']

            #Get the "customerPhoneExpensesAmount" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerPhoneExpensesAmount" variable.                        
            addCustomerPhoneExpensesAmount = request.form['customerPhoneExpensesAmount']
            
            #Get the "customerOtherExpensesAmount" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerOtherExpensesAmount" variable.                        
            addCustomerOtherExpensesAmount = request.form['customerOtherExpensesAmount']

            #Get the "customerTotalExpensesAmount" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerTotalExpensesAmount" variable.                        
            addCustomerTotalExpensesAmount = request.form['customerTotalExpensesAmount']

            #Get the "customerAccountUsername" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerUsername" variable.                        
            addCustomerUsername = request.form['customerAccountUsername']

            #Get the "customerAccountPassword" data from the "updateAccountForm" and store for updating the customer account details in the "addCustomerPassword" variable.                        
            addCustomerPassword = request.form['customerAccountPassword']
            
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()

            #Create a table if non-existent for the customer accounts data to be added 
            sqlQ = "CREATE TABLE IF NOT EXISTS customerAccounts(customerAccountID INT PRIMARY KEY, customerAccountCreatedDate VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), customerDateOfBirth VARCHAR(255), customerResidentialStatus VARCHAR(255), customerDateOfMoveIn VARCHAR(255), customerPhoneNumber VARCHAR(255), customerEmailAddress VARCHAR(255), customerEmploymentStatus VARCHAR(255), customerDateEmploymentCommenced VARCHAR(255), customerEmployerName VARCHAR(255), customerEmployerAddress VARCHAR(255), customerEmployerContactNumber VARCHAR(255), customerLengthOfTimeAsSelfEmployed VARCHAR(255), customerCompanyName VARCHAR(255), customerCompanyAddress VARCHAR(255), customerGovernmentBenefitsDescription VARCHAR(255), customerGrossMonthlyIncome VARCHAR(255), customerYearlyIncomeAfterTax VARCHAR(255), customerMotorCostsDescription VARCHAR(255), customerMotorCostsAmount VARCHAR(255), customerFoodExpensesDescription VARCHAR(255), customerFoodExpensesAmount VARCHAR(255), customerClothingExpensesDescription VARCHAR(255), customerClothingExpensesAmount VARCHAR(255), customerChildcareCostsDescription VARCHAR(255), customerChildcareCostsAmount VARCHAR(255), customerHousingCostsDescription VARCHAR(255), customerHousingCostsAmount VARCHAR(255), customerHomeRentalCostsDescription VARCHAR(255), customerHomeRentalCostsAmount VARCHAR(255), customerMortgageRepaymentsDescription VARCHAR(255), customerMortgageRepaymentsAmount VARCHAR(255), customerUtilityCostsDescription VARCHAR(255), customerUtilityCostsAmount VARCHAR(255), customerPhoneExpensesDescription VARCHAR(255), customerPhoneExpensesAmount VARCHAR(255), customerOtherExpensesDescription VARCHAR(255), customerOtherExpensesAmount VARCHAR(255), customerTotalExpensesAmount VARCHAR(255), customerAccountUsername VARCHAR(255), customerAccountPassword VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
            
            #Update the "customerAccounts" table in the "alsDB.db" database with the values of the "updateAccountForm" on the "/templates/user/loggedin/updatecustomerdetails.html" web-page for the customer account that was chosen for the updating of the customer account information.
            cursor.execute("UPDATE customerAccounts SET customerFirstName = ?, customerLastName = ?, customerDateOfBirth = ?, customerResidentialStatus = ?, customerDateOfMoveIn =?, customerPhoneNumber = ?, customerEmailAddress = ?, customerEmploymentStatus = ?, customerDateEmploymentCommenced = ?, customerEmployerName = ?, customerEmployerAddress = ?, customerEmployerContactNumber = ?, customerLengthOfTimeAsSelfEmployed = ?, customerCompanyName = ?, customerCompanyAddress = ?, customerGovernmentBenefitsDescription = ?, customerGrossMonthlyIncome = ?, customerYearlyIncomeAfterTax = ?, customerMotorCostsDescription = ?, customerMotorCostsAmount = ?, customerFoodExpensesDescription = ?, customerFoodExpensesAmount = ?, customerClothingExpensesDescription = ?, customerClothingExpensesAmount = ?, customerChildcareCostsDescription = ?, customerChildcareCostsAmount = ?, customerHousingCostsDescription = ?, customerHousingCostsAmount = ?, customerHomeRentalCostsDescription = ?, customerHomeRentalCostsAmount = ?, customerMortgageRepaymentsDescription = ?, customerMortgageRepaymentsAmount = ?, customerUtilityCostsDescription = ?, customerUtilityCostsAmount = ?, customerPhoneExpensesDescription = ?, customerPhoneExpensesAmount = ?, customerOtherExpensesDescription = ?, customerOtherExpensesAmount = ?, customerTotalExpensesAmount = ?, customerAccountPassword = ?, customerAccountUsername = ? WHERE customerAccountID = ?", (addCustomerFirstName,addCustomerLastName, addCustomerDateOfBirth, addCustomerResidentialAddress, addCustomerDateOfMoveIn, addCustomerPhoneNumber, addCustomerEmailAddress, addCustomerEmploymentStatus, addCustomerDateEmploymentCommenced, addCustomerEmployerName, addCustomerEmployerAddress, addCustomerEmployerContactNumber, addCustomerLengthOfTimeAsSelfEmployed, addCustomerCompanyName, addCustomerCompanyAddress, addCustomerGovernmentBenefitsDescription, addCustomerGrossMonthlyIncome, addCustomerYearlyIncomeAfterTax, addCustomerMotorCostsDescription, addCustomerMotorCostsAmount, addCustomerFoodExpensesDescription, addCustomerFoodExpensesAmount, addCustomerClothingExpensesDescription, addCustomerClothingExpensesAmount, addCustomerChildcareCostsDescription, addCustomerChildcareCostsAmount, addCustomerHousingExpensesDescription, addCustomerHousingExpensesAmount, addCustomerHomeRentalCostsDescription, addCustomerHomeRentalCostsAmount, addCustomerMortgageRepaymentsDescription, addCustomerMortgageRepaymentsAmount, addCustomerUtilityCostsDescription, addCustomerUtilityCostsAmount, addCustomerPhoneExpensesDescription, addCustomerPhoneExpensesAmount, addCustomerOtherExpensesDescription, addCustomerOtherExpensesAmount, addCustomerTotalExpensesAmount, addCustomerPassword, addCustomerUsername, customerAccountID))
            
            #Commit the update of the customer account details to the "alsDB.db" database.
            mydb.commit()

            #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
            userUsername = session['userUsername']
        
            #Create a variable "updatedCustomerAccountMsg" to inform the system user that the customer account was updated succesfully to send to the "/templates/user/loggedin/home.html" web-page to display using Jinja2.
            updatedCustomerAccountMsg = "You succesfully updated details of customer with the customerAccountID " + customerAccountID
            
            #Render the "/templates/user/loggedin/home.html" web-page returning the "updatedCustomerAccountMsg" and the "userUsername" variables to the web-page.
            return render_template('user/loggedin/home.html', _updatedCustomerAccountMsg = updatedCustomerAccountMsg, _userUsername = userUsername)
            
        #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
        elif session['userLoggedIn'] != True:
            
            #Render the "/templates/user/login.html" web-page when accessed with the system user is not logged in and the session variable "session['userLoggedIn']" is not set.
            return render_template('user/login.html')
    
    #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
    userUsername = session['userUsername']
        
    #Render the "/templates/user/loggedin/home.html" returning the "session['userUsername']" to be displayed using Jinja2.
    return render_template('user/loggedin/home.html', _userUsername = userUsername)
    
'''
The "addcustomer()" route renders the "/templates/user/loggedin/addcustomer.html" web-page displayed to the user to provide the system user to add a new customer audit account details.
'''
@app.route('/user/loggedin/addcustomer', methods=['GET','POST'])
def addcustomer():
    
    #If the "session['userLoggedIn']" variable is set to "True" then the user will be directed to the "/user/loggedin/addcustomer" route.
    if session['userLoggedIn'] == True:
    
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''
    
        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
        userUsername = session['userUsername']
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "System user " + userUsername + " accessed /user/loggedin/addcustomer route."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/user/loggedin/addcustomer route accessed."
        
        #Provide which section of the web-app was accessed.
        logUser = userUsername
        
        #Provide the location where the log was entered.
        logLocation = "/user/loggedin/addcustomer"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()
        
        #
        return render_template('user/loggedin/addcustomer.html', _userUsername = userUsername)

    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
    
        #Create an informative message to the user that they are not logged in to the user system.
        notLoggedInMsg = "You are not logged in. Log in to continue to the User - Audit Log Service API!"
        
        #Render the "/templates/user/login.html" web-page if the "session['userLoggedIn']" variable is not set to "True".
        return render_template('user/login.html', _notLoggedInMsg = notLoggedInMsg)

'''
The "viewcust()" function allows the logged in system user access to view all the customer accounts on the "/templates/user/loggedin/viewcustomers.html" web-page.
'''
@app.route('/user/loggedin/viewcustomers', methods=['GET','POST'])
def viewcust():
    
    #Check if the user is logged in with the session['userLoggedIn'] variable set when the correct credentials were entered on the "/templates/user/login.html" web-page to access the "/user/loggedin/viewcustomers" route.
    if session['userLoggedIn'] == True:
    
        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        #Create the "customerAccounts" table in the "alsDB.db" if non-existent.
        sqlQ = "CREATE TABLE IF NOT EXISTS customerAccounts(customerAccountID INT PRIMARY KEY, customerAccountCreatedDate VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), customerDateOfBirth VARCHAR(255), customerResidentialStatus VARCHAR(255), customerDateOfMoveIn VARCHAR(255), customerPhoneNumber VARCHAR(255), customerEmailAddress VARCHAR(255), customerEmploymentStatus VARCHAR(255), customerDateEmploymentCommenced VARCHAR(255), customerEmployerName VARCHAR(255), customerEmployerAddress VARCHAR(255), customerEmployerContactNumber VARCHAR(255), customerLengthOfTimeAsSelfEmployed VARCHAR(255), customerCompanyName VARCHAR(255), customerCompanyAddress VARCHAR(255), customerGovernmentBenefitsDescription VARCHAR(255), customerGrossMonthlyIncome VARCHAR(255), customerYearlyIncomeAfterTax VARCHAR(255), customerMotorCostsDescription VARCHAR(255), customerMotorCostsAmount VARCHAR(255), customerFoodExpensesDescription VARCHAR(255), customerFoodExpensesAmount VARCHAR(255), customerClothingExpensesDescription VARCHAR(255), customerClothingExpensesAmount VARCHAR(255), customerChildcareCostsDescription VARCHAR(255), customerChildcareCostsAmount VARCHAR(255), customerHousingCostsDescription VARCHAR(255), customerHousingCostsAmount VARCHAR(255), customerHomeRentalCostsDescription VARCHAR(255), customerHomeRentalCostsAmount VARCHAR(255), customerMortgageRepaymentsDescription VARCHAR(255), customerMortgageRepaymentsAmount VARCHAR(255), customerUtilityCostsDescription VARCHAR(255), customerUtilityCostsAmount VARCHAR(255), customerPhoneExpensesDescription VARCHAR(255), customerPhoneExpensesAmount VARCHAR(255), customerOtherExpensesDescription VARCHAR(255), customerOtherExpensesAmount VARCHAR(255), customerTotalExpensesAmount VARCHAR(255), customerAccountUsername VARCHAR(255), customerAccountPassword VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)
        
        #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
        usersUsername = session['userUsername']
        
        #Check if the "sort" form was submitted for sorting the customer account details if the system user had sorted on the select box and then submitted the query on the "/user/loggedin/viewcustomers" route, then will return the "/templates/user/loggedin/viewcustomers.html" web-page.
        if request.args.get('f') == 'sort':
            
            #Get the value of the value from the "/user/loggedin/viewcustomers" route "sortbox" "sortbox" stored in the "sortedAccounts" variable.
            sortedAccounts = request.form['sortbox']
            
            #Select all the customer data from the "customerAccounts" table in the "alsDB.db" database to check if there is any customer accounts in the "customerAccounts" table.
            sqlQ = "SELECT * FROM customerAccounts"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
            
            #Calculate the number of rows in the "sqlQ" query.
            rows = len(cursor.fetchall())
            
            #If there is a row or rows of customer details found in the "sqlQ" then the sorted customer accounts can be selected from the "customerAccounts" table in the "alsDB.db" database.
            if rows > 0:
                
                #If the system user selected to sort the customer account via the customers first name then the customer details will be selected and sent to the "/templates/user/loggedin/viewcustomers.html" web-page in the alphabetical order of the customers first name from the "customerAccounts" table in the "alsDB.db" database.
                if sortedAccounts == 'Customer First Name Ascending Order':
                    
                    #Select the customer accounts in alphabetical order of the "customerFirstName" from the "customerAccounts" table in the "alsDB.db" database.
                    sqlQ = "SELECT * FROM customerAccounts ORDER BY customerFirstName ASC"
                    
                    #Create a variable with a message to inform the system user that the customer accounts are sorted in ascending alphabetical order of the customers first name values.
                    sortedMsg = "The customer accounts have been sorted in ascending first name alphabetical order."
                    
                #Select the customer accounts in  descending alphabetical order of the "customerFirstName" from the "customerAccounts" table in the "alsDB.db" database.
                elif sortedAccounts == 'Customer First Name Descending Order':
                    
                    #Select the customer accounts in descending alphabetical order of the "customerFirstName" from the "customerAccounts" table in the "alsDB.db" database.
                    sqlQ = "SELECT * FROM customerAccounts ORDER BY customerFirstName DESC"
                    
                    #Create a variable with a message to inform the system user that the customer accounts are sorted in descending alphabetical order of the customers first name values.
                    sortedMsg = "The customer accounts have been sorted in descending first name alphabetical order."

                elif sortedAccounts == 'Customer Last Name Ascending Order':
                    
                    #Select the customer accounts in ascending alphabetical order of the "customerLastName" from the "customerAccounts" table in the "alsDB.db" database.
                    sqlQ = "SELECT * FROM customerAccounts ORDER BY customerLastName ASC"
                    
                    #Create a variable with a message to inform the system user that the customer accounts are sorted in ascending alphabetical order of the customers last name values.
                    sortedMsg = "The customer accounts have been sorted in ascending last name alphabetical order."
                    
                #Select the customer accounts in  descending alphabetical order of the "customerLastName" from the "customerAccounts" table in the "alsDB.db" database.
                elif sortedAccounts == 'Customer Last Name Descending Order':
                    
                    #Select the customer accounts in descending alphabetical order of the "customerLastName" from the "customerAccounts" table in the "alsDB.db" database.
                    sqlQ = "SELECT * FROM customerAccounts ORDER BY customerLastName DESC"
                    
                    #Create a variable with a message to inform the system user that the customer accounts are sorted in descending alphabetical order of the customers first name values.last
                    sortedMsg = "The customer accounts have been sorted in descending last name alphabetical order."

                #Select the customer accounts in ascending order of the "customerAccountID" from the "customerAccounts" table in the "alsDB.db" database.
                elif sortedAccounts == 'CustomerID Ascending Order':
                
                    #Select the customer accounts in ascending order of the "customerAccountID" from the "customerAccounts" table in the "alsDB.db" database.
                    sqlQ = "SELECT * FROM customerAccounts ORDER BY customerAccountID ASC" 
                
                    #Create a variable with a message to inform the system user that the customer accounts are sorted in ascending order of the customers ID values.
                    sortedMsg = "The customer accounts have been sorted by the customer account ID in ascending order."

                #Select the customer accounts in descending order of the "customerAccountID" from the "customerAccounts" table in the "alsDB.db" database.
                elif sortedAccounts == 'CustomerID Descending Order':
                
                    #Select the customer accounts in descending order of the "customerAccountID" from the "customerAccounts" table in the "alsDB.db" database.
                    sqlQ = "SELECT * FROM customerAccounts ORDER BY customerAccountID DESC"
                    
                    #Create a variable with a message to inform the system user that the customer accounts are sorted in ascending order of the customers ID values.
                    sortedMsg = "The customer accounts have been sorted by the customer account ID in descending order."
                    
                #Execute the "sqlQ" query.
                cursor.execute(sqlQ)
                
                #Store the "sqlQ" results in the "customerAccountDetails" variable to send to the "/templates/user/loggedin/viewcustomers.html" web-page to be displayed using Jinja2.
                customerAccounts = cursor.fetchall()
                
                #Render the "/templates/user/loggedin/viewcustomers.html" web-page sending the "customerAccountDetails" to the web-page with the system users session username.
                return render_template('user/loggedin/viewcustomers.html', _customerAccounts = customerAccounts, _usersUsername = usersUsername, _sortedMsg = sortedMsg)        

        #Select all the details from the "customerAccounts" table in the "alsDB.db" to send to the "/templates/user/loggedin/viewcustomers.html" web-page for viewing to the system user.
        sqlQ = "SELECT * FROM customerAccounts"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)
        
        #Store the "sqlQ" query results in the "customerAccountDetails" variable to be sent to the "/templates/user/loggedin/viewcustomers.html" web-page to be displayed using Jinja2.
        customerAccounts = cursor.fetchall()
        
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''
            
        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
        userUsername = session['userUsername']
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "System user " + userUsername + " accessed /user/loggedin/viewcustomers route."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/user/loggedin/viewcustomers route accessed."
        
        #Provide which section of the web-app was accessed.
        logUser = userUsername
        
        #Provide the location where the log was entered.
        logLocation = "/user/loggedin/viewcustomers"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()

        #Render the "/templates/user/loggedin/viewcustomers.html" web-page with the "customerAccountDetails" variable and the users session username to be passed to the web-page and displayed using Jinja2.
        return render_template('user/loggedin/viewcustomers.html', _customerAccounts = customerAccounts, _usersUsername = usersUsername)
        
    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
        
        #Render the "/templates/user/login.html" web-page when accessed with the system user is not logged in and the session variable "session['userLoggedIn']" is not set.
        return render_template('user/login.html')

'''
The "custupdate()" function displays the "/templates/user/loggedin/updatecustomer.html" web-page to the logged in system user to select a customer account and render the "/templates/user/loggedin/updatecustomerdetails.html" web-page when the system user has chosen a customer account to update.
'''
@app.route('/user/loggedin/updatecustomers', methods=['GET','POST'])
def custupdate():
    
    #Check if the user is logged in with the session['userLoggedIn'] variable set when the correct credentials were entered on the "/templates/user/login.html" web-page to access the "/user/loggedin/updatecustomers" route.
    if session['userLoggedIn'] == True:
    
        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
        usersUsername = session['userUsername']
        
        #If the system user has pressed the "sortBtn" to sort the customer accounts and the "sortUpdateAccounts" form has been submitted then the customer accounts will be selected and the details sent to the "/templates/user/loggedin/updatecustomer.html" web-page in the sorted order selected.
        if request.args.get('f') == 'sortUpdateAccounts':
            
            #Store the option from the "sortAccountsBox" select box in the "sortedAccounts" variable.
            sortedAccounts = request.form['sortAccountsBox']
            
            #If the system user has selected to sort the customer accounts by customer first name in ascending order then the query will be selected and the results will be displayed to the system user in that order on the "/templates/user/loggedin/updatecustomer.html" web-page.
            if sortedAccounts == 'Customer First Name Ascending Order':
            
                #Select the customer accounts sorted by the "firstName" in alphabetical ascending order.
                sqlQ = "SELECT * FROM customerAccounts ORDER BY customerFirstName ASC"
                
                #Create a message to be displayed to the system user stating the customer accounts are sorted in ascending alphabetical order by the customers first name. 
                sortedMsg = "The customer accounts have been sorted by the first name in alphabetical ascending order."
                
            #If the system user has selected to sort the customer accounts by customer first name in descending order then the query will be selected and the results will be displayed to the system user in that order on the "/templates/user/loggedin/updatecustomer.html" web-page.
            elif sortedAccounts == 'Customer First Name Descending Order':
            
                #Select the customer accounts sorted by the "firstName" in alphabetical descending order.
                sqlQ = "SELECT * FROM customerAccounts ORDER BY customerFirstName DESC"
            
                #Create a message to be displayed to the system user stating the customer accounts are sorted in descending alphabetical order by the customers first name. 
                sortedMsg = "The customer accounts have been sorted by the first name in alphabetical descending order."

            #If the system user has selected to sort the customer accounts by customer last name in ascending order then the query will be selected and the results will be displayed to the system user in that order on the "/templates/user/loggedin/updatecustomer.html" web-page.
            elif sortedAccounts == 'Customer Last Name Ascending Order':
            
                #Select the customer accounts sorted by the "lastName" in alphabetical ascending order.
                sqlQ = "SELECT * FROM customerAccounts ORDER BY customerLastName ASC"
                
                #Create a message to be displayed to the system user stating the customer accounts are sorted in ascending alphabetical order by the customers last name. 
                sortedMsg = "The customer accounts have been sorted by the last name in alphabetical ascending order."

            #If the system user has selected to sort the customer accounts by customer last name in descending order then the query will be selected and the results will be displayed to the system user in that order on the "/templates/user/loggedin/updatecustomer.html" web-page.
            elif sortedAccounts == 'Customer Last Name Descending Order':
            
                #Select the customer accounts sorted by the "lastName" in alphabetical descending order.
                sqlQ = "SELECT * FROM customerAccounts ORDER BY customerLastName DESC"
                
                #Create a message to be displayed to the system user stating the customer accounts are sorted in descending alphabetical order by the customers last name. 
                sortedMsg = "The customer accounts have been sorted by the last name in alphabetical descending order."

            #If the system user has selected to sort the customer accounts by customer account ID in ascending order then the query will be selected and the results will be displayed to the system user in that order on the "/templates/user/loggedin/updatecustomer.html" web-page.
            elif sortedAccounts == 'CustomerID Ascending Order':
            
                #Select the customer accounts sorted by the "customerID" in ascending order.
                sqlQ = "SELECT * FROM customerAccounts ORDER BY customerAccountID ASC"
                
                #Create a message to be displayed to the system user stating the customer accounts are sorted in descending order by the customers account ID.
                sortedMsg = "The customer accounts have been sorted by the customer account ID's in ascending order."

            #If the system user has selected to sort the customer accounts by customer account ID in descending order then the query will be selected and the results will be displayed to the system user in that order on the "/templates/user/loggedin/updatecustomer.html" web-page.
            elif sortedAccounts == 'CustomerID Descending Order':
            
                #Select the customer accounts sorted by the "customerID" in descending order.
                sqlQ = "SELECT * FROM customerAccounts ORDER BY customerAccountID DESC"
                
                #Create a message to be displayed to the system user stating the customer accounts are sorted in descending order by the customers account ID.
                sortedMsg = "The customer accounts have been sorted by the customer account ID in descending order."
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
            
            #Store the customer accounts found from the "sqlQ" query in the "customerAccounts" variable to send to the "/templates/user/loggedin/updatecustomer.html" web-page.
            customerAccounts = cursor.fetchall()
            
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
            userUsername = session['userUsername']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "System user " + userUsername + " accessed /user/loggedin/updatecustomers route."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/user/loggedin/updatecustomers route accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = userUsername
            
            #Provide the location where the log was entered.
            logLocation = "/user/loggedin/updatecustomers"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()
            
            #Render the "/templates/user/loggedin/updatecustomer.html" returning the customer accounts data, the sorted message to the system user and the system users username to be displayed using Jinja2.
            return render_template('user/loggedin/updatecustomer.html', _customerAccounts = customerAccounts, _sortedMsg = sortedMsg, _userUsername = usersUsername)

        #Select all the customer accounts from the "customerAccounts" table from the "alsDB.db" database.
        sqlQ = "SELECT * FROM customerAccounts"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)
        
        #Store the "sqlQ" query results in the "customerAccounts" variable.
        customerAccounts = cursor.fetchall()
        
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''
    
        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
        userUsername = session['userUsername']
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "System user " + userUsername + " accessed /user/loggedin/updatecustomers route."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/user/loggedin/updatecustomers route accessed."
        
        #Provide which section of the web-app was accessed.
        logUser = userUsername
        
        #Provide the location where the log was entered.
        logLocation = "/user/loggedin/updatecustomers"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()
        
        #Render the "/templates/user/loggedin/updatecustomer.html" returning the customer accounts data and the system users username to be displayed using Jinja2.
        return render_template('user/loggedin/updatecustomer.html', _customerAccounts = customerAccounts, _userUsername = usersUsername)
  
    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
        
        #Render the "/templates/user/login.html" web-page when accessed with the system user is not logged in and the session variable "session['userLoggedIn']" is not set.
        return render_template('user/login.html')
  
'''
The "updatecustform()" function selects the details of the customer account to be updated and updates the selected customer account in the "customerAccounts" table in the "alsDB.db" database.
'''
@app.route('/user/loggedin/updatecustomerdetails', methods=['GET','POST'])
def updatecustform():

    #Check if the user is logged in if the "session['userLoggedIn']" variable is asigned from the "/user/loggedin/home" route.
    if session['userLoggedIn'] == True:
    
        #Check if the form submitted was the "updateAccountForm" from the "/templates/user/loggedin/updatecustomer.html" web-page.
        if request.args.get('f') == 'updateCustomerAccount':
            
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
            usersUsername = session['userUsername']
            
            #Get the "customerIDDetails" which is the name of the hidden input on the "/templates/user/loggedin/updatecustomer.html" web-page with the "customerAccountID" of the customer account to be updated.
            customerDetailsID = request.form['customerIDDetails']
            
            #Select the customer details with the "customerAccountID"  of the customer selected from the "/templates/user/loggedin/updatecustomer.html" web-page from the "customerAccount" table of the "alsDB.db" database.
            sqlQ = "SELECT * FROM customerAccounts WHERE customerAccountID = ?"
            
            #Execute the "sqlQ" query providing the "customerAccountID" to select that customers account with that "customerAccountID".
            cursor.execute(sqlQ, (customerDetailsID,))
            
            #Store the details of the "sqlQ" query to the "customerDetails" variable.
            customerDetails = cursor.fetchall()
            
            #Initialise the index "i" variable to "0"
            i = 0
            
            #Initialise the "customerAccounts" variable as an empty dictionary.
            customerDict = {}
            
            #Loop through the "customerDetails" "sqlQ" results to store in the "customerDict" dictionary.
            for account in customerDetails:
                for info in account:
                    
                    #Store each of the account details in the "customerDetailsVar" variable.
                    customerDetailsVar = {i:info}
                    
                    #Increment the index "i" value to store for each data in "customerDict" dictionary.
                    i = i + 1
                    
                    #Update the "customerDict" dictionary with each of the "customerDetailsVar" data.
                    customerDict.update(customerDetailsVar)
                    
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
            userUsername = session['userUsername']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "System user " + userUsername + " updated the customer with ID " + customerDetailsID + " on the /user/loggedin/updatecustomerdetails route."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/user/loggedin/updatecustomerdetails route accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = userUsername
            
            #Provide the location where the log was entered.
            logLocation = "/user/loggedin/updatecustomerdetails"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()
            
            #Render the "/templates/user/loggedin/updatecustomerdetails.html" web-page providing the customer details of the customer account to the web-page to be edited to update those customer details and the users username to be displayed using Jinja2.
            return render_template('user/loggedin/updatecustomerdetails.html', _customerDict = customerDict, _userUsername = usersUsername)
        
    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
        
        #Render the "/templates/user/login.html" web-page when accessed with the system user is not logged in and the session variable "session['userLoggedIn']" is not set.
        return render_template('user/login.html')
    
'''
The "deleted()" function allows the system user to view and delete selected customer accounts that are displayed on the "/templates/user/loggedin/deleted.html" web-page.
'''
@app.route('/user/loggedin/deletecustomeraccounts', methods=['GET','POST'])
def deleted():

    #Check if the user is logged in if the "session['userLoggedIn']" variable is asigned from the "/user/loggedin/home" route.
    if session['userLoggedIn'] == True:

        #Check if the "sortDelete" form has been submitted
        if request.args.get('f') == 'sortDelete':
            
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()

            #Store the "sortAccounts" option from the select box on the "sortDelete" form on the "deleted.html" in the "sortedAccounts" variable.
            sortedAccounts = request.form['sortAccounts']
            
            #If the "sortedAccounts" select box option is chosen to sort the customer accounts by the first name in ascending alphabetical order then the customer account details will be selected, stored in the "sqlQ" query variable and displayed to the system user sorted.
            if sortedAccounts == 'Customer First Name Ascending Order':
            
                #Select all the customer account details from the "customerAccounts" table in the "alsDB.db" database ordered by the "customerFirstName" field in alphabetical order ascending.
                sqlQ = "SELECT * FROM customerDetails ORDER BY customerFirstName ASC"
                
            #If the "sortedAccounts" select box option is chosen to sort the customer accounts by the first name in descending alphabetical order then the customer account details will be selected, stored in the "sqlQ" query variable and displayed to the system user sorted.
            elif sortedAccounts == 'Customer First Name Descending Order':
            
                #Select all the customer account details from the "customerAccounts" table in the "alsDB.db" database ordered by the "customerFirstName" field in alphabetical order descending.
                sqlQ = "SELECT * FROM customerDetails ORDER BY customerFirstName DESC"

            #If the "sortedAccounts" select box option is chosen to sort the customer accounts by the last name in ascending alphabetical order then the customer account details will be selected, stored in the "sqlQ" query variable and displayed to the system user sorted.
            elif sortedAccounts == 'Customer Last Name Ascending Order':

                #Select all the customer account details from the "customerAccounts" table in the "alsDB.db" database ordered by the "customerLastName" field in alphabetical order ascending.
                sqlQ = "SELECT * FROM customerDetails ORDER BY customerLastName ASC"
                
            #If the "sortedAccounts" select box option is chosen to sort the customer accounts by the last name in descending alphabetical order then the customer account details will be selected, stored in the "sqlQ" query variable and displayed to the system user sorted.
            elif sortedAccounts == 'Customer Last Name Descending Order':
            
                #Select all the customer account details from the "customerAccounts" table in the "alsDB.db" database ordered by the "customerLastName" field in alphabetical order descending.
                sqlQ = "SELECT * FROM customerDetails ORDER BY customerLastName DESC"
                
            #If the "sortedAccounts" select box option is chosen to sort the customer accounts by the "customerAccountID" in ascending order then the customer account details will be selected, stored in the "sqlQ" query variable and displayed to the system user sorted.
            elif sortedAccounts == 'CustomerID Ascending Order':
            
                #Select all the customer account details from the "customerAccounts" table in the "alsDB.db" database ordered by the "customerAccountID" field in descending order.
                sqlQ = "SELECT * FROM customerDetails ORDER BY customerAccountID ASC"
                
            #If the "sortedAccounts" select box option is chosen to sort the customer accounts by the "customerAccountID" in descending order then the customer account details will be selected, stored in the "sqlQ" query variable and displayed to the system user sorted.
            elif sortedAccounts == 'CustomerID Descending Order':
            
                #Select all the customer account details from the "customerAccounts" table in the "alsDB.db" database ordered by the "customerAccountID" field in descending order.
                sqlQ = "SELECT * FROM customerAccounts ORDER BY customerAccountID DESC"

            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
            
            #Store the "sqlQ" query in the "customerAccounts" variable to pass to the "/templates/user/loggedin/deleted.html" web-page to be displayed using Jinja2.
            customerAccountsDetails = cursor.fetchall()
            
            #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
            usersUsername = session['userUsername']
            
            #Render the "/templates/user/loggedin/deleted.html" web-page passing the "customerAccountsDetails" and the "session['userUsername']" variables to be displayed using Jinja2.
            return render_template('/user/loggedin/deleted.html', _customerAccountsDetails = customerAccountsDetails, _userUsername = usersUsername)
            
        #Check if the "deleteCustomerAccount" form was submitted on the "/templates/user/loggedin/deleted.html" to delete the customer account that was selected by the system user for deletion.
        if request.args.get('f') == 'deleteCustomerAccount':
            
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Get the "deleteCustomerDetails" hidden form input from the "deleteCustomerAccount" form of the "/templates/user/loggedin/deleted.html" and store the value in the "accountID" variable to find customer account to delete.
            accountID = request.form['deleteCustomerDetails']
            
            #Delete from the "customerAccounts" table in the "alsDB.db" database.the details with the primary "customerAccountID" ID with the value of the "accountID" variable.
            sqlQ = "DELETE FROM customerAccounts WHERE customerAccountID = ?"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ, (accountID,))
 
            #Create a "deletedAccountMsg" variable to inform the system user that the selected account was deleted.
            deletedCustomerAccountMsg = "The customer account with the customer account ID " + accountID + " has been deleted."
            
            #Select all the customer accounts from the "customerAccounts" table in the "alsDB.db" database to display to the user on the "/templates/user/loggedin/deleted.html" web-page.
            sqlQ = "SELECT * FROM customerAccounts"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
            
            #Commit the changes to the "alsDB.db" database.
            mydb.commit()
            
            #Store all the customer accounts from the "customerAccounts" table in the "alsDB.db" database in the "customerAccountDetails" variable.
            customerAccountsDetails = cursor.fetchall()

            #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
            usersUsername = session['userUsername']
            
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
            userUsername = session['userUsername']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "System user " + userUsername + " deleted the customer account with the ID." + accountID + "."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/user/loggedin/deletecustomeraccounts route accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = userUsername
            
            #Provide the location where the log was entered.
            logLocation = "/user/loggedin/deletecustomeraccounts"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()
            
            #Render the "/templates/user/loggedin/deleted.html" web-page to the system user sending the "customerAccountsDetails" , the "deletedAccountMsg" and the "session['userUsername']" variables to the web-page for display using Jinja2.
            return render_template('user/loggedin/deleted.html', _customerAccountsDetails = customerAccountsDetails, _deletedCustomerAccountMsg = deletedCustomerAccountMsg)
        
        #If the system user has just accessed the "/templates/user/loggedin/deleted.html" web-page without having submitted the "sortDelete" form or the "deleteCustomerAccount" form then the system user will just be displayed the customer accounts that are ready for deletion.
        else:
            
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Select all the customer accounts from the "customerAccounts" table in the "alsDB.db" database to display to the user using Jinja2 on the "/templates/user/loggedin/deleted.html"web-page.
            sqlQ = "SELECT * FROM customerAccounts"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
            
            #Store the customer accounts from the "sqlQ" query in the "customerAccountDetails" variable to pass to the "/templates/user/loggedin/deleted.html" web-page displayed using Jinja2.
            customerAccountsDetails = cursor.fetchall()

            #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
            usersUsername = session['userUsername']
            
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
            userUsername = session['userUsername']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "System user " + userUsername + " accessed the /user/loggedin/deletecustomeraccounts route."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/user/loggedin/deletecustomeraccounts route accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = userUsername
            
            #Provide the location where the log was entered.
            logLocation = "/user/loggedin/deletecustomeraccounts"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()
            
            #Render the "/templates/user/loggedin/deleted.html" web-page sending the "usersUsername" and the "customerAccountsDetails" variable for display using Jinja2.
            return render_template('user/loggedin/deleted.html', _customerAccountsDetails = customerAccountsDetails, _userUsername = usersUsername)

    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
        
        #Render the "/user/login.html" web-page if the "session['loggedIn']" variable is not set to "True".
        return render_template('user/login.html')

'''
The "auditview()" function allows the system user to view all customer account details so that a customer account can be selected and an audit created and sent to the customer.
'''
@app.route('/user/loggedin/createsendaudits', methods=['GET','POST'])
def auditview():
    
    #Check if the user is logged in if the "session['userLoggedIn']" variable is asigned from the "/user/loggedin/home" route.
    if session['userLoggedIn'] == True:
                    
        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()

        #Create the "customerAccounts" table in the "alsDB.db" if non-existent.
        sqlQ = "CREATE TABLE IF NOT EXISTS customerAccounts(customerAccountID INT PRIMARY KEY, customerAccountCreatedDate VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), customerDateOfBirth VARCHAR(255), customerResidentialStatus VARCHAR(255), customerDateOfMoveIn VARCHAR(255), customerPhoneNumber VARCHAR(255), customerEmailAddress VARCHAR(255), customerEmploymentStatus VARCHAR(255), customerDateEmploymentCommenced VARCHAR(255), customerEmployerName VARCHAR(255), customerEmployerAddress VARCHAR(255), customerEmployerContactNumber VARCHAR(255), customerLengthOfTimeAsSelfEmployed VARCHAR(255), customerCompanyName VARCHAR(255), customerCompanyAddress VARCHAR(255), customerGovernmentBenefitsDescription VARCHAR(255), customerGrossMonthlyIncome VARCHAR(255), customerYearlyIncomeAfterTax VARCHAR(255), customerMotorCostsDescription VARCHAR(255), customerMotorCostsAmount VARCHAR(255), customerFoodExpensesDescription VARCHAR(255), customerFoodExpensesAmount VARCHAR(255), customerClothingExpensesDescription VARCHAR(255), customerClothingExpensesAmount VARCHAR(255), customerChildcareCostsDescription VARCHAR(255), customerChildcareCostsAmount VARCHAR(255), customerHousingCostsDescription VARCHAR(255), customerHousingCostsAmount VARCHAR(255), customerHomeRentalCostsDescription VARCHAR(255), customerHomeRentalCostsAmount VARCHAR(255), customerMortgageRepaymentsDescription VARCHAR(255), customerMortgageRepaymentsAmount VARCHAR(255), customerUtilityCostsDescription VARCHAR(255), customerUtilityCostsAmount VARCHAR(255), customerPhoneExpensesDescription VARCHAR(255), customerPhoneExpensesAmount VARCHAR(255), customerOtherExpensesDescription VARCHAR(255), customerOtherExpensesAmount VARCHAR(255), customerTotalExpensesAmount VARCHAR(255), customerAccountUsername VARCHAR(255), customerAccountPassword VARCHAR(255))"

        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)
        
        #Check if the "searchForm" form was submitted by the system user which provided a detail of the customer account to be searched and will then provide and display the result(s) to the system user on the "/templates/user/loggedin/createsendaudits.html" web-page.
        if request.args.get('f') == 'searchForm':
            
            #Retrieve and store the selected option from the "searchForm" form so the sql query results in the "customerAccounts" table in the "alsDb.db" will be selected based on that selected option.
            selectBoxResult = request.form['selectBox']
            
            #Retrieve and store the "searchInput" value from the !searchForm" form so the customer accounts can be selected with the value matching the "searchInputResult" variable in the "customerAccounts" table in the "alsDb.db".
            searchInputResult = request.form['searchInput']

            #Check if the "selectBoxResult" select option value has been selected to search the "customerAccounts" table in the "alsDB.db" via the "customerFirstName" and will select the results with the "customerFirstName" table data as or like the "searchInputResult" variable.
            if selectBoxResult == 'Search First Name':
            
                #Select all customer accounts data that match or contain the "searchInputResult" variable data from the "customerAccounts" table in the "alsDB.db".
                sqlQ = "SELECT * FROM customerAccounts WHERE customerFirstName = ? OR customerFirstName LIKE ?"
                
                #Execute the "sqlQ" using the "searchInputResult" variable as the arguments to match fully or contain part of the "customerFirstName" field.
                cursor.execute(sqlQ, (searchInputResult, searchInputResult,))
                
                #Store the "sqlQ" query results in the "customerAccountDetails" variable to send to the "/templates/user/loggedin/createsendaudits.html" web-page for display using Jinja2.
                customerAccountDetails = cursor.fetchall()
                
                #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
                usersUsername = session['userUsername']

                #Render the "/templates/user/loggedin/createsendaudits.html" web-page sending the "customerAccountDetails" and the "usersUsername" variables for display using Jinja2.
                return render_template('user/loggedin/createsendaudits.html', _customerAccountDetails = customerAccountDetails, _userUsername = usersUsername)

            #Check if the "selectBoxResult" select option value has been selected to search the "customerAccounts" table in the "alsDB.db" via the "customerLastName" and will select the results with the "customerLastName" table data as or like the "searchInputResult" variable.
            elif selectBoxResult == 'Search Last Name':
                
                #Select all customer accounts data that match or contain the "searchInputResult" variable data from the "customerAccounts" table in the "alsDB.db".
                sqlQ = "SELECT * FROM customerAccounts WHERE customerLastName = ? OR customerLastName LIKE ?"

                #Execute the "sqlQ" using the "searchInputResult" variable as the arguments to match fully or contain part of the "customerLastName" field.
                cursor.execute(sqlQ, (searchInputResult, searchInputResult,))

                #Store the "sqlQ" query results in the "customerAccountDetails" variable to send to the "/templates/user/loggedin/createsendaudits.html" web-page for display using Jinja2.
                customerAccountDetails = cursor.fetchall()
                
                #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
                usersUsername = session['userUsername']

                #Render the "/templates/user/loggedin/createsendaudits.html" web-page sending the "customerAccountDetails" and the "usersUsername" variables for display using Jinja2.
                return render_template('user/loggedin/createsendaudits.html', _customerAccountDetails = customerAccountDetails, _userUsername = usersUsername)

            #Check if the "selectBoxResult" select option value has been selected to search the "customerAccounts" table in the "alsDB.db" via the "customerResidentialStatus" and will select the results with the "customerResidentialStatus" table data as or like the "searchInputResult" variable.
            elif selectBoxResult == 'Search Address':

                #Select all customer accounts data that match or contain the "searchInputResult" variable data from the "customerAccounts" table in the "alsDB.db".
                sqlQ = "SELECT * FROM customerAccounts WHERE customerResidentialStatus = ? OR customerResidentialStatus LIKE ?"

                #Execute the "sqlQ" using the "searchInputResult" variable as the arguments to match fully or contain part of the "customerResidentialStatus" field.
                cursor.execute(sqlQ, (searchInputResult, searchInputResult,))
                
                #Store the "sqlQ" query results in the "customerAccountDetails" variable to send to the "/templates/user/loggedin/createsendaudits.html" web-page for display using Jinja2.
                customerAccountDetails = cursor.fetchall()
                
                #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
                usersUsername = session['userUsername']

                #Render the "/templates/user/loggedin/createsendaudits.html" web-page sending the "customerAccountDetails" and the "usersUsername" variables for display using Jinja2.
                return render_template('user/loggedin/createsendaudits.html', _customerAccountDetails = customerAccountDetails, _userUsername = usersUsername)

            #Check if the "selectBoxResult" select option value has been selected to search the "customerAccounts" table in the "alsDB.db" via the "customerPhoneNumber" and will select the results with the "customerPhoneNumber" table data as or like the "searchInputResult" variable.
            elif selectBoxResult == 'Search Phone Number':
            
                #Select all customer accounts data that match or contain the "searchInputResult" variable data from the "customerAccounts" table in the "alsDB.db".
                sqlQ = "SELECT * FROM customerAccounts WHERE customerPhoneNumber = ? OR customerPhoneNumber LIKE ?"

                #Execute the "sqlQ" using the "searchInputResult" variable as the arguments to match fully or contain part of the "customerPhoneNumber" field.
                cursor.execute(sqlQ, (searchInputResult, searchInputResult,))

                #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
                usersUsername = session['userUsername']

                #Store the "sqlQ" query results in the "customerAccountDetails" variable to send to the "/templates/user/loggedin/createsendaudits.html" web-page for display using Jinja2.
                customerAccountDetails = cursor.fetchall()
                
                #Render the "/templates/user/loggedin/createsendaudits.html" web-page sending the "customerAccountDetails" and the "usersUsername" variables for display using Jinja2.
                return render_template('user/loggedin/createsendaudits.html', _customerAccountDetails = customerAccountDetails, _userUsername = usersUsername)

            #Check if the "selectBoxResult" select option value has been selected to search the "customerAccounts" table in the "alsDB.db" via the "customerEmailAddress" and will select the results with the "customerEmailAddress" table data as or like the "searchInputResult" variable.
            elif selectBoxResult == 'Search Email Address':
            
                #Select all customer accounts data that match or contain the "searchInputResult" variable data from the "customerAccounts" table in the "alsDB.db".
                sqlQ = "SELECT * FROM customerAccounts WHERE customerEmailAddress = ? OR customerEmailAddress LIKE ?"

                #Execute the "sqlQ" using the "searchInputResult" variable as the arguments to match fully or contain part of the "customerPhoneNumber" field.
                cursor.execute(sqlQ, (searchInputResult, searchInputResult,))

                #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
                usersUsername = session['userUsername']

                #Store the "sqlQ" query results in the "customerAccountDetails" variable to send to the "/templates/user/loggedin/createsendaudits.html" web-page for display using Jinja2.
                customerAccountDetails = cursor.fetchall()
                
                #Render the "/templates/user/loggedin/createsendaudits.html" web-page sending the "customerAccountDetails" and the "usersUsername" variables for display using Jinja2.
                return render_template('user/loggedin/createsendaudits.html', _customerAccountDetails = customerAccountDetails, _userUsername = usersUsername)

            #Check if the "selectBoxResult" select option value has been selected to search the "customerAccounts" table in the "alsDB.db" via the "customerFirstName" and will select the results with the "customerEmploymentStatus" table data as or like the "searchInputResult" variable.
            elif selectBoxResult == 'Search Employment Status':
            
                #Select all customer accounts data that match or contain the "searchInputResult" variable data from the "customerAccounts" table in the "alsDB.db".
                sqlQ = "SELECT * FROM customerAccounts WHERE customerEmploymentStatus = ? OR customerEmploymentStatus LIKE ?"
                
                #Execute the "sqlQ" using the "searchInputResult" variable as the arguments to match fully or contain part of the "customerEmploymentStatus" field.
                cursor.execute(sqlQ, (searchInputResult, searchInputResult,))

                #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
                usersUsername = session['userUsername']

                #Store the "sqlQ" query results in the "customerAccountDetails" variable to send to the "/templates/user/loggedin/createsendaudits.html" web-page for display using Jinja2.
                customerAccountDetails = cursor.fetchall()
                
                '''
                Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
                '''
            
                #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
                mydb = sqlite3.connect('alsDB.db')
                
                #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
                cursor = mydb.cursor()
                
                #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
                sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
                
                #Execute the "sqlQ" query.
                cursor.execute(sqlQ)

                #Access the current datetime. 
                logDate = datetime.now()
                
                #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
                userUsername = session['userUsername']
                
                #Provide a log message upon accessing the route with information of the specific action taken on the route.
                logMessage = "System user " + userUsername + " accessed on the /user/loggedin/creatsendaudits route."
                
                #Provide a category for the ability to search based on action of the log.
                logCategory = "/user/loggedin/creatsendaudits route accessed."
                
                #Provide which section of the web-app was accessed.
                logUser = userUsername
                
                #Provide the location where the log was entered.
                logLocation = "/user/loggedin/creatsendaudits"
                
                #Insert the log data into the "messageLogs" database.
                cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
                
                #Commit the log to the "alsDB.db" database.
                mydb.commit()
                
                #Render the "/templates/user/loggedin/createsendaudits.html" web-page sending the "customerAccountDetails" and the "usersUsername" variables for display using Jinja2.
                return render_template('user/loggedin/createsendaudits.html', _customerAccountDetails = customerAccountDetails, _userUsername = usersUsername)

        #Check if the "auditCustomer" form was submitted by the system user so the customer account details of the customer to send an audit is selected using the hidden input field data which contains the "customerAccountID" of the customer to find in the "customerAccounts" table in the "alsDB.db" database. The audit will the be provided with the audit details displayed to the system user to send to that customers account.
        if request.args.get('f') == 'auditCustomer':

            #Store the customer ID from the "auditCustomer" form "accountCustomerDetailsID" hidden input in the "customerAccountDetailsID" variable.
            customerAccountDetailsID = request.form['accountCustomerDetailsID']
            
            #Select the customer account details from the "customerAccounts" table in the "alsDB.db" that contained the "customerAccountDetailsID" from the "auditCustomer" form on the "/templates/user/loggedin/createsendaudits.html" web-page 
            sqlQ = "SELECT * FROM customerAccounts WHERE customerAccountID = ?"
            
            #Execute the "sqlQ" query using the "customerAccountDetailsID" variable as the value of the "customerAccountID" to select the customer account with that "customerAccountID".
            cursor.execute(sqlQ, (customerAccountDetailsID,))
            
            #Store the results of the "sqlQ" query in the "customerAccountDetails" variable to send to be displayed on the "/templates/user/loggedin/createsendaudits.html" web-page using Jinja2.
            customerAccountDetails = cursor.fetchall()

            #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
            usersUsername = session['userUsername']
            
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
            userUsername = session['userUsername']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "System user " + userUsername + " accessed on the /user/loggedin/creatsendaudits route."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/user/loggedin/creatsendaudits route accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = userUsername
            
            #Provide the location where the log was entered.
            logLocation = "/user/loggedin/creatsendaudits"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()
            
            #Render the "/templates/user/loggedin/createsendaudits.html" web-page sending the "customerAccountDetails" and the "usersUsername" variables for display using Jinja2.
            return render_template('user/loggedin/createsendaudits.html', _customerAccountDetails = customerAccountDetails, _userUsername = usersUsername)
        
        #If the "templates/user/loggedin/createsendaudits.html" page is accessed then all the customer accounts data from the "customerAccounts" table in the "alsDB.db" database will be displayed to the system user using Jinja2.
        else:

            #Select all the customer accounts data from the "customerAccounts" table in the "alsDB.db" database to display to the "/templates/user/loggedin/createsendaudits.html" web-page using Jinja2.
            sqlQ = "SELECT * FROM customerAccounts"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
            usersUsername = session['userUsername']

            #Store the results of the "sqlQ" query in the "customerAccountDetails" variable to send to be displayed on the "/templates/user/loggedin/createsendaudits.html" web-page using Jinja2.
            customerAccountDetails = cursor.fetchall()
            
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
            userUsername = session['userUsername']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "System user " + userUsername + " accessed on the /user/loggedin/creatsendaudits route."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/user/loggedin/creatsendaudits route accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = userUsername
            
            #Provide the location where the log was entered.
            logLocation = "/user/loggedin/creatsendaudits"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()
            
            #Render the "/templates/user/loggedin/createsendaudits.html" web-page sending the "customerAccountDetails" and the "usersUsername" variables for display using Jinja2.
            return render_template('user/loggedin/createsendaudits.html', _customerAccountDetails = customerAccountDetails, _userUsername = usersUsername)
            
    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
        
        #Render the "/user/login.html" web-page if the "session['userLoggedIn']" variable is not set to "True".
        return render_template('user/login.html')

'''
The "viewaudit()" function shows the details of the customer audit on the "/templates/user/loggedin/viewaudit.html" web-page and the system user can then send the audit to the customer.
'''
@app.route('/user/loggedin/viewaudit', methods=['GET','POST'])
def viewaudit():
    
    #Check if the user is logged in if the "session['userLoggedIn']" variable is asigned from the "/templates/user/loggedin/home" route.
    if session['userLoggedIn'] == True:

        #Check if the "auditCustomer" form from the "/templates/user/loggedin/createsendaudits.html" web-page was submitted to allow the system user to send an audit to the customer with the details that were selected on the "/templates/user/loggedin/createsendaudits.html" web-page.
        if request.args.get('f') == 'auditCustomer':

            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()

            #Create the "customerAccounts" table in the "alsDB.db" if non-existent.
            sqlQ = "CREATE TABLE IF NOT EXISTS customerAccounts(customerAccountID INT PRIMARY KEY, customerAccountCreatedDate VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), customerDateOfBirth VARCHAR(255), customerResidentialStatus VARCHAR(255), customerDateOfMoveIn VARCHAR(255), customerPhoneNumber VARCHAR(255), customerEmailAddress VARCHAR(255), customerEmploymentStatus VARCHAR(255), customerDateEmploymentCommenced VARCHAR(255), customerEmployerName VARCHAR(255), customerEmployerAddress VARCHAR(255), customerEmployerContactNumber VARCHAR(255), customerLengthOfTimeAsSelfEmployed VARCHAR(255), customerCompanyName VARCHAR(255), customerCompanyAddress VARCHAR(255), customerGovernmentBenefitsDescription VARCHAR(255), customerGrossMonthlyIncome VARCHAR(255), customerYearlyIncomeAfterTax VARCHAR(255), customerMotorCostsDescription VARCHAR(255), customerMotorCostsAmount VARCHAR(255), customerFoodExpensesDescription VARCHAR(255), customerFoodExpensesAmount VARCHAR(255), customerClothingExpensesDescription VARCHAR(255), customerClothingExpensesAmount VARCHAR(255), customerChildcareCostsDescription VARCHAR(255), customerChildcareCostsAmount VARCHAR(255), customerHousingCostsDescription VARCHAR(255), customerHousingCostsAmount VARCHAR(255), customerHomeRentalCostsDescription VARCHAR(255), customerHomeRentalCostsAmount VARCHAR(255), customerMortgageRepaymentsDescription VARCHAR(255), customerMortgageRepaymentsAmount VARCHAR(255), customerUtilityCostsDescription VARCHAR(255), customerUtilityCostsAmount VARCHAR(255), customerPhoneExpensesDescription VARCHAR(255), customerPhoneExpensesAmount VARCHAR(255), customerOtherExpensesDescription VARCHAR(255), customerOtherExpensesAmount VARCHAR(255), customerTotalExpensesAmount VARCHAR(255), customerAccountUsername VARCHAR(255), customerAccountPassword VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
            
            #Retrieve the "accountCustomerDetailsID" from the "auditCustomer" form and store in the "customerDetailsID" variable.
            customerDetailsID = request.form['accountCustomerDetailsID']
            
            #Select the customer account details with the "customerAccountID" in the "customerAccounts" table in the alsDB.db" to send to the "/templates/user/loggedin/viewaudit.html" web-page.
            sqlQ = "SELECT * FROM customerAccounts WHERE customerAccountID = ?"
            
            #Execute the "sqlQ" query using the "customerDetailsID" from the "/templates/user/loggedin/createsendaudits.html" web-page to find the customer account details to send to the "/templates/user/loggedin/viewaudit.html" web-page.
            cursor.execute(sqlQ, (customerDetailsID,))
            
            #Store the results of the "sqlQ" query in the "customerAccountDetails" variable to send to be displayed on the "/templates/user/loggedin/viewaudit.html" web-page using Jinja2.
            customerAccountDetails = cursor.fetchall()

            #Get and store the current date and time of the audit being created in the "currentDate" variable 
            currentDate = datetime.now().date()
            
            #Change the "currentDate" variable to String format.
            dateNow = str(currentDate)
            
            #Initialise the "index" variable to "0" to store as an index in the "customerAuditDictionary" dictionary variable to send to the ".templates/user/loggedin/viewaudit.html" web-page.
            index = 0
            
            #Initialise the "customerAuditDictionary" as an empty dict variable.
            customerAuditDictionary = {}
            
            #Loop through each of the "customerAccountDetails" variable values to store the values of the customers account details in the "customerAuditDictionary"
            for detail in customerAccountDetails:
                for info in detail:
                
                    #Create a "customerInfo" variable to store the current dictionary information in to update the "customerAuditDictionary" dictionary variable with.the key:value pair of each "index" incremented by one each loop and the "info" of the loop
                    customerInfo = {index:info}
                    
                    #Increment the "index" variable by one each loop.
                    index = index + 1
                    
                    #Update the "customerAuditDictionary" with the "customerInfo" variable data to send to the "/templates/user/loggedin/viewaudit.html" web-page.
                    customerAuditDictionary.update(customerInfo)
            
            #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
            usersUsername = session['userUsername']
            
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
            userUsername = session['userUsername']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "System user " + userUsername + " accessed on the /user/loggedin/createsendaudits route."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/user/loggedin/createsendaudits route accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = userUsername
            
            #Provide the location where the log was entered.
            logLocation = "/user/loggedin/createsendaudits"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()
            
            #Render the "/templates/user/loggedin/viewaudit.html" web-page sending the "customerAuditDictionary", the "dateNow" and the "usersUsername" variables for display using Jinja2.
            return render_template('user/loggedin/viewaudit.html', _customerAuditDictionary = customerAuditDictionary, _dateNow = dateNow, _userUsername = usersUsername)
    
    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
        
        #Render the "/user/login.html" web-page if the "session['userLoggedIn']" variable is not set to "True".
        return render_template('user/login.html')

'''
The "submitaudit()" function stores the customer audit in the "alsDB.db" database and renders the ".templates/user/loggedin/home.html" web-page to the system user.
'''
@app.route('/user/loggedin/submitaudit', methods=['GET','POST'])
def submitaudit():

    #Check if the user is logged in if the "session['userLoggedIn']" variable is assigned from the "/templates/user/loggedin/home" route.
    if session['userLoggedIn'] == True:

        #Check if the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" webpage has been submitted by the system user 
        if request.args.get('f') == 'submitAudit':
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()

            #Create the "customerAccounts" table in the "alsDB.db" if non-existent.
            sqlQ = "CREATE TABLE IF NOT EXISTS customerAccounts(customerAccountID INT PRIMARY KEY, customerAccountCreatedDate VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), customerDateOfBirth VARCHAR(255), customerResidentialStatus VARCHAR(255), customerDateOfMoveIn VARCHAR(255), customerPhoneNumber VARCHAR(255), customerEmailAddress VARCHAR(255), customerEmploymentStatus VARCHAR(255), customerDateEmploymentCommenced VARCHAR(255), customerEmployerName VARCHAR(255), customerEmployerAddress VARCHAR(255), customerEmployerContactNumber VARCHAR(255), customerLengthOfTimeAsSelfEmployed VARCHAR(255), customerCompanyName VARCHAR(255), customerCompanyAddress VARCHAR(255), customerGovernmentBenefitsDescription VARCHAR(255), customerGrossMonthlyIncome VARCHAR(255), customerYearlyIncomeAfterTax VARCHAR(255), customerMotorCostsDescription VARCHAR(255), customerMotorCostsAmount VARCHAR(255), customerFoodExpensesDescription VARCHAR(255), customerFoodExpensesAmount VARCHAR(255), customerClothingExpensesDescription VARCHAR(255), customerClothingExpensesAmount VARCHAR(255), customerChildcareCostsDescription VARCHAR(255), customerChildcareCostsAmount VARCHAR(255), customerHousingCostsDescription VARCHAR(255), customerHousingCostsAmount VARCHAR(255), customerHomeRentalCostsDescription VARCHAR(255), customerHomeRentalCostsAmount VARCHAR(255), customerMortgageRepaymentsDescription VARCHAR(255), customerMortgageRepaymentsAmount VARCHAR(255), customerUtilityCostsDescription VARCHAR(255), customerUtilityCostsAmount VARCHAR(255), customerPhoneExpensesDescription VARCHAR(255), customerPhoneExpensesAmount VARCHAR(255), customerOtherExpensesDescription VARCHAR(255), customerOtherExpensesAmount VARCHAR(255), customerTotalExpensesAmount VARCHAR(255), customerAccountUsername VARCHAR(255), customerAccountPassword VARCHAR(255))"

            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
            
            #Retrieve the "EmployedvSelfEmployed" hidden input value from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page.
            employedVsSelfEmployed = request.form['EmployedvSelfEmployed']
            
            #Get and store the current date and time of the sent audit to the customer in the "auditDateTime" variable.
            auditDateTime = datetime.now()
            
            #Create the "selfEmployedCustomerAudits" table in the "alsDB.db" to store the data of the customer audit from the "/templates/loggedin/viewaudit.html" web-page.
            sqlQ = "CREATE TABLE IF NOT EXISTS selfEmployedCustomerAudits(auditID INT PRIMARY KEY, auditDate VARCHAR(255), customerAccountID VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), grossMonthlyIncomeTaxRateInputLabel VARCHAR(255), lengthOfTimeAsSelfEmployed VARCHAR(255), companyName VARCHAR(255), companyAddress VARCHAR(255), grossMonthlyIncome VARCHAR(255), grossMonthlyIncomeTaxAmount VARCHAR(255), yearlyIncomeAfterTax VARCHAR(255), taxRate4PerCent VARCHAR(255), payByDate VARCHAR(255), paymentDetails VARCHAR(255), paidAudit VARCHAR(255))"

            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Create the "employedCustomerAudits" table in the "alsDB.db" to store the data of the customer audit from the "/templates/loggedin/viewaudit.html" web-page.
            sqlQ = "CREATE TABLE IF NOT EXISTS employedCustomerAudits(auditID INT PRIMARY KEY, auditDate VARCHAR(255), customerAccountID VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), grossMonthlyIncomeTaxRateInputLabel VARCHAR(255), dateEmploymentCommenced VARCHAR(255), employerName VARCHAR(255), employerAddress VARCHAR(255), employerContactNumber VARCHAR(255), grossMonthlyIncome VARCHAR(255), grossMonthlyIncomeTaxAmount VARCHAR(255), yearlyIncomeAfterTax VARCHAR(255), taxRate1PerCent VARCHAR(255), payByDate VARCHAR(255), paymentDetails VARCHAR(255), paidAudit VARCHAR(255))"
        
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
        
            #Check if the "employedVsSelfEmployed" variable has "Employed" as the value to collect the audit details if the customer is employed and store those collected details in the "employedCustomerAudits" table in the "alsDB.db" database.
            if employedVsSelfEmployed == 'Employed':
                
                #Store the "customerAccountID" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerAccountDetailsID" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerAccountDetailsID = request.form['customerAccountID']

                #Store the "customerFirstName" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page  in the "addCustomerFirstName" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerFirstName = request.form['customerFirstName']
                
                #Store the "customerLastName" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerLastName" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerLastName = request.form['customerLastName']
                
                #Store the "grossMonthlyIncomeTaxRateInputLabel" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerGrossMonthlyIncomeTaxRateInputLabel" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerGrossMonthlyIncomeTaxRateInputLabel = request.form['grossMonthlyIncomeTaxRateInput']    
                
                #Store the "dateOfEmployment" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerDateOfEmployment" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerDateOfEmployment = request.form['dateOfEmployment']
                
                #Store the "employerName" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerEmployerName" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerEmployerName = request.form['employerName']
                
                #Store the "employerAddress" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerEmployerAddress" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerEmployerAddress = request.form['employerAddress']

                #Store the "employerContact" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerEmployerContact" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerEmployerContact = request.form['employerContactNumber']

                #Store the "grossMonthlyIncomeTotal" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerGrossMonthlyIncome" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerGrossMonthlyIncome = request.form['grossMonthlyIncomeTotal']

                #Store the "grossMonthlyIncomeValue" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerGrossMonthlyIncomeValue" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerGrossMonthlyIncomeValue = request.form['grossMonthlyIncomeValue']

                #Store the "YearlyIncomeAfterTax" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerYearlyIncomeAfterTax" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerYearlyIncomeAfterTax = request.form['YearlyIncomeAfterTax']

                #Store the "taxRate1PerCent" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerTaxRate1PerCent" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerTaxRate1PerCent = request.form['taxRate1PerCent']

                #Store the "auditDate" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerAuditDate" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerAuditPayByDate = request.form['auditDate']

                #Store the "auditAddress" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerAuditAddress" in the "employedCustomerAudits" table in the "alsDB.db".
                addCustomerAuditAddress = request.form['auditAddress']
                
                #Set the "paid" variables value to "NO" to store in the "employedCustomerAudits" table in the "alsDB.db".
                paid = "NO"

                #Select the last entry of the "auditID" from the "employedCustomerAudits" table in the "alsDB.db".
                sqlQ = "SELECT auditID FROM employedCustomerAudits ORDER BY auditID DESC LIMIT 1"
                
                #Execute the "sqlQ" query.
                cursor.execute(sqlQ)
                
                #Initialise the "customerAuditID" to "0".
                customerAuditID = 0
                
                #Loop through the rfesults of the "sqlQ" query.
                for audit in cursor.fetchall():
                
                    #Store the last entered "auditID" in the "customerAuditID" variable.
                    customerAuditID = int(audit[0])

                #Check if there is a numerical "auditID" stored from the "for" loop and if there is then the "auditID" to be stored in the "employedCustomerAudits" table in the "alsDB.db" database will be incremented by one of the last entered "auditID" to create the next "auditID" for entry to the "employedCustomerAudits" table in the "addCustomerAuditID" variable.
                if customerAuditID > 0:
                    
                    #Increment the "customerAuditID" by one and store in the "addCustomerAuditID" variable.
                    addCustomerAuditID = customerAuditID + 1
                    
                #If the value of the "customerAuditID" is not greater than "0" then the first "auditID" to store is given the value"1".
                else:
                    
                    #Store the value "1" in the "addCustomerAuditID"to be stored in the "employedCustomerAudits" table in the "alsDB.db" database as the first entry in the "employedCustomerAudits" table.
                    addCustomerAuditID = 1

                #Create the "employedCustomerAudits" table in the "alsDB.db" to store the data of the customer audit from the "/templates/user/loggedin/viewaudit.html" web-page.
                sqlQ = "CREATE TABLE IF NOT EXISTS employedCustomerAudits(auditID INT PRIMARY KEY, auditDate VARCHAR(255), customerAccountID VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), grossMonthlyIncomeTaxRateInputLabel VARCHAR(255), dateEmploymentCommenced VARCHAR(255), employerName VARCHAR(255), employerAddress VARCHAR(255), employerContactNumber VARCHAR(255), grossMonthlyIncome VARCHAR(255), grossMonthlyIncomeTaxAmount VARCHAR(255), yearlyIncomeAfterTax VARCHAR(255), taxRate1PerCent VARCHAR(255), payByDate VARCHAR(255), paymentDetails VARCHAR(255), paidAudit VARCHAR(255))"

                #Execute the "sqlQ" query.
                cursor.execute(sqlQ)
                
                #Insert into the "employedCustomerAudits" table in the "alsDB.db" the values of the customer audit that has been submitted from the "submitAudit" form in the "/templates/user/loggedin/viewaudit.html" web-page.
                cursor.execute("INSERT INTO employedCustomerAudits(auditID, auditDate, customerAccountID, customerFirstName, customerLastName, grossMonthlyIncomeTaxRateInputLabel, dateEmploymentCommenced, employerName, employerAddress, employerContactNumber, grossMonthlyIncome, grossMonthlyIncomeTaxAmount, yearlyIncomeAfterTax, taxRate1PerCent, payByDate, paymentDetails, paidAudit) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(addCustomerAuditID, auditDateTime, addCustomerAccountDetailsID, addCustomerFirstName, addCustomerLastName, addCustomerGrossMonthlyIncomeTaxRateInputLabel, addCustomerDateOfEmployment, addCustomerEmployerName, addCustomerEmployerAddress, addCustomerEmployerContact, addCustomerGrossMonthlyIncome, addCustomerGrossMonthlyIncomeValue, addCustomerYearlyIncomeAfterTax, addCustomerTaxRate1PerCent, addCustomerAuditPayByDate, addCustomerAuditAddress, paid))
                
                #Commit the entry to the "alsDB.db" database.
                mydb.commit()
                
                #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
                usersUsername = session['userUsername']
                
                #Create a message to inform the system user on the "/templates/user/loggedin/home.html" web-page that the audit was sent to the customer.
                sentAuditMsg = "The audit was sucessfully sent to customer " + addCustomerAccountDetailsID 
                
                '''
                Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
                '''
            
                #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
                mydb = sqlite3.connect('alsDB.db')
                
                #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
                cursor = mydb.cursor()
                
                #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
                sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
                
                #Execute the "sqlQ" query.
                cursor.execute(sqlQ)

                #Access the current datetime. 
                logDate = datetime.now()
                
                #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
                userUsername = session['userUsername']
                
                #Provide a log message upon accessing the route with information of the specific action taken on the route.
                logMessage = "System user " + userUsername + " sent an audit to the customer with ID " + addCustomerAccountDetailsID + "."
                
                #Provide a category for the ability to search based on action of the log.
                logCategory = "/user/loggedin/submitaudit route accessed."
                
                #Provide which section of the web-app was accessed.
                logUser = userUsername
                
                #Provide the location where the log was entered.
                logLocation = "/user/loggedin/submitaudit"
                
                #Insert the log data into the "messageLogs" database.
                cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
                
                #Commit the log to the "alsDB.db" database.
                mydb.commit()

                #Render the "/templates/user/loggedin/home.html" web-page to the system user sending the "sentAuditMsg" and "usersUsername" variables to be displayed to the system user using Jinja2.
                return render_template('user/loggedin/home.html', _sentAuditMsg = sentAuditMsg, _userUsername = usersUsername)

            #Check if the "employedVsSelfEmployed" variable has "Employed" as the value to collect the audit details if the customer is employed and store those collected details in the "employedCustomerAudits" table in the "alsDB.db" database.
            if employedVsSelfEmployed == 'Self Employed':
                
                #Store the "customerAccountID" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerAccountDetailsID" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerAccountDetailsID = request.form['customerAccountID']
                
                #Store the "customerFirstName" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerFirstName" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerFirstName = request.form['customerFirstName']

                #Store the "customerLastName" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerLastName" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerLastName = request.form['customerLastName']
                
                #Store the "customerLastName" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerGrossMonthlyIncomeTaxRateInputLabel" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerGrossMonthlyIncomeTaxRateInputLabel = request.form['grossMonthlyIncomeTaxRateInput']    

                #Store the "customerLastName" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerLengthOfTimeAsSelfEmployed" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerLengthOfTimeAsSelfEmployed = request.form['lengthOfTimeAsSelfEmployed']
                
                #Store the "companyName" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCompanyName" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCompanyName = request.form['companyName']
                
                #Store the "companyAddress" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerCompanyAddress" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerCompanyAddress = request.form['companyAddress']
                
                #Store the "grossMonthlyIncomeTotal" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerGrossMonthlyIncome" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerGrossMonthlyIncome = request.form['grossMonthlyIncomeTotal']

                #Store the "grossMonthlyIncomeValue" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerGrossMonthlyIncomeValue" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerGrossMonthlyIncomeValue = request.form['grossMonthlyIncomeValue']
                
                #Store the "YearlyIncomeAfterTax" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerYearlyIncomeAfterTax" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerYearlyIncomeAfterTax = request.form['YearlyIncomeAfterTax']
                
                #Store the "taxRate4PerCent" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerTaxRate4PerCent" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerTaxRate4PerCent = request.form['taxRate4PerCent']
                
                #Store the "auditDate" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerAuditPayByDate" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerAuditPayByDate = request.form['auditDate']
                
                #Store the "auditDate" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerAuditAddress" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                addCustomerAuditAddress = request.form['auditAddress']
                
                #Store the "paid" from the "submitAudit" form on the "/templates/user/loggedin/viewaudit.html" web-page in the "addCustomerAuditAddress" in the "selfEmployedCustomerAudits" table in the "alsDB.db".
                paid = "NO"
                
                #Select the last entry of the "auditID" from the "employedCustomerAudits" table in the "alsDB.db".
                sqlQ = "SELECT auditID FROM selfEmployedCustomerAudits ORDER BY auditID DESC LIMIT 1"
                
                #Execute the "sqlQ" query.
                cursor.execute(sqlQ)
                
                #Initialise the "customerAuditID" to "0".
                customerAuditID = 0
                
                #Loop through the rfesults of the "sqlQ" query.
                for audit in cursor.fetchall():
                
                    #Store the last entered "auditID" in the "customerAuditID" variable.
                    customerAuditID = int(audit[0])

                #Check if there is a numerical "auditID" stored from the "for" loop and if there is then the "auditID" to be stored in the "employedCustomerAudits" table in the "alsDB.db" database will be incremented by one of the last entered "auditID" to create the next "auditID" for entry to the "employedCustomerAudits" table in the "addCustomerAuditID" variable.
                if customerAuditID > 0:
                    
                    #Increment the "customerAuditID" by one and store in the "addCustomerAuditID" variable.
                    addCustomerAuditID = customerAuditID + 1
                    
                #If the value of the "customerAuditID" is not greater than "0" then the first "auditID" to store is given the value"1".
                else:
                    
                    #Store the value "1" in the "addCustomerAuditID"to be stored in the "employedCustomerAudits" table in the "alsDB.db" database as the first entry in the "employedCustomerAudits" table.
                    addCustomerAuditID = 1
                
                #Create the "selfEmployedCustomerAudits" table in the "alsDB.db" to store the data of the customer audit from the "/templates/loggedin/viewaudit.html" web-page.
                sqlQ = "CREATE TABLE IF NOT EXISTS selfEmployedCustomerAudits(auditID INT PRIMARY KEY, auditDate VARCHAR(255), customerAccountID VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), grossMonthlyIncomeTaxRateInputLabel VARCHAR(255), lengthOfTimeAsSelfEmployed VARCHAR(255), companyName VARCHAR(255), companyAddress VARCHAR(255), grossMonthlyIncome VARCHAR(255), grossMonthlyIncomeTaxAmount VARCHAR(255), yearlyIncomeAfterTax VARCHAR(255), taxRate4PerCent VARCHAR(255), payByDate VARCHAR(255), paymentDetails VARCHAR(255), paidAudit VARCHAR(255))"

                #Execute the "sqlQ" query.
                cursor.execute(sqlQ)
                
                #Insert into the "selfEmployedCustomerAudits" table in the "alsDB.db" the values of the customer audit that has been submitted from the "submitAudit" form in the "/templates/user/loggedin/viewaudit.html" web-page.
                cursor.execute("INSERT INTO selfEmployedCustomerAudits(auditID, auditDate, customerAccountID, customerFirstName, customerLastName, grossMonthlyIncomeTaxRateInputLabel, lengthOfTimeAsSelfEmployed, companyName, companyAddress, grossMonthlyIncome, grossMonthlyIncomeTaxAmount, yearlyIncomeAfterTax, taxRate4PerCent, payByDate, paymentDetails, paidAudit) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(addCustomerAuditID, auditDateTime, addCustomerAccountDetailsID, addCustomerFirstName, addCustomerLastName, addCustomerGrossMonthlyIncomeTaxRateInputLabel, addCustomerLengthOfTimeAsSelfEmployed, addCompanyName, addCustomerCompanyAddress, addCustomerGrossMonthlyIncome, addCustomerGrossMonthlyIncomeValue, addCustomerYearlyIncomeAfterTax, addCustomerTaxRate4PerCent, addCustomerAuditPayByDate, addCustomerAuditAddress, paid))
                
                #Commit the entry to the "alsDB.db" database.
                mydb.commit()    

                #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
                usersUsername = session['userUsername']
                
                #Create a message to inform the system user on the "/templates/user/loggedin/home.html" web-page that the audit was sent to the customer.
                sentAuditMsg = "The audit was sucessfully sent to customer " + addCustomerAccountDetailsID 
                '''
                Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
                '''
            
                #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
                mydb = sqlite3.connect('alsDB.db')
                
                #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
                cursor = mydb.cursor()
                
                #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
                sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
                
                #Execute the "sqlQ" query.
                cursor.execute(sqlQ)

                #Access the current datetime. 
                logDate = datetime.now()
                
                #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
                userUsername = session['userUsername']
                
                #Provide a log message upon accessing the route with information of the specific action taken on the route.
                logMessage = "System user " + userUsername + " sent an audit to the customer with ID " + addCustomerAccountDetailsID + "."
                
                #Provide a category for the ability to search based on action of the log.
                logCategory = "/user/loggedin/submitaudit route accessed."
                
                #Provide which section of the web-app was accessed.
                logUser = userUsername
                
                #Provide the location where the log was entered.
                logLocation = "/user/loggedin/submitaudit"
                
                #Insert the log data into the "messageLogs" database.
                cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
                
                #Commit the log to the "alsDB.db" database.
                mydb.commit()

                #Render the "/templates/user/loggedin/home.html" web-page to the system user sending the "sentAuditMsg" and "usersUsername" variables to be displayed to the system user using Jinja2.
                return render_template('user/loggedin/home.html', _sentAuditMsg = sentAuditMsg, _userUsername = usersUsername)
    
    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
        
        #Render the "/user/login.html" web-page if the "session['userLoggedIn']" variable is not set to "True".
        return render_template('user/login.html')

'''
The "employedaudits()" function displays the "/templates/user/loggedin/employedaudits.html" web-page with the selected details of the employed customer audits to the system user so an employed audit can be selected and the full audit viewed on the "/templates/user/loggedin/viewemployedaudits.html" web-page. 
'''
@app.route('/user/loggedin/employedaudits', methods=['GET','POST'])
def employedaudits():

    #Check if the user is logged in if the "session['userLoggedIn']" variable is assigned from the "/templates/user/loggedin/home" route.
    if session['userLoggedIn'] == True:

        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        #Create the "employedCustomerAudits" table in the "alsDB.db" to store the data of the customer audit from the "/templates/loggedin/viewaudit.html" web-page.
        sqlQ = "CREATE TABLE IF NOT EXISTS employedCustomerAudits(auditID INT PRIMARY KEY, auditDate VARCHAR(255), customerAccountID VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), grossMonthlyIncomeTaxRateInputLabel VARCHAR(255), dateEmploymentCommenced VARCHAR(255), employerName VARCHAR(255), employerAddress VARCHAR(255), employerContactNumber VARCHAR(255), grossMonthlyIncome VARCHAR(255), grossMonthlyIncomeTaxAmount VARCHAR(255), yearlyIncomeAfterTax VARCHAR(255), taxRate1PerCent VARCHAR(255), payByDate VARCHAR(255), paymentDetails VARCHAR(255), paidAudit VARCHAR(255))"
    
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)
        
        #Retrive all the "customerAccountID", the "customerFirstName", the "customerLastName" and the "auditID" entries from the "employedCustomerAudits" table in the "alsDB.db".
        sqlQ = "SELECT auditID, customerFirstName, customerLastName, customerAccountID, paidAudit FROM employedCustomerAudits"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)
        
        #Store the results of the "sqlQ" query in the "employedAudits" variable to send to the "/templates/user/loggedin/employedaudits.html" web-page using Jinja2 to display the data to the system user.
        employedAudits = cursor.fetchall()

        #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
        usersUsername = session['userUsername']
        
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''
    
        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
        userUsername = session['userUsername']
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "System user " + userUsername + " accessed the /user/loggedin/employedaudits."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/user/loggedin/employedaudits route accessed."
        
        #Provide which section of the web-app was accessed.
        logUser = userUsername
        
        #Provide the location where the log was entered.
        logLocation = "/user/loggedin/employedaudits"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()

        #Render the "/templates/user/loggedin/employedaudits.html" web-page to the system user sending the "employedAudits" and "usersUsername" variables to be displayed to the system user using Jinja2.
        return render_template('user/loggedin/employedaudits.html', _employedAudits = employedAudits, _userUsername = usersUsername)

    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
        
        #Render the "/user/login.html" web-page if the "session['userLoggedIn']" variable is not set to "True".
        return render_template('user/login.html')

'''
The "viewemployedaudits()" function allows the system user to view the selected audit from the "/templates/user/loggedin/employedaudits.html" web-page.
'''
@app.route('/user/loggedin/viewemployedaudits', methods=['GET','POST'])
def viewemployedaudits():
    
    #Check if the user is logged in if the "session['userLoggedIn']" variable is assigned from the "/templates/user/loggedin/home" route.
    if session['userLoggedIn'] == True:
        
        #Check if the "submitEmployedAudits" form on the "/templates/user/loggedin/employedaudits.html" webpage has been submitted by the system user 
        if request.args.get('f') == 'employedAudits':

            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create the "employedCustomerAudits" table in the "alsDB.db" to store the data of the customer audit from the "/templates/loggedin/viewaudit.html" web-page.
            sqlQ = "CREATE TABLE IF NOT EXISTS employedCustomerAudits(auditID INT PRIMARY KEY, auditDate VARCHAR(255), customerAccountID VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), grossMonthlyIncomeTaxRateInputLabel VARCHAR(255), dateEmploymentCommenced VARCHAR(255), employerName VARCHAR(255), employerAddress VARCHAR(255), employerContactNumber VARCHAR(255), grossMonthlyIncome VARCHAR(255), grossMonthlyIncomeTaxAmount VARCHAR(255), yearlyIncomeAfterTax VARCHAR(255), taxRate1PerCent VARCHAR(255), payByDate VARCHAR(255), paymentDetails VARCHAR(255), paidAudit VARCHAR(255))"
        
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Store the "customerAuditID" from the "submitEmployedAudits" form in the "customerEmployedAuditID" variable.
            customerEmployedAuditID = request.form['customerAuditID']

            #Select the audit details from the "employedCustomerAudits" table in the "alsDB.db" which has the "auditID" of the selected customer from the "submitEmployedAudits" form on the "/templates/user/loggedin/employedaudits.html" web-page to display to the user on the ".templates/user/loggedin/viewemployedaudits.html" web-page.
            sqlQ = "SELECT * FROM employedCustomerAudits WHERE auditID = ?"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ, (customerEmployedAuditID,))
                        
            #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
            usersUsername = session['userUsername']

            #Store the results of the "sqlQ" query in the "employedAudits" variable to send to the "/templates/user/loggedin/viewemployedaudits.html" web-page using Jinja2 to display the data to the system user.
            employedCustomerAudit = cursor.fetchall()
        
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
            userUsername = session['userUsername']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "System user " + userUsername + " accessed the /user/loggedin/employedaudits route to view the audit with ID " + customerEmployedAuditID + "."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/user/loggedin/viewemployedaudits route accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = userUsername
            
            #Provide the location where the log was entered.
            logLocation = "/user/loggedin/viewemployedaudits"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()

            #Render the "/templates/user/loggedin/viewemployedaudits.html" sending the "employedCustomerAudit" and the "usersUsername" variables to be displayed using Jinja2.
            return render_template('user/loggedin/viewemployedaudits.html', _employedCustomerAudit = employedCustomerAudit, _userUsername = usersUsername)
            
        #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
        usersUsername = session['userUsername']
                        
        #Render the "/templates/user/loggedin/home.html" web-page if the "submitEmployedAudits" form has not been submitted.
        return render_template('user/loggedin/home.html', _userUsername = usersUsername)

    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
        
        #Render the "/user/login.html" web-page if the "session['userLoggedIn']" variable is not set to "True".
        return render_template('user/login.html')

'''
The "selfemployedaudits()" function displays the "/templates/user/loggedin/selfemployedaudits.html" web-page with the selected details of the self employed customer audits to the system user so an employed audit can be selected and the full audit viewed on the "/templates/user/loggedin/viewselfemployedaudits.html" web-page. 
'''
@app.route('/user/loggedin/selfemployedaudits', methods=['GET','POST'])
def selfempaudits():

    #Check if the user is logged in if the "session['userLoggedIn']" variable is assigned from the "/templates/user/loggedin/home" route.
    if session['userLoggedIn'] == True:

        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        #Create the "selfEmployedCustomerAudits" table in the "alsDB.db" to store the data of the customer audit from the "/templates/loggedin/viewaudit.html" web-page.
        sqlQ = "CREATE TABLE IF NOT EXISTS selfEmployedCustomerAudits(auditID INT PRIMARY KEY, auditDate VARCHAR(255), customerAccountID VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), grossMonthlyIncomeTaxRateInputLabel VARCHAR(255), lengthOfTimeAsSelfEmployed VARCHAR(255), companyName VARCHAR(255), companyAddress VARCHAR(255), grossMonthlyIncome VARCHAR(255), grossMonthlyIncomeTaxAmount VARCHAR(255), yearlyIncomeAfterTax VARCHAR(255), taxRate4PerCent VARCHAR(255), payByDate VARCHAR(255), paymentDetails VARCHAR(255), paidAudit VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)
        
        #Retrive all the "customerAccountID", the "customerFirstName", the "customerLastName" and the "auditID" entries from the "selfEmployedCustomerAudits" table in the "alsDB.db".
        sqlQ = "SELECT auditID, customerFirstName, customerLastName, customerAccountID, paidAudit FROM selfEmployedCustomerAudits"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)
        
        #Store the results of the "sqlQ" query in the "selfEmployedAudits" variable to send to be displayed in the "/templates/user/loggedin/viewselfemployedaudits.html" web-page.
        selfEmployedAudits = cursor.fetchall()
        
        #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
        usersUsername = session['userUsername']
        
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''
    
        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
        userUsername = session['userUsername']
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "System user " + userUsername + " accessed the /user/loggedin/selfemployedaudits route."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/user/loggedin/selfemployedaudits route accessed."
        
        #Provide which section of the web-app was accessed.
        logUser = userUsername
        
        #Provide the location where the log was entered.
        logLocation = "/user/loggedin/selfemployedaudits"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()

        #Render the "/templates/user/loggedin/selfemployedaudits.html" sending the "selfEmployedAudits" and the "usersUsername" variables to be displayed using Jinja2.
        return render_template('user/loggedin/selfemployedaudits.html', _selfEmployedAudits = selfEmployedAudits, _userUsername = usersUsername)
        
    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
        
        #Render the "/user/login.html" web-page if the "session['userLoggedIn']" variable is not set to "True".
        return render_template('user/login.html')

'''
The "viewselfemployedaudits()" function allows the system user to view the selected audit from the "/templates/user/loggedin/selfemployedaudits.html" web-page.
'''
@app.route('/user/loggedin/viewselfemployedaudits', methods=['GET','POST'])
def viewselfemployedaudits():

    #Check if the user is logged in if the "session['userLoggedIn']" variable is assigned from the "/templates/user/loggedin/home" route.
    if session['userLoggedIn'] == True:

        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()

        #Check if the "selfEmployedAudits" form on the "
        if request.args.get('f') == 'selfEmployedAudits':
    
            #Create the "selfEmployedCustomerAudits" table in the "alsDB.db" to store the data of the customer audit from the "/templates/loggedin/viewaudit.html" web-page.
            sqlQ = "CREATE TABLE IF NOT EXISTS selfEmployedCustomerAudits(auditID INT PRIMARY KEY, auditDate VARCHAR(255), customerAccountID VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), grossMonthlyIncomeTaxRateInputLabel VARCHAR(255), lengthOfTimeAsSelfEmployed VARCHAR(255), companyName VARCHAR(255), companyAddress VARCHAR(255), grossMonthlyIncome VARCHAR(255), grossMonthlyIncomeTaxAmount VARCHAR(255), yearlyIncomeAfterTax VARCHAR(255), taxRate4PerCent VARCHAR(255), payByDate VARCHAR(255), paymentDetails VARCHAR(255), paidAudit VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)
            
            #Get the "auditID" of the customer audit to be displayed to the system user from the "selfEmployedAudits" form on the "/templates/user/loggedin/viewselfemployedaudits,html" web-page.
            customerAuditID = request.form['customerAuditID']
            
            #Retrieve the self-employed customer audit from the "selfEmployedCustomerAudits" table in the "alsDB.db" database.
            sqlQ = "SELECT * FROM selfEmployedCustomerAudits WHERE auditID = ?"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ, (customerAuditID,))
            
            #Store the "sqlQ" query results in the "selfEmployedAudits" variable.
            selfEmployedAudit = cursor.fetchall()
            
            #Store the users username from the "session['userUsername']" variable to the "usersUsername" variable.
            usersUsername = session['userUsername']
        
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
            userUsername = session['userUsername']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "System user " + userUsername + " accessed the /user/loggedin/viewselfemployedaudits route to view the audit with ID " + customerAuditID + "."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/user/loggedin/viewselfemployedaudits route accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = userUsername
            
            #Provide the location where the log was entered.
            logLocation = "/user/loggedin/viewselfemployedaudits"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()

            #Render the "/templates/user/loggedin/viewselfemployedaudits.html" sending the "selfEmployedAudit" and the "usersUsername" variables to be displayed using Jinja2.
            return render_template('user/loggedin/viewselfemployedaudits.html', _selfEmployedAudit = selfEmployedAudit, _userUsername = usersUsername)
        
    #If the "session['userLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/user/login.html" web-page.
    elif session['userLoggedIn'] != True:
        
        #Render the "/templates/user/login.html" web-page if the "session['userLoggedIn']" variable is not set to "True".
        return render_template('user/login.html')

'''
The "customerlogin()" function provides access to the "templates/customer/customerlogin.html" web-page which contains a form for the customer to enter the credentials provided by the system user when the system user has created a customer account.
'''
@app.route('/customer/', methods=['GET','POST'])
@app.route('/customer/login', methods=['GET','POST'])
def customerlogin():

    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
    cursor = mydb.cursor()

    #End the "session['customerUsername']" variable and set to none.
    session.pop('customerUsername', None)

    #End the "session['customerLoggedIn']" variable and set to none.
    session.pop('customerLoggedIn', None)
    
    #End the "session['customerID']" variable and set to none.
    session.pop('customerID', None)
    
    #Create the "employedCustomerAudits" table in the "alsDB.db" to store the data of the customer audit from the "/templates/loggedin/viewaudit.html" web-page.
    sqlQ = "CREATE TABLE IF NOT EXISTS employedCustomerAudits(auditID INT PRIMARY KEY, auditDate VARCHAR(255), customerAccountID VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), grossMonthlyIncomeTaxRateInputLabel VARCHAR(255), dateEmploymentCommenced VARCHAR(255), employerName VARCHAR(255), employerAddress VARCHAR(255), employerContactNumber VARCHAR(255), grossMonthlyIncome VARCHAR(255), grossMonthlyIncomeTaxAmount VARCHAR(255), yearlyIncomeAfterTax VARCHAR(255), taxRate1PerCent VARCHAR(255), payByDate VARCHAR(255), paymentDetails VARCHAR(255), paidAudit VARCHAR(255))"

    #Execute the "sqlQ" query.
    cursor.execute(sqlQ)
    
    #Create the "selfEmployedCustomerAudits" table in the "alsDB.db" to store the data of the customer audit from the "/templates/loggedin/viewaudit.html" web-page.
    sqlQ = "CREATE TABLE IF NOT EXISTS selfEmployedCustomerAudits(auditID INT PRIMARY KEY, auditDate VARCHAR(255), customerAccountID VARCHAR(255), customerFirstName VARCHAR(255), customerLastName VARCHAR(255), grossMonthlyIncomeTaxRateInputLabel VARCHAR(255), lengthOfTimeAsSelfEmployed VARCHAR(255), companyName VARCHAR(255), companyAddress VARCHAR(255), grossMonthlyIncome VARCHAR(255), grossMonthlyIncomeTaxAmount VARCHAR(255), yearlyIncomeAfterTax VARCHAR(255), taxRate4PerCent VARCHAR(255), payByDate VARCHAR(255), paymentDetails VARCHAR(255), paidAudit VARCHAR(255))"

    #Execute the "sqlQ" query.
    cursor.execute(sqlQ)
    
    '''
    Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
    '''
    
    #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
    sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
    
    #Execute the "sqlQ" query.
    cursor.execute(sqlQ)

    #Access the current datetime. 
    logDate = datetime.now()
    
    #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
    customerUsername = "User Unknown - Not Logged In"
    
    #Provide a log message upon accessing the route with information of the specific action taken on the route.
    logMessage = "The customer/login route accessed."
    
    #Provide a category for the ability to search based on action of the log.
    logCategory = "/customer/login route accessed."
    
    #Provide which section of the web-app was accessed.
    logUser = "Unknown User - Not Logged In"
    
    #Provide the location where the log was entered.
    logLocation = "/customer/login"
    
    #Insert the log data into the "messageLogs" database.
    cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
    
    #Commit the log to the "alsDB.db" database.
    mydb.commit()

    #Render the "/templates/customer/customerlogin.html" web-page when the user accesses the "/customer/" or the "/customer/login" route.
    return render_template('customer/customerlogin.html')

'''
The "customerhome()" function checks if the correct credentials have been entered by the user on the "/templates/customer/customerlogin.html" web-page and allows access to the "/templates/customer/loggedin/customerhome.html" or will return the user to the "templates/customer/customerlogin.html" if the wrong customer credentials have be enterred by the user.The "customerhome()" function will also be called when the customer has paid an audit on the "/templates/customer/loggedin/viewpayemployedaudits.html" and the "/templates/customer/loggedin/viewpayselfemployedaudits.html" web-page's. If the customer is not logged in and the "session['customerLoggedIn']" variable is not set to "True" then the "/tmeplates/customer/customerlogin.html" web-page will be rendered.
'''
@app.route('/customer/loggedin/customerhome', methods=['GET','POST'])
def customerhome():
        
    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
    cursor = mydb.cursor()

    #Check if the "customerLogin" form has been submitted so the customer can be logged in and allowed access to the "/templates/customer/loggedin/home.html" web-page.
    if request.args.get('f') == 'customerLogin':
        
        #Retrieve the "customerUsername" from the "customerLogin" form on the "/templates/customer/customerlogin.html" web-page.
        customerUsername = request.form['customerUsername']

        #Retrieve the "customerPassword" from the "customerLogin" form on the "/templates/customer/customerlogin.html" web-page.
        customerPassword = request.form['customerPassword']

        #Create a table "customerAccountLogin" if non-existent to add the customer login credentials for the ability to enter credentials on the "/customer/login" route of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS customerAccountLogin(customerLoginID INT PRIMARY KEY, customerUsername VARCHAR(255), customerPassword VARCHAR(255), customerID VARCHAR(255))"
        
        #Execute the "sqlQ query.
        cursor.execute(sqlQ)
        
        #Select the customers details from the "customerAccountLogin" table to check if the correct customer account credentials have been entered to allow the customer to access the "/templates/customer/customerhome.html" web-page.
        sqlQ = "SELECT customerUsername, customerPassword, customerID FROM customerAccountLogin WHERE customerUsername = ? AND customerPassword = ?"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ, (customerUsername, customerPassword,))
        
        #Initialise the "customerID" variable to 0.
        customerID = 0
        
        #Count the number of rows within the "sqlQ" query.
        rows = len(cursor.fetchall())
        
        #Select the "customerID" from the "customerAccountLogin" table in the "alsDB.db" database.
        sqlQ = "SELECT customerID FROM customerAccountLogin WHERE customerUsername = ? AND customerPassword = ?"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ, (customerUsername, customerPassword,))
        
        #Loop through the "sqlQ" query to get the customers ID.
        for each in cursor.fetchall():
        
            #Store the loggedin customers ID in the "customerID" variable.
            customerID = each[0]

        #If there is no credentials found in the "sqlQ" query, then provide a "loginFailMsg" to the user and return to the "customer/customerlogin.html" web-page.
        if rows > 0:
                    
            #Create a session variable "session['customerID'] with the "customerID" variable value.
            session['customerID'] = customerID
            
            #Create a session variable "session['customerUsername'] with the "customerUsername" variable value.
            session['customerUsername'] = customerUsername
            
            #Create a session variable "session['customerLoggedIn'] set to "True".
            session['customerLoggedIn'] = True
    
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "customerID" variable as the "session['customerID']"'s variable value.
            customerID = session['customerID']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "The customer with ID " + str(customerID) + " logged in and accessed /customer/loggedin/customerhome route."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/customer/loggedin/customerhome route was accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = customerUsername
            
            #Provide the location where the log was entered.
            logLocation = "/customer/loggedin/customerhome"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()

            #Render the "/templates/customer/loggedin/customerhome.html".
            return render_template('customer/loggedin/customerhome.html', _customerUsername = customerUsername)
        
        #If the "customerUsername" and the "customerPassword" are not found in the "sqlQ" query then the "/templates/customer/customerlogin.html" web-page will be rendered with the "wrongCredentialsMsg" displayed to the customer.
        elif rows == 0:
        
            #Create a "wrongCredentialsMsg" variable to inform the customer that the wrong credentials had been entered.
            wrongCredentialsMsg = "You have entered the wrong credentials! Please try again."
            
            #Render the "customer/customerlogin.html" with the "wrongCredentialsMsg" variable sent to be displayed to the customer using Jinja2.
            return render_template('customer/customerlogin.html', _wrongCredentialsMsg = wrongCredentialsMsg)

    #Check if the user is logged in if the "session['customerLoggedIn']" variable is assigned from the "/templates/customer/loggedin/customerhome" route.
    if session['customerLoggedIn'] == True:
        
        #Store the "session['customerUsername']" in the "customerUsername" variable.
        customerUsername = session['customerUsername']

        #Check if the "viewPayEmployedAuditForm" form has been submitted to update the "employedCustomerAudits" table in the "alsDB.db" database for the "paid" table data changed to "YES" when the "payAudit" button has been pressed by the customer on the "viewPayEmployedAuditForm" form on the "/templates/customer/loggedin/viewpayemployedaudits.html" web-page.
        if request.args.get('f') == 'viewPayEmployedAuditForm':
        
            #Get the "auditID" from the "viewPayEmployedAuditForm" form on the "/templates/customer/loggedin/viewpayemployedaudits.html" web-page.
            auditID = request.form['auditID']
            
            #Initialise the "paid" variable to "YES" to update the "employedCustomerAudits" table in the "alsDB.db" database.
            paid = "YES"
            
            #Update the "employedCustomerAudits" table in the "alsDB.db" with the "paidAudit" value changed to the value of the "paid" variable.
            cursor.execute("UPDATE employedCustomerAudits SET paidAudit = ? WHERE auditID = ?", (paid, auditID,))
            
            #Commit the changes to the "alsDB.db" database.
            mydb.commit()
            
            #Create the "paidAuditMsg" variable to send and display to the "/templates/customer/loggedin/customerhome.html" web-page. 
            paidAuditMsg = "The audit has been paid. Thank you!"

            #Store the "session['customerUsername']" in the "customerUsername" variable.
            customerUsername = session['customerUsername']
    
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
            customerID = session['customerID']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "The customer with ID " + str(customerID) + " accessed the /customer/loggedin/customerhome route and paid the employed audit with ID " + auditID + "."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/customer/loggedin/customerhome route was accessed and an employed audit was paid."
            
            #Provide which section of the web-app was accessed.
            logUser = customerUsername
            
            #Provide the location where the log was entered.
            logLocation = "/customer/loggedin/customerhome"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()

            #Render the "/templates/customer/loggedin/customerhome.html" web-page.
            return render_template('customer/loggedin/customerhome.html', _customerUsername = customerUsername, _paidAuditMsg = paidAuditMsg)
            
        #Check if the "viewPaySelfEmployedAuditForm" form has been submitted to update the "selfEmployedCustomerAudits" table in the "alsDB.db" database for the "paid" table data changed to "YES" when the "payAudit" button has been pressed by the customer on the "viewPaySelfEmployedAuditForm" form on the "/templates/customer/loggedin/viewpayselfemployedaudits.html" web-page.
        if request.args.get('f') == 'viewPaySelfEmployedAuditForm':
            
            #Get the "auditID" from the "viewPaySelfEmployedAuditForm" form on the "/templates/customer/loggedin/viewpayselfemployedaudits.html" web-page.
            auditID = request.form['auditID']
            
            #Initialise the "paid" variable to "YES" to update the "selfEmployedCustomerAudits" table in the "alsDB.db" database.
            paid = "YES"
            
            #Update the "selfEmployedCustomerAudits" table in the "alsDB.db" with the "paidAudit" value changed to the value of the "paid" variable.
            cursor.execute("UPDATE selfEmployedCustomerAudits SET paidAudit = ? WHERE auditID = ?", (paid, auditID,))
            
            #Commit the changes to the "alsDB.db" database.
            mydb.commit()
            
            #Create the "paidAuditMsg" variable to send and display to the "/templates/customer/loggedin/customerhome.html" web-page. 
            paidAuditMsg = "The audit has been paid. Thank you!"

            #Store the "session['customerUsername']" in the "customerUsername" variable.
            customerUsername = session['customerUsername']
    
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "customerID" variable as the "session['customerID']"'s variable value.
            customerID = session['customerID']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "The customer with ID " + customerID + " accessed the /customer/loggedin/customerhome route and paid the self employed audit with ID " + auditID + "."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/customer/loggedin/customerhome route was accessed and an employed audit was paid."
            
            #Provide which section of the web-app was accessed.
            logUser = customerUsername
            
            #Provide the location where the log was entered.
            logLocation = "/customer/loggedin/customerhome"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()

            #Render the "/templates/customer/loggedin/customerhome.html" web-page sending the "customerUsername" and the "paidAuditMsg" variable to be displayed using Jinja2.
            return render_template('customer/loggedin/customerhome.html', _customerUsername = customerUsername, _paidAuditMsg = paidAuditMsg)
            
        #Render the "/templates/customer/loggedin/customerhome.html" web-page sending the "customerUsername" variable to be displayed using Jinja2.
        return render_template('customer/loggedin/customerhome.html', _customerUsername = customerUsername)

    #If the "session['customerLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/customer/customerlogin.html" web-page.
    elif session['customerLoggedIn'] != True:
        
        #Render the "/templates/user/customerlogin.html" web-page if the "session['customerLoggedIn']" variable is not set to "True".
        return render_template('customer/customerlogin.html')

'''
The "viewpayaudit()" displays the loggedin customers employed and self employed audits to the "/templates/customer/loggedin/viewpayaudits.html" web-page. If the user is not logged in as a customer then the "/templates/customer/customerlogin.html" web-page will be rendered.
'''
@app.route('/customer/loggedin/viewpayaudit', methods=['GET','POST'])
def viewpayaudit():
    
    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
    cursor = mydb.cursor()

    #Check if the user is logged in if the "session['customerLoggedIn']" variable is assigned from the "/templates/customer/loggedin/customerhome" route.
    if session['customerLoggedIn'] == True:
        
        #Store the "session['customerID']" in the "customerID" variable.
        customerID = session['customerID']

        #Store the "session['customerUsername']" in the "customerUsername" variable.
        customerUsername = session['customerUsername']
        
        #Initialise the "selfEmployedAudits" variable to an empty string.
        selfEmployedAudits = ""
        
        #Initialise the "employedAudits" variable to an empty string.
        employedAudits = ""

        #Select the customer audits from the "selfEmployedCustomerAudits" table in the "alsDB.db" database.
        sqlQ = "SELECT * FROM employedCustomerAudits WHERE customerAccountID = ?"

        #Execute the "sqlQ query.
        cursor.execute(sqlQ, (customerID,))
                        
        #Store the "sqlQ" results in the "employedAudits" variable.
        employedAudits = cursor.fetchall()
        
        #Select the customer audits from the "selfEmployedCustomerAudits" table in the "alsDB.db" database.
        sqlQ = "SELECT * FROM selfEmployedCustomerAudits WHERE customerAccountID = ?"

        #Execute the "sqlQ query.
        cursor.execute(sqlQ, (customerID,))
        
        #Store the "sqlQ" results in the "selfEmployedAudits" variable.
        selfEmployedAudits = cursor.fetchall()
        
        '''
        Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
        '''
    
        #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
        mydb = sqlite3.connect('alsDB.db')
        
        #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
        cursor = mydb.cursor()
        
        #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
        sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
        
        #Execute the "sqlQ" query.
        cursor.execute(sqlQ)

        #Access the current datetime. 
        logDate = datetime.now()
        
        #Initialise the "userUsername" variable as the "session['userUsername']"'s variable value.
        customerUsername = session['customerUsername']
        
        #Provide a log message upon accessing the route with information of the specific action taken on the route.
        logMessage = "The customer with ID " + str(customerID) + " accessed the /customer/loggedin/viewpayaudit route."
        
        #Provide a category for the ability to search based on action of the log.
        logCategory = "/customer/loggedin/viewpayaudit route was accessed."
        
        #Provide which section of the web-app was accessed.
        logUser = customerUsername
        
        #Provide the location where the log was entered.
        logLocation = "/customer/loggedin/viewpayaudit"
        
        #Insert the log data into the "messageLogs" database.
        cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
        
        #Commit the log to the "alsDB.db" database.
        mydb.commit()
        
        #Render the "/templates/customer/loggedin/viewpayaudit.html" sending the "selfEmployedAudits" and the "usersUsername" variables to be displayed using Jinja2.
        return render_template('customer/loggedin/viewpayaudit.html', _selfEmployedAudits = selfEmployedAudits, _employedAudits = employedAudits, _customerUsername = customerUsername)
    
    #If the "session['customerLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/customer/customerlogin.html" web-page.
    elif session['customerLoggedIn'] != True:
        
        #Render the "/templates/user/customerlogin.html" web-page if the "session['customerLoggedIn']" variable is not set to "True".
        return render_template('customer/customerlogin.html')

'''
The "viewpayselfemployedaudit()" function uses the "auditID" from the "/templates/customer/loggedin/viewpayaudit.html" web-page to select the selcted audit details and displays the audit to the customer. The customer can then choose to click the button to pay the audit and be returned to the "/templates/customer/loggedin/customerhome.html"web-page. If the user is not logged in then the /templates/customer/customerlogin.html" web-page will be rendered.
'''
@app.route('/customer/loggedin/viewpayselfemployedaudits', methods=['GET','POST'])
def viewpayselfemployedaudit():   
    
    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
    cursor = mydb.cursor()

    #Check if the user is logged in if the "session['customerLoggedIn']" variable is assigned from the "/templates/customer/loggedin/customerhome" route.
    if session['customerLoggedIn'] == True:
        
        #Store the "session['customerID']" in the "customerID" variable.
        customerID = session['customerID']

        #Store the "session['customerUsername']" in the "customerUsername" variable.
        customerUsername = session['customerUsername']
        
        #Check if the "viewPaySelfEmployedAuditForm" was submitted by the customer on the "/templates/customer/loggedin/viewpayaudit.html" web-page to select the customers audit and send those details to the "/templates/customer/loggedin/viewpayselfemployedaudits.html" so the customer can pay the audit.
        if request.args.get('f') == 'viewPaySelfEmployedAuditForm':
        
            #Get the "auditID" from the "/templates/customer/loggedin/viewpayaudit.html" web-page and store in the "customerAuditID" variable.
            customerAuditID = request.form['auditID']
            
            #Select the customer audits from the "selfEmployedCustomerAudits" table in the "alsDB.db" database.
            sqlQ = "SELECT * FROM selfEmployedCustomerAudits WHERE auditID = ?"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ, (customerAuditID,))
            
            #Store the "sqlQ" results in the "selfEmployedAudits" variable to send to the "/templates/customer/loggedin/viewpayselfemployedaudits.html" web-page to display using Jinja2.
            selfEmployedAudits = cursor.fetchall()
        
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "The customer with ID " + str(customerID) + " accessed the /customer/loggedin/viewpayselfemployedaudits route to pay the self employed audit with ID " + customerAuditID + "."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/customer/loggedin/viewpayselfemployedaudits route was accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = customerUsername
            
            #Provide the location where the log was entered.
            logLocation = "/customer/loggedin/viewpayselfemployedaudits"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()
        
            #Render the "/templates/customer/loggedin/viewpayselfemployedaudits.html" web-page to the customer sending the "selfEmployedAudits" and the "customerUsername" variables to be displayed using Jinja2.
            return render_template('customer/loggedin/viewpayselfemployedaudits.html', _selfEmployedAudits = selfEmployedAudits, _customerUsername = customerUsername)
        
        #Render the "/templates/customer/loggedin/customerhome.html" web-page to the customer sending the "customerUsername" variable to be displayed usig Jinja2.
        return render_template('customer/loggedin/customerhome.html', _customerUsername = customerUsername)
        
    #If the "session['customerLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/customer/customerlogin.html" web-page.
    elif session['customerLoggedIn'] != True:
        
        #Render the "/templates/user/customerlogin.html" web-page if the "session['customerLoggedIn']" variable is not set to "True".
        return render_template('customer/customerlogin.html')

'''
The "viewpayemployedaudit()" function uses the "auditID" from the "/templates/customer/loggedin/viewpayaudit.html" web-page to select the selcted audit details and displays the audit to the customer. The customer can then choose to click the button to pay the audit and be returned to the "/templates/customer/loggedin/customerhome.html"web-page. If the user is not logged in then the /templates/customer/customerlogin.html" web-page will be rendered.
'''
@app.route('/customer/loggedin/viewpayemployedaudits', methods=['GET','POST'])
def viewpayemployedaudit():   
    
    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
    cursor = mydb.cursor()
    
    #Check if the user is logged in if the "session['customerLoggedIn']" variable is assigned from the "/templates/customer/loggedin/customerhome" route.
    if session['customerLoggedIn'] == True:
        
        #Store the "session['customerID']" in the "customerID" variable.
        customerID = session['customerID']
        
        #Store the "session['customerUsername']" in the "customerUsername" variable.
        customerUsername = session['customerUsername']
        
        #Check if the "viewPayEmployedAuditForm" was submitted by the customer on the "/templates/customer/loggedin/viewpayaudit.html" web-page to select the customers audit and send those details to the "/templates/customer/loggedin/viewpayemployedaudits.html" so the customer can pay the audit.
        if request.args.get('f') == 'viewPayEmployedAuditForm':
        
            #Get the "auditID" from the "/templates/customer/loggedin/viewpayaudit.html" web-page and store in the "customerAuditID" variable.
            customerAuditID = request.form['auditID']
            
            #Select the customer audits from the "employedCustomerAudits" table in the "alsDB.db" database.
            sqlQ = "SELECT * FROM employedCustomerAudits WHERE auditID = ?"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ, (customerAuditID,))
            
            #Store the "sqlQ" results in the "employedAudits" variable to send to the "/templates/customer/loggedin/viewpayemployedaudits.html" web-page to display using Jinja2.
            employedAudits = cursor.fetchall()
        
            '''
            Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
            '''
        
            #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
            mydb = sqlite3.connect('alsDB.db')
            
            #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
            cursor = mydb.cursor()
            
            #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
            sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
            
            #Execute the "sqlQ" query.
            cursor.execute(sqlQ)

            #Access the current datetime. 
            logDate = datetime.now()
            
            #Initialise the "customerUsername" variable as the "session['customerUsername']"'s variable value.
            customerUsername = session['customerUsername']
            
            #Provide a log message upon accessing the route with information of the specific action taken on the route.
            logMessage = "The customer with ID " + str(customerID) + " accessed the /customer/loggedin/viewpayemployedaudits route to pay the employed audit with ID " + customerAuditID + "."
            
            #Provide a category for the ability to search based on action of the log.
            logCategory = "/user/loggedin/viewpayemployedaudits route was accessed."
            
            #Provide which section of the web-app was accessed.
            logUser = customerUsername
            
            #Provide the location where the log was entered.
            logLocation = "/customer/loggedin/viewpayemployedaudits"
            
            #Insert the log data into the "messageLogs" database.
            cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
            
            #Commit the log to the "alsDB.db" database.
            mydb.commit()
        
            #Render the "/templates/customer/loggedin/viewpayemployedaudits.html" web-page to the customer sending the "employedAudits" and the "customerUsername" variables to be displayed using Jinja2.
            return render_template('customer/loggedin/viewpayemployedaudits.html', _employedAudits = employedAudits, _customerUsername = customerUsername)
            
        #Render the "/templates/customer/loggedin/customerhome.html" web-page to the customer sending the "customerUsername" variable to be displayed usig Jinja2.
        return render_template('customer/loggedin/customerhome.html', _customerUsername = customerUsername)
        
    #If the "session['customerLoggedIn']" variable is not set to "True" then the user will be directed to the "/templates/customer/customerlogin.html" web-page.
    elif session['customerLoggedIn'] != True:
        
        #Render the "/templates/user/customerlogin.html" web-page if the "session['customerLoggedIn']" variable is not set to "True".
        return render_template('customer/customerlogin.html')

'''
Pop the customer session variables when the "/customer/logout" route is accessed to log the user out of the customer part of the web-app system.
'''
@app.route('/customer/logout', methods=['GET','POST'])
def customerlogout():

    '''
    Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
    '''

    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
    cursor = mydb.cursor()
    
    #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
    sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
    
    #Execute the "sqlQ" query.
    cursor.execute(sqlQ)

    #Access the current datetime. 
    logDate = datetime.now()
    
    #Initialise the "customerID" variable as the "session['customerID']"'s variable value.
    customerID = session['customerID']

    #Initialise the "customerID" variable as the "session['customerID']"'s variable value.
    customerUsername = session['customerUsername']
    
    #Provide a log message upon accessing the route with information of the specific action taken on the route.
    logMessage = "The customer with ID " + str(customerID) + " logged out of the Customer - ALS API."
    
    #Provide a category for the ability to search based on action of the log.
    logCategory = "/customer/logout route was accessed."
    
    #Provide which section of the web-app was accessed.
    logUser = customerUsername
    
    #Provide the location where the log was entered.
    logLocation = "/customer/logout"
    
    #Insert the log data into the "messageLogs" database.
    cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
    
    #Commit the log to the "alsDB.db" database.
    mydb.commit()

    #End the "session['customerUsername']" variable and set to none.
    session.pop('customerUsername', None)

    #End the "session['customerLoggedIn']" variable and set to none.
    session.pop('customerLoggedIn', None)
    
    #End the "session['customerID']" variable and set to none.
    session.pop('customerID', None)
    
    #Provide the user a logged out message.
    loggedOutMsg = "You have succesfully logged out!"
        
    #Render the "/templates/customer/customerlogin.html" to the user when the "/customer/logout" route is accessed.
    return render_template('customer/customerlogin.html', _loggedOutMsg = loggedOutMsg)

'''
Pop the system users session variables when the "/user/logout" route is accessed to log the user out of the system user part of the web-app system.
'''
@app.route('/user/logout', methods=['GET','POST'])
def userlogout():

    #Provide the user a logged out message.
    loggedOutMsg = "You have succesfully logged out!"
        
    '''
    Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
    '''

    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
    cursor = mydb.cursor()
    
    #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
    sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
    
    #Execute the "sqlQ" query.
    cursor.execute(sqlQ)

    #Access the current datetime. 
    logDate = datetime.now()
    
    #Initialise the "systemUserID" variable as the "session['systemUserID']"'s variable value.
    userID = session['systemUserID']
    
    #Provide a log message upon accessing the route with information of the specific action taken on the route.
    logMessage = "The user with ID " + str(userID) + " logged out of the Customer - ALS API."
    
    #Provide a category for the ability to search based on action of the log.
    logCategory = "/user/logout route was accessed."
    
    #Provide which section of the web-app was accessed.
    logUser = userID
    
    #Provide the location where the log was entered.
    logLocation = "/user/logout"
    
    #Insert the log data into the "messageLogs" database.
    cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
    
    #Commit the log to the "alsDB.db" database.
    mydb.commit()
    
    #End the "session['usersUsername']" variable and set to none.
    session.pop('usersUsername', None)

    #End the "session['userLoggedIn']" variable and set to none.
    session.pop('userLoggedIn', None)
    
    #End the "session['systemUserID']" variable and set to none.
    session.pop('systemUserID', None)
    
    #Render the "/templates/user/login.html" to the user when the "/user/logout" route is accessed.
    return render_template('user/login.html', _loggedOutMsg = loggedOutMsg)

'''
Pop the administrative users session variables when the "/admin/logout" route is accessed to log the user out of the admin part of the web-app system.
'''
@app.route('/admin/logout', methods=['GET','POST'])
def adminlogout():
        
    '''
    Provide log information to store in "alsDB.db" database, including datetime of when the log is entered, a log message to provide information on the specific log, a log category for sorting techniques when logs are accessed via the admin later, a logUser field to provide which part of the web-app system was accessed/used at the time of the log.
    '''

    #Setup local sqlite3 database connection to the "alsDB.db" and store in "mydb" variable.
    mydb = sqlite3.connect('alsDB.db')
    
    #Provide a cursor object for querying the "alsDB.db" sqlite3 database.
    cursor = mydb.cursor()
    
    #Create a database table if non-existent "messageLogs" which will be supplied with messages based on the activity of certain actions on the web-app for informative information and/or data to be accessable by the administrative user(s) of the web-app.
    sqlQ = "CREATE TABLE IF NOT EXISTS messageLogs(logDate VARCHAR(255), logMessage VARCHAR(255), logCategory VARCHAR(255), logUser VARCHAR(255), logLocation VARCHAR(255))"
    
    #Execute the "sqlQ" query.
    cursor.execute(sqlQ)

    #Access the current datetime. 
    logDate = datetime.now()
    
    #Provide a log message upon accessing the route with information of the specific action taken on the route.
    logMessage = "The administrative user with username " + session['adminUsername'] + " logged out of the Admin - ALS API."
    
    #Provide a category for the ability to search based on action of the log.
    logCategory = "/admin/logout route was accessed."
    
    #Provide which section of the web-app was accessed.
    logUser = session['adminUsername']
    
    #Provide the location where the log was entered.
    logLocation = "/admin/logout"
    
    #Insert the log data into the "messageLogs" database.
    cursor.execute("INSERT INTO messageLogs(logDate, logMessage, logCategory, logUser, logLocation) VALUES(?,?,?,?,?)",(logDate, logMessage, logCategory, logUser, logLocation))
    
    #Commit the log to the "alsDB.db" database.
    mydb.commit()
    
    #End the "session['adminUsername']" variable and set to none.
    session.pop('adminUsername', None)

    #End the "session['adminLoggedIn']" variable and set to none.
    session.pop('adminLoggedIn', None)
    
    #Provide the user a logged out message.
    loggedOutMsg = "You have succesfully logged out!"
    
    #Render the "/templates/admin/login.html" to the user when the "/admin/logout" route is accessed.
    return render_template('admin/login.html', _loggedOutMsg = loggedOutMsg)

#Run the web-app system with the debug mode on.
if __name__ == "__main__":
	app.run(debug=True)