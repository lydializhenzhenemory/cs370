# detectaive
![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/3b91b0e2-c8b5-4baf-bf21-cc7b3baa9286)

```mermaid
sequenceDiagram
    participant aws database
    participant back4app backend
    participant firebase frontend
    participant cloudfare url
    participant user

    user->>cloudfare url: access website through the registered url
    cloudfare url->>firebase frontend: cloudfare fetches the hosted frontend
    firebase frontend->>firebase frontend: user signs in using Google OAuth
    firebase frontend->>back4app backend: sends user information
    firebase frontend->>back4app backend: requests story/GPT response
    back4app backend->>aws database: stores user information
    back4app backend->>aws database: requests story/additional info
    back4app backend->>back4app backend: sends requests to ChatGPT 4.0
```

# setup:
Note: While the end user will access everything front to back (i.e. url->frontend->backend->database), it is recommended to do the setup back to front (database->backend->frontend->url) as each step requires information from the previous one.

## Cloudfare (optional)
### Create account
Head to [Cloudfare](https://www.cloudflare.com/ ) and create an account
### Search for and purchase domain
Once you have an account, navigate to 'Domain Registeration' to purchase your domain
### Add firebase-provided ip to Type A and Type TXT DNS Records
Once you have a domain, go into domain management and into DNS records. In firebase, navigate to the Hosting page and click 'add a custom domain.' Then add both a TYPE A and TYPE TXT DNS record in cloudfare using the information provided by Firebase hosting.
### Optional: Set up CNAME record for subdomains (like www.)
This will allow you to access the website using www. so instead of just detectaive.com, users will also be able to use www.detectaive.com

## Firebase
### Frontend vue project
### Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### Hosting
Navigate to [Firebase](https://firebase.google.com/) to create an account and a project. Next, download and set up CLI. Once you are done, type
```
firebase init hosting
```
and follow the instructions listed there. You will be asked to choose a project, directory and configuration. After that is done, all that is left is to drag built frontend from dist folder frpm your vue project into public folder of your firebase directory and type
```
firebase deploy
```

## Back4App
### Create account
Navigate to [Back4App](https://www.back4app.com/), create and account and a project.
### Fork the backend code on github
Back4app will try to host the code directly from a github repo which you need to own so you will need to fork a version of the backend.
### Create new backend container for that forked project
Make sure the Docker file is present then select the repo in project, Back4App should take care of the rest. To use the new backend in the frontend, you will need to replace the current backend url with the one provided by Back4App
### Setting up Enviornmental Variables
These help keep secrets (like API keys) hidden from the end user. You will need to enter your OPENAI_API_KEY, and database information like HOST, PORT, DATABASE, USER, and PASSWORD. You can either use these names or edit the Docker file.

## AWS
- use with
    - run on command line: mysql -h [endpoints] -u [username] -p
    - connect to Emory Unplugged for ip address that are allowed to access
    - use 
        USE detectaive;
        SHOW TABLES;
        DESCRIBE table_name;
        etc to view and modify columns
