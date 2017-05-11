from django.test import TestCase
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from statecoin50.forms import CoinDetailForm, CoinCollectorForm, UserRegistrationForm

from django.contrib.auth.forms import AuthenticationForm
import string

# Test that forms are validating correctly, and don't accept invalid data



class RegistrationFormTests(TestCase):

    def test_register_user_with_valid_data_is_valid(self):
        form_data = { 'username' : 'bob' , 'email' : 'bob@bob.com', 'first_name' : 'bob', 'last_name' : 'whatever', 'password1' : 'qwertyuiop', 'password2' : 'qwertyuiop' }
        form = UserRegistrationForm(form_data)
        self.assertTrue(form.is_valid())


    def test_register_user_with_missing_data_fails(self):
        form_data = { 'username': 'bob', 'email' : 'bob@bob.com', 'first_name' : 'bob', 'last_name' : 'whatever', 'password1' : 'qwertyuiop', 'password2' : 'qwertyuiop' }
        # Remove each key-value from dictionary, assert form not valid
        for field in form_data.keys():
            data = dict(form_data)
            del(data[field])
            form = UserRegistrationForm(data)
            self.assertFalse(form.is_valid())


    def test_register_user_with_password_mismatch_fails(self):
        form_data = { 'username' : 'another_bob' , 'email' : 'bob@bob.com', 'first_name' : 'bob', 'last_name' : 'whatever', 'password1' : 'qwertyuiop', 'password2' : 'qwertyuiop2' }
        form = UserRegistrationForm(form_data)
        self.assertFalse(form.is_valid())


    def test_register_user_with_email_already_in_db_fails(self):

        # Create a user with email bob@bob.com
        bob = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        bob.save()

        # attempt to create another user with same email
        form_data = { 'username' : 'another_bob' , 'email' : 'bob@bob.com', 'first_name' : 'bob', 'last_name' : 'whatever', 'password1' : 'qwertyuiop', 'password2' : 'qwertyuiop' }
        form = UserRegistrationForm(form_data)
        self.assertFalse(form.is_valid())


    def test_register_user_with_username_already_in_db_fails(self):

        # Create a user with username bob
        bob = User(username='bob', email='bob@bob.com')
        bob.save()

        # attempt to create another user with same username
        form_data = { 'username' : 'bob' , 'email' : 'another_bob@bob.com', 'first_name' : 'bob', 'last_name' : 'whatever', 'password1' : 'qwertyuiop', 'password2' : 'qwertyuiop' }
        form = UserRegistrationForm(form_data)
        self.assertFalse(form.is_valid())


#resource reference http://stackoverflow.com/questions/22457557/how-to-test-login-process
class LoginFormTests(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'sally',
            'password': 'qwertyuiop'}
        User.objects.create_user(**self.credentials)
    def test_login_valid_username_password_ok(self):
        user = authenticate(username='sally', password='qwertyuiop')

        print(user)
        self.assertTrue(user is not None)

    def test_login_invalid_username(self):
        user = authenticate(username='bob', password='qwertyuiop')
        self.assertFalse(user is not None)

    def test_login_invalid_password(self):
        user = authenticate(username='sally', password='qwertyuiop2')
        self.assertFalse(user is not None)
