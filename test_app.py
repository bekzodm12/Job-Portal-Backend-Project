import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import (
    setup_db,
    Company,
    Candidate,
    Vacancy,
    Application
)


class JobPortalTestCase(unittest.TestCase):
    '''This class represents the jobportal test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "jobportal_test"
        self.database_path = "postgres://{}/{}". \
            format('postgres:mb@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.test_user_company = os.environ['USER_TOKEN_COMPANY']
        self.test_user_candidate = os.environ['USER_TOKEN_CANDIDATE']

        self.new_company = {
            "address": "1600 Amphitheatre Parkway",
            "city": "Mountain View",
            "description": "Google LLC is an American multinational \
                technology \
                company that specializes in Internet-related services and \
                products, which include online advertising technologies, \
                a search engine, cloud computing, software, and hardware.",
            "email": "info@gmail.com",
            "employee": 10000,
            "facebook_link":
                "https://www.facebook.com/GoogleDE/?brand_redir=104958162837",
            "industry": "IT",
            "name": "Google",
            "region": "California",
            "seeking_employee": True,
            "website_link": "https://www.google.com"
        }

        self.edit_company = {
            "name": "Google Inc."
        }

        self.new_candidate = {
            "name": "Max",
            "surname": "Musterman"
        }

        self.edit_candidate = {
            "date_of_birth": '01.01.2000',
            "city": "San Francisco",
            "region": "California"
        }

        self.new_vacancy = {
            "job_title": "Full-Stack Developer",
            "city": "San Francisco",
            "region": "California",
            "company_id": 1
        }

        self.edit_vacancy = {
            "min_salary": 100000
        }

        self.new_application = {
            "company_id": 1,
            "candidate_id": 1,
            "cover_letter": "I am a perfect candidate"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    '''
    POST
    '''
    '''
    Company
    '''
    def test_add_new_company(self):
        '''Tests successful request to post a new company into the database'''
        res = self.client().post('/companies', json=self.new_company,
                                 headers={
                                     'Authorization': 'Bearer '
                                     + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_404_not_found_when_add_company(self):
        '''Tests error 404 for incorrect route'''
        res = self.client().post('/company', json=self.new_company,
                                 headers={
                                     'Authorization': 'Bearer '
                                     + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    Candidate
    '''
    def test_add_new_candidate(self):
        '''Tests successful request to post a new
        candidate profile into the database'''
        res = self.client().post('/candidates', json=self.new_candidate,
                                 headers={
                                     'Authorization': 'Bearer '
                                     + self.test_user_candidate})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_404_not_found_add_new_candidate(self):
        '''Tests error 404 for incorrect route'''
        res = self.client().post('/candidate', json=self.new_candidate,
                                 headers={
                                     'Authorization': 'Bearer '
                                     + self.test_user_candidate})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    Vacancy
    '''
    def test_add_new_vacancy(self):
        '''Tests successful request to post a new vacancy into the database'''
        res = self.client().post('/vacancies', json=self.new_vacancy,
                                 headers={
                                     'Authorization': 'Bearer '
                                     + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_404_not_found_when_add_new_vacancy(self):
        '''Tests error 404 for incorrect route'''
        res = self.client().post('/vacancy', json=self.new_vacancy,
                                 headers={
                                     'Authorization': 'Bearer '
                                     + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    Application
    '''
    def test_add_new_application(self):
        '''Tests successful request to post
        a new candidate application by vacancy id'''
        res = self.client().post('/vacancies/1/applications',
                                 json=self.new_application,
                                 headers={
                                     'Authorization': 'Bearer '
                                     + self.test_user_candidate})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_406_not_acceptable_when_post_application(self):
        '''Tests error 406 when posting a duplicate application'''
        res = self.client().post('/vacancies/1/applications',
                                 json=self.new_application,
                                 headers={
                                     'Authorization': 'Bearer '
                                     + self.test_user_candidate})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 406)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not acceptable')

    '''
    GET
    '''
    '''
    Company
    '''

    def test_get_companies(self):
        '''Tests successful request to get companies'''
        res = self.client().get('/companies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['companies'])

    def test_error_404_not_found_when_get_companies(self):
        '''Test error 404 when get companies for incorrect route'''
        res = self.client().get('/company')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_get_company_by_id(self):
        '''Tests successful request to get company by id'''
        res = self.client().get('/companies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['company'])

    def test_error_404_not_found_when_get_company_by_id(self):
        '''Tests error 404 when id is not valid'''
        res = self.client().get('/companies/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    Candidate
    '''
    def test_get_candidate_by_id(self):
        '''Tests successful request to get a candidate by id'''
        res = self.client().get('/candidates/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['candidate'])

    def test_error_404_not_found_when_get_candidate_by_id(self):
        '''Tests error 404 when id is not valid'''
        res = self.client().get('/candidates/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    Vacancy
    '''
    def test_get_vacancies(self):
        '''Tests successful request to get vacancies'''
        res = self.client().get('/vacancies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['vacancies'])

    def test_error_404_not_found_when_get_vacancies(self):
        '''Test error 400 when get vacancies with incorrect route'''
        res = self.client().get('/vacancy')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_get_vacancy_by_id(self):
        '''Tests successful request to get a vacancy by id'''
        res = self.client().get('/vacancies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['vacancy'])

    def test_error_404_not_found_when_get_vacancy_by_id(self):
        '''Tests error 404 when id is not valid'''
        res = self.client().get('/vacancies/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    Application
    '''
    def test_get_applications_by_candidate_id(self):
        '''Tests successful request for applications by candidate id'''
        res = self.client().get('/candidates/1/applications',
                                headers={
                                    'Authorization': 'Bearer '
                                    + self.test_user_candidate})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_404_not_found_when_get_applications_by_candidate_id(self):
        '''Tests error 404 when getting applications by invalid candidate id'''
        res = self.client().get('/candidates/1000/applications',
                                headers={
                                    'Authorization': 'Bearer '
                                    + self.test_user_candidate})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_get_applications_by_vacancy_id(self):
        '''Tests successful request of applications by vacancy id'''
        res = self.client().get('/vacancies/1/applications',
                                headers={
                                    'Authorization': 'Bearer '
                                    + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_404_not_found_when_get_applications_by_vacancy_id(self):
        '''Tests error 404 when getting applications by invalid vacancy id'''
        res = self.client().get('/vacancies/1000/applications',
                                headers={
                                    'Authorization': 'Bearer '
                                    + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    UPDATE
    '''
    '''
    Company
    '''

    def test_update_company_by_id(self):
        '''Tests successful update of company information by id'''
        res = self.client().patch('/companies/1', json=self.edit_company,
                                  headers={
                                      'Authorization': 'Bearer '
                                      + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    def test_error_404_not_found_when_update_company(self):
        '''Test error 404 when trying to edit inexisting company id'''
        res = self.client().patch('/companies/1000', json=self.edit_company,
                                  headers={
                                      'Authorization': 'Bearer '
                                      + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    Candidate
    '''
    def test_update_candidate_by_id(self):
        '''Tests successful update of a candidate information by id'''
        res = self.client().patch('/candidates/1', json=self.edit_candidate,
                                  headers={
                                      'Authorization': 'Bearer '
                                      + self.test_user_candidate})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    def test_error_422_unprocessable_when_update_candidate(self):
        '''Test error 422 when trying to edit inexisting candidate id'''
        res = self.client().patch('/candidates/1000', json=self.edit_candidate,
                                  headers={
                                      'Authorization': 'Bearer '
                                      + self.test_user_candidate})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    '''
    Vacancy
    '''
    def test_update_vacancy_by_id(self):
        '''Tests successful update of a vacancy information by id'''
        res = self.client().patch('/vacancies/1', json=self.edit_vacancy,
                                  headers={
                                      'Authorization': 'Bearer '
                                      + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    def test_error_422_unprocessable_when_update_vacancy(self):
        '''Test error 422 when vacancy id is not valid'''
        res = self.client().patch('/vacancies/1000', json=self.edit_vacancy,
                                  headers={
                                      'Authorization': 'Bearer '
                                      + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    '''
    DELETE
    '''
    '''
    Application
    '''

    def test_delete_application(self):
        '''Tests successful deleting of an application'''
        res = self.client().delete('/applications/1',
                                   headers={
                                       'Authorization': 'Bearer '
                                       + self.test_user_candidate})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    def test_error_422_when_deleting_application(self):
        '''Tests error 422 when deleting application
        by invalid application id'''
        res = self.client().delete('/applications/1000',
                                   headers={
                                       'Authorization': 'Bearer '
                                       + self.test_user_candidate})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    '''
    Vacancy
    '''
    def test_delete_vacancy_by_id(self):
        '''Tests successful deleting of a vacancy by id'''
        res = self.client().delete('/vacancies/1',
                                   headers={
                                       'Authorization': 'Bearer '
                                       + self.test_user_company})
        data = json.loads(res.data)
        vacancy = Vacancy.query.filter(Vacancy.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)
        self.assertIsNone(vacancy)

    def test_error_422_unprocessable_when_delete_vacancy(self):
        '''Tests error 422 when vacancy id does not exist'''
        res = self.client().delete('/vacancies/1000',
                                   headers={
                                       'Authorization': 'Bearer '
                                       + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    '''
    Company
    '''
    def test_delete_company_by_id(self):
        '''Tests successful deleting of a company by id'''
        res = self.client().delete('/companies/1',
                                   headers={
                                       'Authorization': 'Bearer '
                                       + self.test_user_company})
        data = json.loads(res.data)
        company = Company.query.filter(Company.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)
        self.assertIsNone(company)

    def test_error_422_unprocessable_when_delete_company(self):
        '''Tests error 422 when company id does not exist'''
        res = self.client().delete('/companies/1000',
                                   headers={
                                       'Authorization': 'Bearer '
                                       + self.test_user_company})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    '''
    Candidate
    '''
    def test_delete_candidate_by_id(self):
        '''Tests successful deleting of a candidate profile by id'''
        res = self.client().delete('/candidates/1',
                                   headers={
                                       'Authorization': 'Bearer '
                                       + self.test_user_candidate})
        data = json.loads(res.data)
        candidate = Candidate.query.filter(Candidate.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)
        self.assertIsNone(candidate)

    def test_error_422_unprocessable_when_delete_candidate(self):
        '''Tests error 422 when candidate id does not exist'''
        res = self.client().delete('/candidates/1000',
                                   headers={
                                       'Authorization': 'Bearer '
                                       + self.test_user_candidate})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    '''
    RBAC TEST
    '''
    '''
    Company
    '''
    def test_error_401_token_not_found_company(self):
        '''Tests error 401 when token is not provided for company user'''
        res = self.client().post('/companies', json=self.new_company,
                                 headers={'Authorization': 'Bearer'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_header')
        self.assertEqual(data['description'], 'Token not found.')

    def test_error_401_no_authorization_header_company(self):
        '''Tests error 401 when authorization
        header is missing for company user'''
        res = self.client().post('/companies', json=self.new_company)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'],
                         'Authorization header is expected.')

    '''
    Candidate
    '''
    def test_error_401_token_not_found_candidate(self):
        '''Tests error 401 when token is not provided for candidate user'''
        res = self.client().post('/candidates', json=self.new_candidate,
                                 headers={'Authorization': 'Bearer'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_header')
        self.assertEqual(data['description'], 'Token not found.')

    def test_error_401_no_authorization_header_candidate(self):
        '''Tests error 401 when authorization header
        is missing for candidate user'''
        res = self.client().post('/candidates',
                                 json=self.new_candidate)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'],
                         'Authorization header is expected.')


def suite():
    '''The suite allows to customize order of execution of test cases because
    some of them depend on specific state in the database.'''
    suite = unittest.TestSuite()
    suite.addTest(JobPortalTestCase('test_add_new_company'))
    suite.addTest(JobPortalTestCase(
        'test_error_404_not_found_when_add_company'))
    suite.addTest(JobPortalTestCase('test_add_new_candidate'))
    suite.addTest(JobPortalTestCase(
        'test_error_404_not_found_add_new_candidate'))
    suite.addTest(JobPortalTestCase('test_add_new_vacancy'))
    suite.addTest(JobPortalTestCase(
        'test_error_404_not_found_when_add_new_vacancy'))
    suite.addTest(JobPortalTestCase('test_add_new_application'))
    suite.addTest(JobPortalTestCase(
        'test_error_406_not_acceptable_when_post_application'))
    suite.addTest(JobPortalTestCase('test_get_companies'))
    suite.addTest(JobPortalTestCase(
        'test_error_404_not_found_when_get_companies'))
    suite.addTest(JobPortalTestCase('test_get_company_by_id'))
    suite.addTest(JobPortalTestCase(
        'test_error_404_not_found_when_get_company_by_id'))
    suite.addTest(JobPortalTestCase('test_get_candidate_by_id'))
    suite.addTest(JobPortalTestCase(
        'test_error_404_not_found_when_get_candidate_by_id'))
    suite.addTest(JobPortalTestCase('test_get_vacancies'))
    suite.addTest(JobPortalTestCase(
        'test_error_404_not_found_when_get_vacancies'))
    suite.addTest(JobPortalTestCase('test_get_vacancy_by_id'))
    suite.addTest(JobPortalTestCase(
        'test_error_404_not_found_when_get_vacancy_by_id'))
    suite.addTest(JobPortalTestCase('test_get_applications_by_candidate_id'))
    suite.addTest(JobPortalTestCase(
        'test_error_404_not_found_when_get_applications_by_candidate_id'))
    suite.addTest(JobPortalTestCase('test_get_applications_by_vacancy_id'))
    suite.addTest(JobPortalTestCase(
        'test_error_404_not_found_when_get_applications_by_vacancy_id'))
    suite.addTest(JobPortalTestCase('test_update_company_by_id'))
    suite.addTest(JobPortalTestCase(
        'test_error_404_not_found_when_update_company'))
    suite.addTest(JobPortalTestCase('test_update_candidate_by_id'))
    suite.addTest(JobPortalTestCase(
        'test_error_422_unprocessable_when_update_candidate'))
    suite.addTest(JobPortalTestCase('test_update_vacancy_by_id'))
    suite.addTest(JobPortalTestCase(
        'test_error_422_unprocessable_when_update_vacancy'))
    suite.addTest(JobPortalTestCase('test_delete_application'))
    suite.addTest(JobPortalTestCase(
        'test_error_422_when_deleting_application'))
    suite.addTest(JobPortalTestCase('test_delete_vacancy_by_id'))
    suite.addTest(JobPortalTestCase(
        'test_error_422_unprocessable_when_delete_vacancy'))
    suite.addTest(JobPortalTestCase('test_delete_company_by_id'))
    suite.addTest(JobPortalTestCase(
        'test_error_422_unprocessable_when_delete_company'))
    suite.addTest(JobPortalTestCase('test_delete_candidate_by_id'))
    suite.addTest(JobPortalTestCase(
        'test_error_422_unprocessable_when_delete_candidate'))
    suite.addTest(JobPortalTestCase('test_error_401_token_not_found_company'))
    suite.addTest(JobPortalTestCase(
        'test_error_401_no_authorization_header_company'))
    suite.addTest(JobPortalTestCase(
        'test_error_401_token_not_found_candidate'))
    suite.addTest(JobPortalTestCase(
        'test_error_401_no_authorization_header_candidate'))

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
