from django.test import TestCase
from statecoin50.models import Coin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
# Create your tests here.

class TestCoin(TestCase):
    def test_coin_field_user_required_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()
        coin = Coin( state = 'Minnesota', stAbbr = 'MN', owned= 'False',
            dateOwned = '', stImg = '', dates = '', details = '')
        with self.assertRaises(ValidationError):
            coin.save()

    def test_coin_field_abbr_maxLength_limit_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()
        coin = Coin(owner = user, state = 'Minnesota', stAbbr = 'Minnesota', owned= 'False',
            dateOwned = '', stImg = '', dates = '', details = '')
        with self.assertRaises(ValidationError):
            coin.save()
