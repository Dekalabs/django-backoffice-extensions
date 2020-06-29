from django.contrib.auth import get_user_model
from test_plus import TestCase

from tests.factories import UserFactory, StuffFactory


User = get_user_model()


class BackofficeTestCase(TestCase):
    user_factory = UserFactory

    def setUp(self):
        self.user = self.make_user()

    def test_get_index(self):
        with self.login(self.user):
            self.get("backoffice:index")
        self.response_200()

    def test_get_sign_in(self):
        self.get("backoffice:sign-in")
        self.response_200()

    def test_post_sign_in(self):
        username = "dummy"
        password = "p0t4t0"
        user = UserFactory(username=username)
        user.set_password(password)
        user.save()
        data = {"username": username, "password": password}
        self.post("backoffice:sign-in", data=data)
        self.response_302()

    def test_get_sign_pot(self):
        with self.login(self.user):
            self.get("backoffice:sign-out")
        self.response_302()

    def test_get_users_list(self):
        UserFactory.create_batch(size=20)
        with self.login(self.user):
            self.get("backoffice:user-list")
        self.response_200()

    def test_get_user_create(self):
        with self.login(self.user):
            self.get("backoffice:user-create")
        self.response_200()

    def test_post_user_create(self):
        data = {"username": "dummy", "password": "p0t4t0"}
        with self.login(self.user):
            self.post("backoffice:user-create", data=data)
        self.response_302()
        self.assertEqual(2, User.objects.count())

    def test_get_user_edit(self):
        user = UserFactory()
        with self.login(self.user):
            self.get("backoffice:user-edit", pk=user.pk)
        self.response_200()

    def test_post_user_edit(self):
        user = UserFactory(username="old")
        data = {"username": "dummy"}
        with self.login(self.user):
            self.post("backoffice:user-edit", pk=user.pk, data=data)
        self.response_302()
        user.refresh_from_db()
        self.assertEqual(data["username"], user.username)

    def test_get_export_users(self):
        UserFactory.create_batch(size=20)
        with self.login(self.user):
            self.get("backoffice:user-export")
        self.response_200()

    def test_get_stuffs_list(self):
        StuffFactory.create_batch(size=20)
        with self.login(self.user):
            self.get("backoffice:stuff-list")
        self.response_200()

    def test_get_stuffs_detail(self):
        stuff = StuffFactory()
        with self.login(self.user):
            self.get("backoffice:stuff-detail", pk=stuff.pk)
        self.response_200()
