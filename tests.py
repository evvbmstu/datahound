import unittest

import mock

from getters import auth


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.api = auth()

    @mock.patch('client.requests.get')
    def test_get_ok(self, mock_get):
        """
        Test getting a 200 OK response from the _get method of MyAPIClient.
        """
        # Construct our mock response object, giving it relevant expected
        # behaviours
        mock_response = mock.Mock()
        expected_dict = {
            "breeds": [
                "pembroke",
                "cardigan",
            ]
        }
        mock_response.json.return_value = expected_dict

        # Assign our mock response as the result of our patched function
        mock_get.return_value = mock_response

        url = 'http://api.corgidata.com/breeds/'
        response_dict = self.client._get(url=url)

        # Check that our function made the expected internal calls
        mock_get.assert_called_once_with(url=url)
        self.assertEqual(1, mock_response.json.call_count)

        # If we want, we can check the contents of the response
        self.assertEqual(response_dict, expected_dict)


class ViewersTestCase(unittest.TestCase):
    def setUp(self):
        self.api = auth()
    pass


class CommunityTestCase(unittest.TestCase):
    def setUp(self):
        self.api = auth()

    def counters_test(self):
        pass

    def sex_data_test(self):
        pass

    def platform_data_test(self):
        pass

    def likes_data_test(self):
        pass

    def age_data_test(self):
        pass


if __name__ == '__main__':
    pass
