from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class SaveDateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_save_date_successfully(self):
        data = {'date': '2023-03-07'}
        response = self.client.post('/login/home/overview/save_date/', data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})

    def test_save_date_with_invalid_data(self):
        data = {'date': 'invalid-date-format'}
        response = self.client.post('/login/home/overview/save_date/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SaveSpeedViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_save_speed_successfully(self):
        data = {'speed': 6.1000000000000005}
        response = self.client.post('/login/home/overview/save_speed/', data, format='json' ,follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})

    def test_save_speed_with_invalid_data(self):
        data = {'speed': 'not-a-number'}
        response = self.client.post('/login/home/overview/save_speed/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
