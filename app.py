from flask import (
  Flask,
  request,
  abort,
  jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import (
  setup_db,
  Company,
  Candidate,
  Vacancy,
  Application
)
from datetime import datetime
from auth import (
  AuthError,
  requires_auth
)
import math
import os
import sys

ITEMS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r'/*': {'origin': '*'}})

    # set up an Access-Control-Allow decorator
    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    '''
    ROUTES
    '''
    # Welcome message
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
          'message': 'Welcome to My Job Portal Backend API Project. ' \
          +'Please refer to the API documentation in README.md to view ' \
          +'and test available endpoints.'
        })

    '''
    COMPANY
    '''
    # Get all companies
    @app.route('/companies', methods=['GET'])
    def get_companies():
        companies = Company.query.all()

        company_list = {company.id: company.name for company in companies}

        return jsonify({
          'success': True,
          'companies': company_list
        })

    # Get company details by company id
    @app.route('/companies/<int:company_id>', methods=['GET'])
    def get_company_details(company_id):
        company = Company.query.filter(Company.id == company_id).one_or_none()

        if company is None:
            abort(404)

        return jsonify({
          'success': True,
          'company': company.format()
        })

    # Add a new company profile
    @app.route('/companies', methods=['POST'])
    @requires_auth('post:companies')
    def add_company(payload):
        try:
            body = request.get_json()

            new_name = body.get('name')
            new_industry = body.get('industry')
            new_employee = body.get('employee')
            new_city = body.get('city')
            new_region = body.get('region')
            new_address = body.get('address')
            new_email = body.get('email')
            new_phone = body.get('phone')
            new_logo_link = body.get('logo_link')
            new_facebook_link = body.get('facebook_link')
            new_website_link = body.get('website_link')
            new_description = body.get('description')
            new_seeking_employee = body.get('seeking_employee')

            company = Company(name=new_name,
                              industry=new_industry,
                              employee=new_employee,
                              city=new_city,
                              region=new_region,
                              address=new_address,
                              email=new_email,
                              phone=new_phone,
                              logo_link=new_logo_link,
                              facebook_link=new_facebook_link,
                              website_link=new_website_link,
                              description=new_description,
                              seeking_employee=new_seeking_employee
                              )

            company.insert()
            return jsonify({
              'success': True
            })
        except:
            print(sys.exc_info())
            abort(422)

    # Update a company by id
    @app.route('/companies/<int:company_id>', methods=['PATCH'])
    @requires_auth('patch:companies')
    def update_company(payload, company_id):
        company = Company.query.filter(Company.id == company_id).one_or_none()

        if company is None:
            abort(404)

        try:
            body = request.get_json()
            company.name = body.get('name', company.name)
            company.industry = body.get('industry', company.industry)
            company.employee = body.get('employee', company.employee)
            company.city = body.get('city', company.city)
            company.region = body.get('region', company.region)
            company.address = body.get('address', company.address)
            company.email = body.get('email', company.email)
            company.phone = body.get('phone', company.phone)
            company.logo_link = body.get('logo_link', company.logo_link)
            company.facebook_link = body.get(
              'facebook_link', company.facebook_link)
            company.website_link = body.get(
              'website_link', company.website_link)
            company.description = body.get('description', company.description)
            company.seeking_employee = body.get(
              'seeking_employee', company.seeking_employee)

            company.update()

            return jsonify({
              'success': True,
              'id': company_id
            })
        except:
            print(sys.exc_info())
            abort(422)

    # Delete a company by ID
    @app.route('/companies/<int:company_id>', methods=['DELETE'])
    @requires_auth('delete:companies')
    def delete_company(payload, company_id):
        try:
            company = Company.query.filter(
              Company.id == company_id
              ).one_or_none()

            if company is None:
                abort(404)

            company.delete()
            return jsonify({
              'success': True,
              'id': company_id
            })
        except:
            print(sys.exc_info())
            abort(422)

    '''
    CANDIDATE
    '''
    # View candidate profile by id
    @app.route('/candidates/<int:candidate_id>', methods=['GET'])
    def get_candidate_details(candidate_id):
        candidate = Candidate.query.filter(
          Candidate.id == candidate_id
          ).one_or_none()

        if candidate is None:
            abort(404)

        return jsonify({
          'success': True,
          'candidate': candidate.format()
        })

    # Add a new candidate profile
    @app.route('/candidates', methods=['POST'])
    @requires_auth('post:candidates')
    def add_candidate_profile(payload):
        try:
            body = request.get_json()

            new_name = body.get('name')
            new_surname = body.get('surname')
            new_date_of_birth = body.get('date_of_birth')
            new_city = body.get('city')
            new_region = body.get('region')
            new_email = body.get('email')
            new_phone = body.get('phone')
            new_facebook_link = body.get('facebook_link')
            new_linkedin_link = body.get('linkedin_link')
            new_address = body.get('address')
            new_work_experience = body.get('work_experience')
            new_education = body.get('education')
            new_seeking_job = body.get('seeking_job')
            new_desired_salary = body.get('desired_salary')
            new_desired_industry = body.get('desired_industry')

            candidate = Candidate(name=new_name,
                                  surname=new_surname,
                                  date_of_birth=new_date_of_birth,
                                  city=new_city,
                                  region=new_region,
                                  email=new_email,
                                  phone=new_phone,
                                  facebook_link=new_facebook_link,
                                  linkedin_link=new_linkedin_link,
                                  address=new_address,
                                  work_experience=new_work_experience,
                                  education=new_education,
                                  seeking_job=new_seeking_job,
                                  desired_salary=new_desired_salary,
                                  desired_industry=new_desired_industry
                                  )

            candidate.insert()
            return jsonify({
              'success': True
            })
        except:
            print(sys.exc_info())
            abort(422)

    # Update a candidate profile by id
    @app.route('/candidates/<int:candidate_id>', methods=['PATCH'])
    @requires_auth('patch:candidates')
    def update_candidate_profile(payload, candidate_id):
        try:
            candidate = Candidate.query.filter(
              Candidate.id == candidate_id
              ).one_or_none()

            if candidate is None:
                abort(404)

            body = request.get_json()
            candidate.name = body.get('name', candidate.name)
            candidate.surname = body.get('surname', candidate.name)
            candidate.date_of_birth = body.get(
              'date_of_birth', candidate.date_of_birth)
            candidate.city = body.get('city', candidate.city)
            candidate.region = body.get('region', candidate.region)
            candidate.email = body.get('email', candidate.email)
            candidate.phone = body.get('phone', candidate.phone)
            candidate.facebook_link = body.get(
              'facebook_link', candidate.facebook_link)
            candidate.linkedin_link = body.get(
              'linkedin_link', candidate.linkedin_link)
            candidate.address = body.get('address', candidate.address)
            candidate.work_experience = body.get(
              'work_experience', candidate.work_experience)
            candidate.education = body.get('education', candidate.education)
            candidate.seeking_job = body.get(
              'seeking_job', candidate.seeking_job)
            candidate.desired_salary = body.get(
              'desired_salary', candidate.desired_salary)
            candidate.desired_industry = body.get(
              'desired_industry', candidate.desired_industry)

            candidate.update()
            return jsonify({
              'success': True,
              'id': candidate_id
            })
        except:
            print(sys.exc_info())
            abort(422)

    # Deleta a canadidate profile by id
    @app.route('/candidates/<int:candidate_id>', methods=['DELETE'])
    @requires_auth('delete:candidates')
    def delete_candidate_profile(payload, candidate_id):
        try:
            candidate = Candidate.query.filter(
              Candidate.id == candidate_id).one_or_none()

            if candidate is None:
                abort(404)

            candidate.delete()
            return jsonify({
              'success': True,
              'id': candidate_id
            })
        except:
            print(sys.exc_info())
            abort(422)

    '''
    VACANCY
    '''
    # Get the list of vacancies
    @app.route('/vacancies', methods=['GET'])
    def get_vacancies():
        vacancies = Vacancy.query.join(
          Company, Vacancy.company_id == Company.id).all()

        vacancy_short_list = [vacancy.format_short() for vacancy in vacancies]

        return jsonify({
          'success': True,
          'vacancies': vacancy_short_list
        })

    # Get details of a vacancy by id
    @app.route('/vacancies/<int:vacancy_id>', methods=['GET'])
    def get_vacancy_details(vacancy_id):
        vacancy = Vacancy.query.join(
          Company, Vacancy.company_id == Company.id). \
          filter(Vacancy.id == vacancy_id).one_or_none()

        if vacancy is None:
            abort(404)

        return jsonify({
          'success': True,
          'vacancy': vacancy.format_long()
        })

    # Add a new vacancy
    @app.route('/vacancies', methods=['POST'])
    @requires_auth('post:vacancies')
    def add_vacancy(payload):
        try:
            body = request.get_json()

            new_job_title = body.get('job_title')
            new_job_description = body.get('job_description')
            new_requirements = body.get('requirements')
            new_benefits = body.get('benefits')
            new_city = body.get('city')
            new_region = body.get('region')
            new_min_salary = body.get('min_salary')
            new_date_posted = datetime.now()
            new_company_id = body.get('company_id')

            vacancy = Vacancy(job_title=new_job_title,
                              job_description=new_job_description,
                              requirements=new_requirements,
                              benefits=new_benefits,
                              city=new_city,
                              region=new_region,
                              min_salary=new_min_salary,
                              date_posted=new_date_posted,
                              company_id=new_company_id)

            vacancy.insert()
            return jsonify({
              'success': True
            })
        except:
            print(sys.exc_info())
            abort(422)

    # Update a vacancy by id
    @app.route('/vacancies/<int:vacancy_id>', methods=['PATCH'])
    @requires_auth('patch:vacancies')
    def update_vacancy(payload, vacancy_id):
        try:
            vacancy = Vacancy.query.filter(
              Vacancy.id == vacancy_id
            ).one_or_none()

            if vacancy is None:
                abort(404)

            body = request.get_json()
            vacancy.job_title = body.get('job_title', vacancy.job_title)
            vacancy.job_description = body.get(
              'job_description', vacancy.job_description)
            vacancy.requirements = body.get(
              'requirements', vacancy.requirements)
            vacancy.benefits = body.get('benefits', vacancy.benefits)
            vacancy.city = body.get('city', vacancy.city)
            vacancy.region = body.get('region', vacancy.region)
            vacancy.min_salary = body.get('min_salary', vacancy.min_salary)
            vacancy.date_posted = datetime.now()

            vacancy.update()
            return jsonify({
              'success': True,
              'id': vacancy_id
            })
        except:
            print(sys.exc_info())
            abort(422)

    # Delete a vacancy by id
    @app.route('/vacancies/<int:vacancy_id>', methods=['DELETE'])
    @requires_auth('delete:vacancies')
    def delete_vacancy(payload, vacancy_id):
        try:
            vacancy = Vacancy.query.filter(
              Vacancy.id == vacancy_id).one_or_none()

            if vacancy is None:
                abort(404)

            vacancy.delete()
            return jsonify({
              'success': True,
              'id': vacancy_id
            })
        except:
            print(sys.exc_info())
            abort(422)

    '''
    APPLICATION
    '''
    # Get the list of applications by candidate id (for candidates)
    @app.route('/candidates/<int:candidate_id>/applications', methods=['GET'])
    @requires_auth('get:applications')
    def get_applications_by_candidate_id(payload, candidate_id):
        applications = Application.query.join(
          Vacancy, Application.vacancy_id == Vacancy.id) \
          .join(Candidate, Application.candidate_id == Candidate.id) \
          .join(Company, Application.company_id == Company.id) \
          .filter(Application.candidate_id == candidate_id).all()

        # Pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        applications_list = [{
          'application_id': application.id,
          'vacancy_id': application.vacancy_id,
          'vacancy_job_title': application.vacancies.job_title,
          'company_id': application.companies.id,
          'company_name': application.companies.name,
          'cover_letter': application.cover_letter,
          'date_submitted': application.date_submitted
        } for application in applications]

        # Raise error if pagination fetches no applications
        if page > math.ceil(len(applications_list) / ITEMS_PER_PAGE):
            abort(404)

        return jsonify({
          'success': True,
          'applications_list': applications_list[start:end],
          'number_applications': len(applications_list)
        })

    # Get the list of applications by vacancy id (for companies)
    @app.route('/vacancies/<int:vacancy_id>/applications', methods=['GET'])
    @requires_auth('get:candidates')
    def get_applications_by_vacancy_id(payload, vacancy_id):
        applications = Application.query.join(
          Vacancy, Application.vacancy_id == Vacancy.id) \
          .join(Candidate, Application.candidate_id == Candidate.id) \
          .join(Company, Application.company_id == Company.id) \
          .filter(Vacancy.id == vacancy_id).all()

        # Pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        applications_list = [{
          'vacancy_id': application.vacancies.id,
          'application_id': application.id,
          'candidate_id': application.candidate.id,
          'candidate_name': application.candidate.name,
          'candidate_surname': application.candidate.surname,
          'cover_letter': application.cover_letter,
          'date_submitted': application.date_submitted
        } for application in applications]

        # Raise error if pagination fetches no applications
        if page > math.ceil(len(applications_list) / ITEMS_PER_PAGE):
            abort(404)

        return jsonify({
          'success': True,
          'applications_list': applications_list[start:end],
          'number_applications': len(applications_list)
        })

    # Add a new application by vacancy id
    @app.route('/vacancies/<int:vacancy_id>/applications', methods=['POST'])
    @requires_auth('post:application')
    def add_application_by_vacancy_id(payload, vacancy_id):
    # try:
        vacancy = Vacancy.query.filter(
          Vacancy.id == vacancy_id).one_or_none()

        if vacancy is None:
            abort(404)

        body = request.get_json()
        new_company_id = body.get('company_id')
        new_vacancy_id = vacancy_id
        new_candidate_id = body.get('candidate_id')
        new_cover_leter = body.get('cover_letter', None)
        new_date_submitted = datetime.now()

        # Check if multiple applications are submitted
        duplicate = Application.query.filter(
          Application.candidate_id == new_candidate_id,
          Application.vacancy_id == new_vacancy_id).one_or_none()

        if duplicate is not None:
            abort(406)

        application = Application(company_id=new_company_id,
                                  vacancy_id=new_vacancy_id,
                                  candidate_id=new_candidate_id,
                                  cover_letter=new_cover_leter,
                                  date_submitted=new_date_submitted)

        application.insert()
        return jsonify({
          'success': True
        })
    # except:
    #     print(sys.exc_info())
    #     abort(422)

    # Delete an application
    @app.route('/applications/<int:application_id>', methods=['DELETE'])
    @requires_auth('delete:application')
    def delete_application(payload, application_id):
        try:
            application = Application.query.filter(
              Application.id == application_id
              ).one_or_none()

            if application is None:
                abort(404)

            application.delete()
            return jsonify({
              'success': True,
              'id': application_id
            })
        except:
            print(sys.exc_info())
            abort(422)

    '''
    ERROR HANDLERS
    '''

    # Error handler for 404 ("Not found")
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          'success': False,
          'error': 404,
          'message': 'Not found'
        }), 404

    # Error handler for 422 ("Unprocessable")
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          'success': False,
          'error': 422,
          'message': 'Unprocessable'
        }), 422

    # Error handler for 500 ("Internal server error")
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal server error'
        }), 500

    # Error handler for 400 ("Bad request")
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad request'
        }), 400

    # Error handler for 406 ("Not acceptable")
    @app.errorhandler(406)
    def not_acceptable(error):
        return jsonify({
          'success': False,
          'error': 406,
          'message': 'Not acceptable'
        }), 406

    # Error handler for Auth decorator
    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify(e.error), e.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    APP.run(host='0.0.0.0', port=port)
