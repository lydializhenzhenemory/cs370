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

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/6887319f-7d52-402e-b45e-16949d1c0cdf)

### Search for and purchase domain
Once you have an account, navigate to 'Domain Registeration' to purchase your domain

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/4f3e839f-aaa6-4b2b-a9ca-eb2a915cc6cd)

### Add firebase-provided ip to Type A and Type TXT DNS Records
Once you have a domain, go into domain management and into DNS records. In firebase, navigate to the Hosting page and click 'add a custom domain.' Then add both a TYPE A and TYPE TXT DNS record in cloudfare using the information provided by Firebase hosting.

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/7ed636df-c5c5-4db9-853f-2ade4614e570)

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/f70af15d-2616-474c-a20f-76ea3f33369b)
![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/55791f1e-530e-450a-addc-0008ee5a168c)

### Optional: Set up CNAME record for subdomains (like www.)
This will allow you to access the website using www. so instead of just detectaive.com, users will also be able to use www.detectaive.com

## Firebase
### Create account and project
Navigate to [Firebase](https://firebase.google.com/) to create an account and a project. 

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/3674db80-e2ce-4c46-992f-dd7c562f649c)

### Set up CLI
Next, download and set up [CLI](https://firebase.google.com/docs/cli#install_the_firebase_cli). Make sure to follow the appropriate instructions for your operating system. Once you are done, type
```
firebase init hosting
```
and follow the instructions listed there. You will be asked to choose a project, directory and configuration. After that is done, all that is left is to drag the built frontend from dist folder from your vue project into the public folder of your Firebase directory.

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/2defbf1d-32d7-4718-a8ac-a29f3bea5cbd)

### Deploying project
Once that is done, type

```
firebase deploy
```
into the CLI. This should fully deploy your frontend code to Firebase.

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/08b5d0c2-bc22-4c90-a747-119622a2e590)

### Optional: Setting up Google Authentication
Optionally, this is also where you can set up your google authentication, if you are using that.

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/9f5b3bb4-3edb-4a88-971f-f0f55e82d9d3)

If you do, you will need to replace the firebase api key with your own, it should look something like this:

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/aa632df6-f559-4463-b1bb-6ccfa9a22225)
(since the firebase API keys are only used to identify the project on the google servers, they are safe to expose to the public)

## Back4App
### Create account
Navigate to [Back4App](https://www.back4app.com/), create and account and a project.

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/d204fd11-e904-46ac-9f77-8ea2245e1b15)

### Fork the backend code on github
Back4app will try to host the code directly from a github repo which you need to own so you will need to fork a version of the backend.

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/22ef2280-9a3c-4694-9183-60f3864473c9)

### Create new backend container for that forked project
Make sure the Docker file is present then select the repo in project, Back4App should take care of the rest. To use the new backend in the frontend, you will need to replace the current backend url with the one provided by Back4App

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/cd20c2bf-6eba-455b-b24c-9253f46bfb3b)

### Setting up Enviornmental Variables
These help keep secrets (like API keys) hidden from the end user. You will need to go into settings then environment variables to enter your OPENAI_API_KEY, and database information like HOST, PORT, DATABASE, USER, and PASSWORD. You can either use these names or edit the Docker file.

![image](https://github.com/lydializhenzhenemory/cs370/assets/97063631/58b78c7b-1b64-4843-b3ae-40c4bb5e9c24)
(These API keys should be kept secure)

## AWS
- use with
    - run on command line: mysql -h [endpoints] -u [username] -p
    - connect to Emory Unplugged for ip address that are allowed to access
    - use 
        USE detectaive;
        SHOW TABLES;
        DESCRIBE table_name;
        etc to view and modify columns
