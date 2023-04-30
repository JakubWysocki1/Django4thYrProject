from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from forum.models import ForumCategory, ForumPost
from forum.forms import ForumPostForm



# Create your tests here.
class ForumTopicsTest(TestCase):
    def setUp(self):
        self.url = reverse('forum:forumtopics')
        self.category1 = ForumCategory.objects.create(name='Category 1', description='Category 1 description')
        self.category2 = ForumCategory.objects.create(name='Category 2', description='Category 2 description')

    def test_ForumTopics(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forumtopics.html')
        self.assertContains(response, self.category1.name)
        self.assertContains(response, self.category2.name)


class CategoryPosts(TestCase):
    def setUp(self):
        self.category = ForumCategory.objects.create(name='Test Category')
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.post = ForumPost.objects.create(category=self.category, user=self.user, title='Test Post', body='Test Content')
        self.url = reverse('forum:categoryposts', args=[self.category.name])
        self.client.login(username='testuser', password='testpassword')
        self.form_data = {
            'title': 'New Post',
            'body': 'New Content',
        }

    def test_CategoryPostsValid(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categoryposts.html')
        self.assertEqual(response.context['category_name'], self.category.name)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)

    def test_CategoryPostsInvalid(self):
        url = reverse('forum:categoryposts', args=['invalid_category'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categoryposts.html')
        self.assertContains(response, 'Category does not exist')
    


class PostViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.category = ForumCategory.objects.create(name='Test Category')
        self.post = ForumPost.objects.create(category=self.category, user=self.user, title='Test Post', body='Test Content')

    
    def test_valid_post(self):
        response = self.client.get(reverse('forum:post', args=[self.category.name, self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post.html')
        self.assertEqual(response.context['post'], self.post)
        self.assertEqual(response.context['category_name'], self.category.name)
    
    def test_invalid_post(self):
        response = self.client.get(reverse('forum:post', args=[self.category.name, 999]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post.html')
        self.assertContains(response, 'Post ID or category does not exist')