# Job Portal API Backend

## Description

This project demonstrates the backend of a simple job portal, enabling users to create company and candidate profiles, post job vacancies and apply for jobs. The backend is designed to work for two types of users: companies and candidates. Also, some general informaiton about posted vacancies and candidate profiles can be viewed by public users. 

Companies can post, update, and delete their job vacancies, view applications submitted for the vacancies, whereas candidates can post, update and delete their profiles, post applications to open job vacancies and delete their applications. Users must be authorized to be able to perform role-based requests to the backend via API described below. 

Authorization of users is enabled via Auth0 in which two seperate roles (companies and candidates) have been created and assigned seperate permissions. 

## Project dependencies

The project depends on the latest version of Python 3.x which we recommend to download and install from their official website and use a virtual environment to install all dependencies.

## PIP dependencies

After having successfully installed Python, navigate to the root folder of the project (the project must be forked to your local machine) and run the following in a command line:

```
pip3 install -r requirements.txt
```

This will install all the required packages to your virtual environment to work with the project.

## Database setup

The `models.py` file contains connection instructions to the Postgres database, which must also be setup and running. Provide a valid username and password, if applicable. 

1. Create a database with name `jobportal` using Psql CLI:

```
create database jobportal;
```

2. Initiate and migrate the database with the following commands in command line:

```
flask db init
flask db migrate
flask db upgrade
```

This will create all necessary tables and relationships to work with the project.

## Data Modelling

The data model of the project is provided in `models.py` file in the root folder. The following schema for the database and helper methods are used for API behaviour:

- There are four tables created: Company, Candidate, Vacancy, and Application.
- The Company table is used by the role 'Company' to add the company profile, update and delete them from the database. The information can be retrieved by any user.
- The Candidate table stored all the information about candidates and is used by 'Candidate' user to create, update and delete their profiles.
- The Vacancy table is used by 'Company' user to create, update and delete job vacancies after they have created their company profile. This table is also used by any user to view vacanies as a list and details of a particular vacancy.
- The vacancy table has a foreign key on the Company table for company_id.
- The Application table is used by a 'Candidate' user to create and delete applications for vacancies, which are initially posted by 'Company' user.
- The Application table has three foreign keys: one on the Company table for company_id, one on the Candidate table for candidate_id, and one on the Vacancy table for vacancy_id. 

## Running the local development server

All necessary credential to run the project are provided in the `setup.sh` file. The credentials can be enabled by running the following command:

```
source setup.sh
```

To run the API server on a local development environmental the following commands must be additionally executed:

### On Linux: export
```
export FLASK_APP=app.py
export FLASK_ENV=development
```

### On Windows: set
```
set FLASK_APP=app.py
set FLASK_ENV=development
```

### API Server

All accessable endpoints of the project are located in the `app.py` file.

Run the following command in the project root folder to start the local development server:

```
flask run
```

## RBAC credentials and roles

Auth0 was set up to manage role-based access control for two users. The API documentation below describes, among others, by which user the endpoints can be accessed. Access credentials and permissions are handled with JWT tockens which must be included in the request header. 

### Permissions

Companies can access API endpoints that have the following permission requirements:

`'post:companies'` - Post company information to the database
`'patch:companies'` - Edit a company information by id
`'delete:companies'` - Delete a company information by id
`'post:vacancies'` - Post a vacancy to the database
`'patch:vacancies'` - Edit a vacancy in the database by id
`'delete:vacancies'` - Delete a vacancy by id from the database
`'get:candidates'` - Get a list of applications by vacancy id

Candidates can access API endpoints that have the following permission requirements:

`'post:candidates'` - Post a candidate information to the database
`'patch:candidates'` - Edit a candidate information by id
`'delete:candidate'` - Delete a candidate profile by id
`'post:application'` - Submit an application by vacancy id
`'delete:application'` - Delete an application by application id
`'get:applications'` - Get a list of submitted applications by candidate id

There are also publicly available endpoints that do not require authorization. This is done to ensure every user can see the general information about jobs and candidates.

## API endpoints

### Public endpoints

#### GET '/companies'
- Fetches a dictionary with id and names of companies who posted their information to the database.
- Request Arguments: None
- Returns: A JSON object with two keys: 'success' and 'company_list' - a dictionary with company id and name.

Sample curl request:
`curl -X GET http://127.0.0.1:5000/companies `

