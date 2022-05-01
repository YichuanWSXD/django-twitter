from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'


class AccountApiTests(TestCase):

    def setUp(self):
        # this function will be running when test function executes
        self.client = APIClient()
        self.user = self.createUser(
            username='admin',
            email='admin@wsxd.com',
            password='correct password',
        )

    def createUser(self, username, email, password):
        # Should not be User.objects.create() since password needs to be encrypted
        return User.objects.create_user(username, email, password)

    def test_login(self):
        # tests need to be started with test_
        # tests should utilize post method
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password'
        })
        # if failed, return status 405 = METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, 405)

        # password is incorrect
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password'
        })
        # if failed, return status 405 = METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, 400)

        # hasn't logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)
        # login with correct password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password'
        })
        # if failed, return status 405 = METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], 'admin@wsxd.com')

        # Test login status
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)


    def test_logout(self):
        # first login
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password'
        })
        # ensure the status is logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        # GET method fails
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        # POST method
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)

        # ensure the status is logged out
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

    def test_signup(self):
        data = {
            'username': 'someone',
            'email': 'someone@wsxd.com',
            'password': 'any password'}
        # Test GET
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # Use incorrect email format
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'not a correct email',
            'password': 'any password'
        })
        self.assertEqual(response.status_code, 400)

        # Password is too short
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'someone@wsxd.com',
            'password': '123'
        })
        self.assertEqual(response.status_code, 400)

        # username is too long
        response = self.client.post(SIGNUP_URL, {
            'username': 'username is tooooooooooooooooooooooooooooooooo loooooooooooooooooong',
            'email': 'someone@wsxd.com',
            'password': 'any password'
        })
        self.assertEqual(response.status_code, 400)

        # success
        response = self.client.post(SIGNUP_URL, data)
        # print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'someone')

        # automatic login
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)