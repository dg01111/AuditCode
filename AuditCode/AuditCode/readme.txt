Author: Danielle Gorman
Date: 23/01/2023
Purpose: The purpose of this file is to provide instructions of how to run and operate the Audit Log Service API. Instructions are based on Ubuntu Terminal instructions

Instructions
1. The take home test is in the Canonical directory. To run the Audit Log Service API web-app system, change dirctory to the Canonical folder -> cd /Canonical
2. Type the command into the Terminal -> python -m audithome flask --app run
3. Open a browser and type the URL address http://127.0.0.1:5000/admin/login 
4. You can log in using the credentials mentioned below 
	Username: admin
	Password: test
Or you can check the admin credentials to log in to the above link using the command in another  Terminal using the command from the Canonical folder -> sqlite3 alsDB.db
then check the credentials using the command on the Terminal -> SELECT * FROM adminLogin;
5. The administrative user then has access to the logs, ability to view system users, add system users, update and delete system users.
6. When a system user has been added to the system, the link to the system user part of the system can be accessed via http://127.0.0.1:5000/user/login with the login credentials provided by the administrative user when they created a system user at http://127.0.0.1:5000/admin/loggedin/addsystemuser
When the system user is logged in, they can add, update, view and delete customer accounts, create and send those customers audits, and view the customers employed/self-employed audits via the http://127.0.0.1:5000/user/loggedin/home route.
The customer whose account was added by the system user can log in to the http://127.0.0.1:5000/customer/customerlogin using the username and password supplied by the system user on the http://127.0.0.1:5000/user/loggedin/addcustomer
The customer can view and pay the audits that have been sent to them by accessing the links on the http://127.0.0.1:5000/customer/loggedin/viewpayaudit