Sample response:
```
{
    "companies": {
        "1": "Amazon",
        "2": "Google",
        "3": "Facebook"
    },
    "success": true
}
```
#### GET '/companies/<int:company_id>'
- Fetches detailed information about a company by company ID
- Request arguments: None
- Returns: A JSON object with two keys: 'success' and 'company' = a dictionary with all company infomration.

Samples curl request:

`curl -X GET http://127.0.0.1:5000/companies/2 `

Sample response:
```
{
    "company": {
        "address": "1600 Amphitheatre Parkway",
        "city": "Mountain View",
        "description": "Google LLC is an American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, a search engine, cloud computing, software, and hardware.",
        "email": "info@gmail.com",
        "employee": 10000,
        "facebook_link": "https://www.facebook.com/GoogleDE/?brand_redir=104958162837",
        "id": 2,
        "industry": "IT",
        "logo_link": null,
        "name": "Google",
        "phone": null,
        "region": "California",
        "seeking_employee": true,
        "website_link": "https://www.google.com"
    },
    "success": true
}
```

#### GET '/candidates/<int:candidate_id>'
- Fetches detailed information about a candidate by id (candidate profile)
- Request arguments: none
- Returns: a JSON object with two keys: 'success' and 'candidate' - a dictionary with all details posted by the candidate

Sample curl request:

`curl -X GET http://127.0.0.1:5000/candidates/2 `

Sample response:
```
{
    "candidate": {
        "address": "Addresss",
        "city": "City",
        "date_of_birth": "date",
        "desired_industry": "IT",
        "desired_salary": 100000,
        "education": "Education information",
        "email": "sample@email.com",
        "facebook_link": "https://www.facebook.com/profilelink",
        "id": 2,
        "linkedin_link": "https://www.linkedin.com/in/profilelink",
        "name": "Max",
        "phone": "+1234567890",
        "region": "region",
        "seeking_job": true,
        "surname": "Musterman",
        "work_experience": "Information about the work experience"
    },
    "success": true
}
```

#### GET '/vacancies'
- Fetches short information about all vacancies
- Request argument: none
- Returns: A JSON object with two keys: 'success and 'vacancies' - a list of dictionaries with the main information about vacancies

Sample curl request:

`curl -X GET http://127.0.0.1:5000/vacancies`

Sample response:
```
{
    "success": true,
    "vacancies": [
        {
            "city": "Frankfurt",
            "company_id": 2,
            "company_name": "Google",
            "date_posted": "01.08.2020",
            "id": 2,
            "job_title": "Full Stack Web Developer",
            "min_salary": 80000,
            "region": "Hesse, Germany"
        }
    ]
}
```

#### GET '/vacancies/<int:vacancy_id>'
- Fetches all posted information about a particular vacancy by id
- Request arguments: none
- Returns: a JSON object with two keys: 'success' and 'vacancy' - a dictionary with all information about a vacancy

Sample curl request:

`curl -X GET http://127.0.0.1:5000/vacancies/2`

Sample response:
```
{
    "success": true,
    "vacancy": {
        "benefits": "comfortable office in the city center, 30 days of vacation, career development and growth, opportunity to work remotely",
        "city": "Frankfurt",
        "company_id": 2,
        "company_name": "Google",
        "date_posted": "01.08.2020",
        "id": 2,
        "job_description": "The company seeks to employ a developer with deep understanding of backend and front end technologies, who will be able to handle requests from multiple projects and take part in developing new ones",
        "job_title": "Full Stack Web Developer",
        "min_salary": 80000,
        "region": "Hesse, Germany",
        "requirements": "- 5+ projects, good knowledge of Python, Flask/Django, html, css, JS, Bootstrap, JQuery, - knowledge of Git"
    }
}
```

### Endpoints accessable by Company user

#### POST '/companies'
- Creates a company profile in the database
- Request arguments: a JSON formatted object with optional keys 'name', 'industry', 'employee', 'city', 'region', 'address', 'email', 'phone', 'logo_link', 'facebook_link', 'website_link', 'description', 'seeking_employee' (boolean).
- Returns: a JSON object with success status true when new company information was successfully added into the database.

Sample curl request:
```
curl -d '{"name":"Google", "region": "California", "seeking_employee": true, "website_link": "https://www.google.com"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY" -X POST http://127.0.0.1:5000/companies
```

Sample response:
```
{
    'success': True
}
```

