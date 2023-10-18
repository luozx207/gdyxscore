### A point system for Guangdong Telecommunication School

Running environment: python3.6+Flask 0.12.2
This is a  point system for Guangdong Telecommunication School, using flask template, sqlite database, jinja template rendering front-end
The function is almost achieved, but the front-end still needs to be improved

Frontend part:
1, pre-registration page, users can submit their pre-registration information, this part of the information exists in a separate data table
2、Login as well as registration page. The user information is stored in the user table, and the session is used to remember the user's login information.
3、After logging in , the user can check his points and recommend others to enroll in the school , the successful recommendation will increase the user's points (the recommended person is placed in the table re , with the attribute user_id associated with the user )
4, you can use the points to exchange prizes

background (background.py) part:
1, the administrator account and ordinary users in the same table, but the administrator account auth attribute value of 1, other users for 0
2, with a decorator to write a function to verify the user's rights, decorating each page of the background
3, the background can view all the users and recommended people, and can change the enrolment status of the recommended people , zero user points , etc., but also by mobile phone number to find the user or recommended people
