# Tracking-number Django

This is a [Django](http://www.djangoproject.com) project that you can use as the starting point to develop your own and deploy it on an aws EC2 instance.


## Installation 

This is a minimal Django 4.2.3 project. following are the steps to run the app in local server (localhost) on port 8080:

1. Clone the repository using `git clone`
2. Create a virtualenv
	`python -m venv venv`
3. Activate the environment.
	`source venv/bin/activate`
4. Install Django and other python dependencies
	`pip install -r requirements.txt`
5. Create a new database using `python manage.py migrate`

## Running the Application

1. Run the development server using `python manage.py runserver`
2. Access the application at `http://localhost:8000`

## Testing the Application using postman


1. Using GET call in postman call the url  `http://13.60.92.251/next-tracking-number/` will give you output like below

	```
	{
    	"tracking_number": "0LW0CULCUU1IQCL9",
    	"created_at": "2024-09-30T10:52:54.192386Z"
        }	
	```