#### PATCH '/companies/<int:company_id>'
- Enables updating of existing company data in the database or add new company information
- Request arguments: a JSON formatted object with optional keys 'name', 'industry', 'employee', 'city', 'region', 'address', 'email', 'phone', 'logo_link', 'facebook_link', 'website_link', 'description', 'seeking_employee' (boolean).
- Returns: a JSON object with success status true and company id when the company information was successfully updated into the database.

Samples curl request:
```
curl -d '{"address": "1600 Amphitheatre Parkway", "city": "Mountain View", "description": "Google LLC is an American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, a search engine, cloud computing, software, and hardware.", "employee": 10000}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY" -X POST http://127.0.0.1:5000/companies/2
```

Sample response:
```
{
    'success': True,
    'id': 2
}
```

#### DELETE '/companies/<int:company_id>'
- Deletes all company information from the database
- Request parameters: none
- Returns: a JSON object with success status true and company id when the company information was successfully deleted from the database.

Sample curl request:
```
curl -X DELETE http://127.0.0.1:5000/companies/2 -H "Authorization: Bearer $USER_TOKEN_COMPANY"
```

Sample response:
```
{
    'success': True,
    'id': 2
}
```

#### POST '/vacancies'
- Creates a job vacancy information in the database which can be accessed with GET request
- Request arguments: a JSON formatted object with optional keys 'job_title', 'job_description', 'requirements', 'benefits', 'city', 'region', 'min_salary', 'company_id' (mandatory).
- Returns: a JSON object with success status true when the vacancy information was successfully added into the database.

Sample curl request:
```
curl -d '{"company_id": 2, "job_description": "The company seeks to employ a developer with deep understanding of backend and front end technologies, who will be able to handle requests from multiple projects and take part in developing new ones",
"job_title": "Full Stack Web Developer", "min_salary": 80000, "region": "Hesse, Germany",
"requirements": "- 5+ projects, good knowledge of Python, Flask/Django, html, css, JS, Bootstrap, JQuery, - knowledge of Git"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY" -X POST http://127.0.0.1:5000/vacancies
```

Sample response:
```
{
    'success': True
}
```

#### PATCH '/vacancies/<int:vacancy_id>'
- Enables updating of existing vacancy data in the database or add more information
- Request arguments: a JSON formatted object with optional keys 'job_title', 'job_description', 'requirements', 'benefits', 'city', 'region', 'min_salary', 'company_id' (mandatory).
- Returns: a JSON object with success status true and vacancy id when the vacancy information was successfully updated in the database.

Sample curl request:
```
curl -d '{"benefits": "comfortable office in the city center, 30 days of vacation, career development and growth, opportunity to work remotely", "city": "Frankfurt"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY" -X PATCH http://127.0.0.1:5000/vacancies/2
```

Sample response:
```
{
    'success': True,
    'id': 2
}
```

#### DELETE '/vacancies/<int:vacancy_id>'
- Deletes all vacancy information from the database
- Request parameters: none
- Returns: a JSON object with success status true and vacamcu id when the vacancy information was successfully deleted from the database.

Sample curl request:
```
curl -X DELETE http://127.0.0.1:5000/vacancies/2 -H "Authorization: Bearer $USER_TOKEN_COMPANY"
```

Sample response:
```
{
    'success': True,
    'id': 2
}
```

#### GET '/vacancies/<int:vacancy_id>/applications'
- Fetches the list of applications submitted for a given vacancy id
- Request arguments: pagination
- Returns: a JSON formatted object with success status true and 'application_list' as a list of dictionaries containing applications, and 'number_applications'

Samples curl request:
```
curl -X GET http://127.0.0.1:5000/vacancies/2/applications -H "Authorization: Bearer $USER_TOKEN_COMPANY"
```

Sample response:
```
{
    "applications_list": [
        {
            "application_id": 4,
            "candidate_id": 2,
            "candidate_name": "Max",
            "candidate_surname": "Musterman",
            "cover_letter": "I want to apply for this position because I am the most suitable for this job",
            "date_submitted": "Thu, 30 Jul 2020 00:51:02 GMT",
            "vacancy_id": 2
        }
    ],
    "number_applications": 1,
    "success": true
}
```

### Endpoints accessable by Candidate users

#### POST '/candidates'
- Creates a candidate profile in the database, which can then be accessed with GET requests
- Request arguments: a JSON formatted object with optional keys 'name', 'surname', 'date_of_birth', 'city', 'region', 'email', 'phone', 'facebook_link', 'linkedin_link', 'address', 'work_experience', 'education', 'seeking_job', 'desired_salary', 'desired_industry'.
- Returns: a JSON object with success status true when the candidate information was successfully inserted into the database.

