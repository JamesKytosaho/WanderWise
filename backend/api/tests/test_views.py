from django.test import TestCase, RequestFactory
from unittest.mock import patch, Mock
from rest_framework import status
from api.views import suggestion

class TestSuggestionView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('api.views.service_locator.get_service')
    def test_suggestion_success(self, mock_get_service):
        # Arrange
        mock_response = Mock()
        mock_response.prompt = "Test prompt"
        mock_response.content = "Test content"
        mock_response.role = "Test role"
        mock_response.model_used = "Test model"
        
        mock_trips_service = Mock()
        mock_trips_service.get_suggestion.return_value = mock_response
        
        mock_get_service.return_value = mock_trips_service

        request = self.factory.get('/suggestion')

        # Act
        response = suggestion(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_trips_service.get_suggestion.assert_called_once()

    @patch('api.views.service_locator.get_service')
    def test_suggestion_error(self, mock_get_service):
        # Arrange
        mock_get_service.side_effect = Exception("Mocked Exception")

        request = self.factory.get('/suggestion')

        # Act
        response = suggestion(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @patch('api.views.service_locator.get_service')
    def test_suggestion_error_from_service(self, mock_get_service):
        # Arrange
        mock_trips_service = Mock()
        mock_trips_service.get_suggestion.side_effect = Exception("Mocked Exception")
        mock_get_service.return_value = mock_trips_service

        request = self.factory.get('/suggestion')

        # Act
        response = suggestion(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)