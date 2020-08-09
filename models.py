'''
Company table
Candidate table
Vacancy table --> FK company ID (one-to-many) | job description, requirements, benefits etc.
Applications table --> FK vacancy ID, FK candidate ID (many-to-many) | cover letter
'''
import os
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

# Connection instructions - uncomment the two lines below to work on local machine
#database_name = "jobportal"
#database_path = "postgres://{}/{}".format('postgres:mb@localhost:5432', database_name)

# Database on Heroku
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)

'''
Company

'''
class Company(db.Model):  
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    industry = Column(String)
    employee = Column(Integer)
    city = Column(String)
    region = Column(String)
    address = Column(String)
    email = Column(String)
    phone = Column(String)
    logo_link = Column(String)
    facebook_link = Column(String)
    website_link = Column(String)
    description = Column(String)
    seeking_employee = Column(Boolean)
    vacancies = db.relationship('Vacancy', backref=db.backref('company', lazy=True))
    applications = db.relationship('Application', backref=db.backref('companies'), lazy=True)

    def __init__(self, name, industry, employee, city, region, \
                address, email, phone, logo_link, facebook_link, \
                website_link, description, seeking_employee):
        self.name = name
        self.industry = industry
        self.employee = employee
        self.city = city
        self.region = region
        self.address = address
        self.email = email
        self.phone = phone
        self.logo_link = logo_link
        self.facebook_link = facebook_link
        self.website_link = website_link
        self.description = description
        self.seeking_employee = seeking_employee

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'industry': self.industry,
            'employee': self.employee,
            'city': self.city,
            'region': self.region,
            'address': self.address,
            'email': self.email,
            'phone': self.phone,
            'logo_link': self.logo_link,
            'facebook_link': self.facebook_link,
            'website_link': self.website_link,
            'description': self.description,
            'seeking_employee': self.seeking_employee
        }

 

'''
Candidate
'''

class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    date_of_birth = Column(DateTime)
    city = Column(String)
    region = Column(String)
    email = Column(String)
    phone = Column(String)
    facebook_link = Column(String)
    linkedin_link = Column(String)
    address = Column(String)
    work_experience = Column(String)
    education = Column(String)
    seeking_job = Column(Boolean)
    desired_salary = Column(Integer)
    desired_industry = Column(String)
    applications = db.relationship('Application', backref=db.backref('candidate'), lazy=True)
    
    def __init__(self, name, surname, date_of_birth, city, region, email, phone, \
                facebook_link, linkedin_link, address, work_experience, education, \
                seeking_job, desired_salary, desired_industry):
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.city = city
        self.region = region
        self.email = email
        self.phone = phone
        self.facebook_link = facebook_link
        self.linkedin_link = linkedin_link
        self.address = address
        self.work_experience = work_experience
        self.education = education
        self.seeking_job = seeking_job
        self.desired_salary = desired_salary
        self.desired_industry = desired_industry
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'date_of_birth': self.date_of_birth,
            'city': self.city,
            'region': self.region,
            'email': self.email,
            'phone': self.phone,
            'facebook_link': self.facebook_link,
            'linkedin_link': self.linkedin_link,
            'address': self.address,
            'work_experience': self.work_experience,
            'education': self.education,
            'seeking_job': self.seeking_job,
            'desired_salary': self.desired_salary,
            'desired_industry': self.desired_industry
        }

'''
Vacancy
'''

class Vacancy(db.Model):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True)
    job_title = Column(String)
    job_description = Column(String)
    requirements = Column(String)
    benefits = Column(String)
    city = Column(String)
    region = Column(String)
    min_salary = Column(Integer)
    date_posted = Column(DateTime)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    applications = db.relationship('Application', backref=db.backref('vacancies'), lazy=True)

    def __init__(self, job_title, job_description, requirements, benefits, \
                city, region, min_salary, date_posted, company_id):
        self.job_title = job_title
        self.job_description = job_description
        self.requirements = requirements
        self.benefits = benefits
        self.city = city
        self.region = region
        self.min_salary = min_salary
        self.date_posted = date_posted
        self.company_id = company_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit() 

    def format_long(self):
        return {
            'id': self.id,
            'job_title': self.job_title,
            'job_description': self.job_description,
            'requirements': self.requirements,
            'benefits': self.benefits,
            'city': self.city,
            'region': self.region,
            'min_salary': self.min_salary,
            'date_posted': self.date_posted,
            'company_id': self.company_id,
            'company_name': self.company.name
        }

    def format_short(self):
        return {
            'id': self.id,
            'job_title': self.job_title,
            'city': self.city,
            'region': self.region,
            'min_salary': self.min_salary,
            'date_posted': self.date_posted,
            'company_id': self.company_id,
            'company_name': self.company.name
            }


'''
Application
'''
class Application(db.Model):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    cover_letter = Column(String)
    date_submitted = Column(DateTime)

    def __init__(self, company_id, vacancy_id, candidate_id, cover_letter, date_submitted):
        self.company_id = company_id
        self.vacancy_id = vacancy_id
        self.candidate_id = candidate_id
        self.cover_letter = cover_letter
        self.date_submitted = date_submitted

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit() 

   