Sample curl request:
```
curl -d '{"date_of_birth": "date", "desired_industry": "IT", "desired_salary": 100000, "education": "Education information", "email": "sample@email.com", "facebook_link": "https://www.facebook.com/profilelink", "linkedin_link": "https://www.linkedin.com/in/profilelink", "name": "Max", "phone": "+1234567890", "region": "region", "seeking_job": true, "surname": "Musterman"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_CANDIDATE" -X POST http://127.0.0.1:5000/candidates
```

Sampel response:
```
{
    'success': True
}
```

#### PATCH '/candidates/<int:candidate_id>'
- Updates a candidate profile information in the database
- Request arguments: a JSON formatted object with optional keys 'name', 'surname', 'date_of_birth', 'city', 'region', 'email', 'phone', 'facebook_link', 'linkedin_link', 'address', 'work_experience', 'education', 'seeking_job', 'desired_salary', 'desired_industry'.
- Returns: a JSON object with success status true and candidate id when the candidate information was successfully updated in the database.

Sample curl request:
```
curl -d '{"address": "Addresss", "city": "City", "work_experience": "Information about the work experience"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_CANDIDATE" -X POST http://127.0.0.1:5000/candidates/2
```

Sample response:
```
{
    'success': True,
    'id': 2
}
```

#### DELETE '/candidates/<int:candidate_id>
- Deletes all candidate profile informaiton from the database
- Request arguments: none
- Returns: a JSON formatted object with success true and candidate id when the candidate information waas successfully deleted from the database.

Sample curl request:
```
curl -X DELETE http://127.0.0.1:5000/candidates/2 -H "Authorization: Bearer $USER_TOKEN_CANDIDATE"
```

Sample response:
```
{
    'success': True,
    'id': 2
}
```

#### GET '/candidates/<int:candidate_id>/applications'
- Fetches the list of applications which the candidate has submitted to job vacancies
- Request arguments: pagination
- Returns: a JSON formatted object with success status true, a paginated list of applications, and the number of all submitted applications.

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/candidates/2/applications -H "Authorization: Bearer $USER_TOKEN_CANDIDATE"
```

Sample response:
```
{
    "applications_list": [
        {
            "application_id": 4,
            "company_id": 2,
            "company_name": "Google",
            "cover_letter": "I want to apply for this position because I am the most suitable for this job",
            "date_submitted": "Thu, 30 Jul 2020 00:51:02 GMT",
            "vacancy_id": 2,
            "vacancy_job_title": "Full Stack Web Developer"
        }
    ],
    "number_applications": 1,
    "success": true
}
```

#### POST '/vacancies/<int:vacancy_id>/applications'
- Submits an applicaiton for an existing job vacancy under given vacancy id in the database
- Request arguments: a JSON formatted object with mandadory keys 'company_id', 'candidate_id', and optional 'cover_letter'.
- Returns: a JSON object with success status true when the application information was successfully inserted into the database.

Sample curl request:
```
curl - d '{"company_id": 2, "candidate_id": 2, "cover_letter": "Some text here"}' -H "Authorization: Bearer $USER_TOKEN_CANDIDATE" -X POST http://127.0.0.1:5000/vacancies/2/applications
```

Sample response:
```
{
    'success': True
}
```

#### DELETE '/applications/<int:application_id>
- Deletes an application by id from the database
- Request arguments: none
- Returns: a JSON object with success status true and deleted application id when the application information was successfully deleted from the database.

Sample curl request:
```
curl -X DELETE http://127.0.0.1:5000/applications/2 -H "Authorization: Bearer $USER_TOKEN_CANDIDATE"
```

Sample response:
```
{
    'success': True,
    'id': 2
}
```

## Testing

The testing of all endpoints was implemented with unittest. Each endpoint can be tested with one success test case and one error test case. RBAC feature can also be tested for company user and candidate user.

All test cases are soted in `test_app.py` file in the project rool folder.

Before running the test application, create `jobportal_test` database using Psql CLI:
```
create database jobportal_test
```

Then in the command line interface run the test file:

`python3 test_app.py`

## Heroku Deployment and Base URL

The backend application has been deployed on Heroku and can be accessed live at
```
https://jobportal-backend.herokuapp.com/
```
