# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, UserUpdateForm, BioUpdateForm
from .models import CustomUser, UserProfile

class SignupTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:signup')
        self.form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        Group.objects.create(name='Customer')

    def test_getSignupView(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertContains(response, '<h1 class="my_title text-center pt-4 pb-3">Create a new account</h1>')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_postSignupViewPass(self):
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1 class="my_title text-center">Your account has been successfully created</h1>')
        user = get_user_model().objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword'))

    def test_postSignupViewInvalid(self):
        self.form_data['password2'] = 'wrongpassword'
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1 class="my_title text-center pt-4 pb-3">Create a new account</h1>')
        self.assertFalse(get_user_model().objects.exists())
       

class SignInTestCase(TestCase):
    def setUp(self):
        self.url = reverse('accounts:signin')
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )

    def test_getSigninView(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')
        self.assertContains(response, '<h1 class="my_title text-center pt-4 pb-5">Login to your account</h1>')


    def test_signinPass(self):
        url = reverse('accounts:signin')
        data = {
            'username': 'testuser',
            'password': 'password',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('main:home')) 
        self.assertTrue(response.wsgi_request.user.is_authenticated) 

    def test_signinFail(self):
        url = reverse('accounts:signin')
        data = {
            'username': 'testuser',
            'password': 'password1',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1 class="my_title text-center pt-4 pb-5">Login to your account</h1>')
        self.assertFalse(response.wsgi_request.user.is_authenticated) 


class SignOutTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', 
            email='testuser@example.com',
            password='password'
        )  
    
     
    def test_signout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('accounts:signout'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('accounts:signin'))
        self.assertContains(response, '<h1 class="my_title text-center pt-4 pb-5">Login to your account</h1>')

class ProfileTestCase(TestCase):
    def setUp(self):
        
        self.user = get_user_model().objects.create_user(
            username='testuser', 
            email='testuser@example.com',
            password='password'
        )
        self.url = reverse('accounts:profile', args=[self.user.username])
        

    def test_ProfileView(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, '<h2>'+self.user.username+'</h2>')
        self.assertIsInstance(response.context['bioform'], BioUpdateForm)

    def test_profileViewBioUpdate(self):
        new_bio = 'New Test Bio'
        form_data = {'bio': new_bio}
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:profile', args=[self.user.username]))
        self.assertEqual(UserProfile.objects.get(user=self.user).bio, new_bio)


class ProfileDetailsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile_name = 'testuser'
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password',
            email='testuser@example.com'
        )
        self.url = reverse('accounts:profileDetails', args=[self.profile_name])
        self.client.login(username='testuser', password='password')

    def test_ProfioeDetailsViewPass(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profileDetails.html')
        self.assertIsInstance(response.context['u_form'], UserUpdateForm)

    def test_ProfioeDetailsViewFail(self):
        self.client.logout()
        user2 = get_user_model().objects.create_user(
            username='testuser2',
            password='password',
            email='testuser2@example.com'
        )
        self.client.login(username='testuser2', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_edit_profile_with_valid_data(self):
        data = {
            'username': 'Test',
            'email': 'testuser@example.ie', 
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:profile', args=['Test']))
        user = get_user_model().objects.get(username='Test')
        self.assertEqual(user.username, 'Test')
        self.assertEqual(user.email, 'testuser@example.ie')
 

        