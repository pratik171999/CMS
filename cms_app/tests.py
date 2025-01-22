from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from cms_app.models import Category, ContentItem

User = get_user_model()

def create_dummy_pdf():
        # Create a dummy PDF file in memory
        pdf_content = io.BytesIO()
        pdf_content.write(b"%PDF-1.4\n%Dummy PDF file\n")  # This is a very basic PDF structure
        pdf_content.seek(0)  # Reset the cursor to the start of the file
        return SimpleUploadedFile("dummy.pdf", pdf_content.read(), content_type="application/pdf")

class UserRegistrationTestCase(APITestCase):
    def test_author_registration(self):
        response = self.client.post('/api/register/', {
            "email": "author@example.com",
            "username": "author",
            "password": "Author@123",
            "phone": "1234567890",
            "address": "Some Address",
            "city": "Some City",
            "state": "Some State",
            "country": "Some Country",
            "pincode": "123456"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 
                         "Author registration failed: Response code is not 201.")
        self.assertEqual(response.data['email'], "author@example.com", 
                         "Author registration failed: Email mismatch.")

    def test_admin_registration(self):
        response = self.client.post('/api/register/', {
            "email": "admin@example.com",
            "username": "admin",
            "password": "Admin@123",
            "phone": "9876543210",
            "address": "Admin Address",
            "city": "Admin City",
            "state": "Admin State",
            "country": "Admin Country",
            "pincode": "654321",
            "is_admin": True
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 
                         "Admin registration failed: Response code is not 201.")
        self.assertTrue(response.data['is_admin'], 
                        "Admin registration failed: 'is_admin' flag is not True.")
        
    def test_login(self):
        # Register the user first
        self.client.post('/api/register/', {
            "email": "author@example.com",
            "username": "author",
            "password": "Author@123",
            "phone": "1234567890",
            "address": "Some Address",
            "city": "Some City",
            "state": "Some State",
            "country": "Some Country",
            "pincode": "123456"
        }, format='json')

        # Login with the user
        response = self.client.post('/login/', {
            "email": "author@example.com",
            "password": "Author@123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # JWT token should be in the response
        return response.data['access']  # Return the token for further use
    
class ContentItemTestCase(APITestCase):

    def setUp(self):
        # Create categories
        self.category = Category.objects.create(name="Tech")

        # Register and login user
        response = self.client.post('/api/register/', {
            "email": "author@example.com",
            "username": "author",
            "password": "Author@123",
            "phone": "1234567890",
            "address": "Some Address",
            "city": "Some City",
            "state": "Some State",
            "country": "Some Country",
            "pincode": "123456"
        }, format='json')

        # Login to get the JWT token
        login_response = self.client.post('/login/', {
            "email": "author@example.com",
            "password": "Author@123"
        }, format='json')

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.token = login_response.data['access']  # Store the token for later use

    def test_create_content_item(self):
        # Prepare the data for the request (excluding the file)
        data = {
            "title": "Sample Content",
            "body": "This is a body of the content.",
            "summary": "Short summary",
            "categories": [self.category.id]  # Assign the category to the content
        }

        # Prepare the dummy PDF file
        file_data = create_dummy_pdf()

        # Use multipart format for file uploads
        response = self.client.post(
            '/api/content/',
            data={**data, 'document': file_data},  # Add the file to the data dictionary
            format='multipart',  # Specify the format to handle file uploads
            HTTP_AUTHORIZATION=f'Bearer {self.token}'  # Add the authentication token header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Sample Content")
        self.assertEqual(response.data['summary'], "Short summary")
        self.assertTrue(response.data['author'], "author@example.com")
        self.assertEqual(response.data['categories'][0], self.category.id)

    def test_create_content_item_without_title(self):
        data = {
            "body": "This is a body of the content.",
            "summary": "Short summary",
            "document": create_dummy_pdf(),  # Use the dummy PDF here
            "categories": [self.category.id]
        }

        response = self.client.post(
            '/api/content/',
            data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'  # Add the token to the headers
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

class ContentItemSearchTestCase(APITestCase):

    def setUp(self):
        # Create categories
        self.category = Category.objects.create(name="Tech")

        # Create a user and authenticate
        self.user = User.objects.create_user(
            email="author@example.com",
            username="author",
            password="Author@123",
            phone="1234567890",
            address="Some Address",
            city="Some City",
            state="Some State",
            country="Some Country",
            pincode="123456"
        )

        # Login to get the JWT token
        login_response = self.client.post('/login/', {
            "email": "author@example.com",
            "password": "Author@123"
        }, format='json')

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.token = login_response.data['access']  # Store the token for later use

        # Create sample content items and assign the author (user)
        self.content1 = ContentItem.objects.create(
            title="Sample Content 1",
            body="This is the body of the first content item.",
            summary="Summary 1",
            document=create_dummy_pdf(),
            author=self.user  # Assign the user as the author
        )
        self.content1.categories.set([self.category])

        self.content2 = ContentItem.objects.create(
            title="Sample Content 2",
            body="This is the body of the second content item.",
            summary="Summary 2",
            document=create_dummy_pdf(),
            author=self.user  # Assign the user as the author
        )
        self.content2.categories.set([self.category])

    def test_search_content_by_title(self):
        # Test search functionality by title
        response = self.client.get('/api/content/?search=Sample Content 1', 
                                   HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Add the token to the header

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Sample Content 1")

    def test_search_content_by_body(self):
        # Test search functionality by body
        response = self.client.get('/api/content/?search=second content', 
                                   HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Add the token to the header

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Sample Content 2")

    def test_search_content_with_no_results(self):
        # Test search with no results
        response = self.client.get('/api/content/?search=nonexistent', 
                                   HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Add the token to the header

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should return an empty list
