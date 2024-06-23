In this Project, I am using Python , flask , and sqlite . On the home page , I have created 2 buttons :- One for Operational user and other for for Client user.
I am using Sqlalchemy as a ORM and making 2 database models:-
The first is for File, where I store (filename,file data in Binary format, uploaded by, uploaded at). 
The second is for User, where I store (username,password in a hash format, email, verified status, verification token).

Operational user functionality :-
When the Operational user button clicked, it will redirect me to a login page.
Where I have a single uploader that will upload a file in the database . So, I programmatically add a single user in the database with the username of "Tushank".

Steps for single user :-
I have made a varibale name hashed_password . In this , I am store my id password with the help of import generated_password_hash . So, it will store in a hash format with the help of encryption algorithm.
Then, made a another varibale called operational_user . Where I pass my all details in the User model table in the database and pass all my methods with the values.
In the next step, I made a app_context() for push a context manually. 

Make a login function:- working 
if my form Rrequest is a POST request then , it will get a username and password to the form .
Then, I will make a variable called user and in this varibale i can run a query to the USER table and filter a username. Whatever first username it will get that would store in the user variable.
Now, if user is empty or a password is not matched then it will flash me a message "Invalid username or password" and redirect to login page.
I will use session to store user-specific data between requests. It will store username that will come from the database. 
If username matched with Tushank only then it will redirect to file page. Otherwise, redirect to login page.

Make a file function :-
Using if Else, if username not in session or session username is not matched with Tushank then it will flash me a message to "Access Denied" and redirect to login page. 
Else, redirect to file page

Make a upload function:-
First, Check if the file part is in the request.
Second, Validate that a file has been selected
Third, Secure the filename and read the file content.
Fourth, add all the in the File table in the database and after successfully add it will automatically redirect to the file page.

Now, we will talk to Client user functionality :-
I will use POST method in this , first make a varibale name as existing user I am running a query in the USER table that was present in the db and check that if the user already exist, if yes, then it will redirect to signUp page.
Make a token varibale that will be holding a generated token.
Then, commit all the data related to user like username, password, email, and verfication token commit in the USER table.
Then, we will send the verification mail message and link with the help of recipients.
Make a verfication link for verify mail.
final using error handling to . IF function works then it will send mail otherwise flash a Failed to send verification email.
If funciton will work then it will automatically redirect to clientLogin page.
else, render signUp page.

Make another email verfication function:-
Using error handling for email expires and set max_age about 24hrs after that token will be expires.
make a varibale called user and run query on the USER table for filter token.
if user got token then, user verified is true and we will add verification status in the db and also none the verfication token. 
else, return message that "verification failed"

Make ClientLogin funciton :-
Make a user variable and run the query and filter out with the help of username.
if user not exist or hash password is not matched with the clientLogin password then, it will render clientLogin page.
Take username and password from the form and find it in the USER table db . if it exist , only then it will show me innerHomePage.
Otherwise, it will render clientLogin page.

Make a innerhomePage funciton :-
I will made a variable called uploaded name and give strict name "Tushank".
make another variable name as files data and run a query in the FILE table in the database and filter out all the files with uploaded_by Tushank and show all the filenames on the innerHomePage screen with the download button below on the filename.

Make a file download function :-
The function retrieves the file record from the database using the provided filename.
If the file record is found, it extracts the file data.
It creates a response to send the file data as an attachment.
The response includes appropriate headers to indicate the file should be downloaded.
If the file record is not found, the function does nothing.
