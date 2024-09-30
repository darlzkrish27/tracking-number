# Tracking-number Django

This is a [Django](http://www.djangoproject.com) project that you can use as the starting point to develop your own and deploy it on an aws EC2 instance.


## Steps to run application

This is a minimal Django 4.2.3 project. following are the steps to run the app in local server (localhost) on port 8080:

1. Create a virtualenv
2. Manually install Django and other dependencies
3. `pip install -r requirements.txt`
4. `python ./manage.py runserver`, to get the application will run on localhost:8000

## Deployement
1. Install Nginx and Gunicorn in the server you want to have the application
2. Check Nginx is working if it is linux server `sudo systemctl start nginx`
3. Configure Nginx file with the project path given and add static files path
	```
	server{

        listen 80;
        server_name 13.60.92.251;


        #location / {
                #include proxy_params;
                #proxy_pass http://unix:/home/ubuntu/tracking-number/tracking-number/parcel_tracker/parcel_tracker/app.sock;

        #}
        # Django static files
        location /static {
            alias /home/ubuntu/tracking-number/tracking-number/parcel_tracker/staticfiles/;
            expires 30d;
        }
        # Django application
        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Host $http_host;
            proxy_pass http://localhost:8000;
            proxy_redirect off;
        }

}
	```
4. Link sites-available and site-enabled folders and restart nginx service `sudo systemctl restart nginx`
5. Run the application.
