from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer



class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some Menu instances for testing
        Menu.objects.create(title="Pizza", price=12.99, inventory=10)
        Menu.objects.create(title="Burger", price=8.99, inventory=20)
        Menu.objects.create(title="Salad", price=7.99, inventory=15)

        # Get a token for a user
        user = User.objects.create_user(username='testuser', password='testpassword')
        token = Token.objects.create(user=user)

        # Set the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_getall(self):
        """Test retrieving all Menu items."""
        response = self.client.get('/restaurant/menu/')
        self.assertEqual(response.status_code, 200)

        # Serialize the expected data
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)  # many=True for serializing a queryset
        expected_data = serializer.data

        # Assert that the serialized data matches the response data
        self.assertEqual(response.data, expected_data)