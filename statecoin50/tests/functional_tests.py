from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import re, time

from django.contrib.auth.models import User


### TODO break into smaller tests; helper methods?


class HomePageTest(LiveServerTestCase):
    ''' hello selenium '''

    browser = webdriver.Firefox()
    browser.get('http://127.0.0.1:8000')
    assert 'Coin Collector' in browser.body
    browser.quit()


class ViewCoins(LiveServerTestCase):

    fixtures = ['users.json', 'coins.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()


    def test_browsing_coincollector(self):

        # Start on home page
        self.browser.get(self.live_server_url)

        # When searching for elements, wait 3 seconds for element to appear on page.
        # Needed because page load time is slower than this script's execution time.
        self.browser.implicitly_wait(3)

        # Find and click on coin's link
        state_list_link = self.browser.find_element_by_link_text('Coin.state')
        state_list_link.click()

        states = [ 'Alabama' , 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado' ]

        coin_divs = self.browser.find_elements_by_class_name('coin')

        for state, div in zip (states, coin_divs):

            # assert state name is present
            assert state in div.text

            # find a link is present with coin name - exception raised if not found
            div.find_element_by_link_text(state)
            # Find the link to view that artist's shows (which will lead to notes). Again, exception raised
            div.find_element_by_link_text('%s coindetail' % coin_pk)


        # Are we on the right page? Do this after finding elements so know page has loaded
        assert '/user/' in self.browser.current_url
