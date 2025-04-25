from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestAllAuthUrls(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "testuser"
        cls.email = "testuser@zenhn.com"
        cls.sign_up_url = reverse("account_signup")
        cls.login_url = reverse("account_login")
        cls.logout_url = reverse("account_logout")
        cls.home_url = reverse("home")
        cls.password = "testpass123"
        cls.User = get_user_model()
        cls.user_dict = {"username": "testuser2", "email": "testuser2@zenhn.com", "password": cls.password}
        cls.user = cls.User.objects.create_user(**cls.user_dict)

    def test_sign_up_url(self):
        res = self.client.get(self.sign_up_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "account/signup.html")
        self.assertContains(res, "Sign Up")
        res = self.client.post(self.sign_up_url,
                               data={"email": self.email, "username":self.username, "password1": self.password,
                                     "password2": self.password}
                               )
        self.assertEqual(res.status_code, 302)
        new_user = self.User.objects.get(email=self.email)
        self.assertEqual(new_user.email, self.email)

    def test_login_url(self):
        res = self.client.get(self.login_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "account/login.html")
        self.assertContains(res, "Login")
        data = {"email": self.user_dict["email"], "password": self.password}
        res = self.client.login(**data)
        self.assertTrue(res)

    def test_logout(self):
        data = {"email": self.user_dict["email"], "password": self.password}
        login = self.client.login(**data)
        self.assertTrue(login)
        res = self.client.get(self.home_url)
        self.assertNotContains(res, "Login")
        self.assertContains(res, "Logout")
        res = self.client.get(self.logout_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "account/logout.html")
        self.assertContains(res, "Logout")
        self.client.logout()
        res = self.client.get(self.home_url)
        self.assertNotContains(res, "Logout")
        self.assertContains(res, "Login")
