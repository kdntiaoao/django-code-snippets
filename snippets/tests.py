from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import resolve

from snippets.models import Snippet
from snippets.views import top, snippet_new, snippet_edit

UserModel = get_user_model()


class TopPageTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test", email="test@example.com", password="top_secret_pass01"
        )
        self.snippet = Snippet.objects.create(
            title="タイトル", code="print('hello')", description="説明", created_by=self.user
        )

    def test_should_return_snippet_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.snippet.title)

    def test_should_return_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)


class TopPageTestWithNoSnippet:
    def test_should_return_no_snippet(self):
        request = RequestFactory().get("/")
        response = top(request)
        self.assertContains(response, "スニペットはまだ投稿されていません。")


class CreateSnippetTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test", email="test@example.com", password="top_secret_pass01"
        )
        self.client.force_login(self.user)  # ログイン

    def test_render_creation_form(self):
        response = self.client.get("/snippets/new/")
        self.assertContains(response, "スニペットの登録", status_code=200)

    def test_create_snippet(self):
        data = {"title": "タイトル", "code": "コード", "description": "解説"}
        self.client.post("/snippets/new/", data)
        snippet = Snippet.objects.get(title="タイトル")
        self.assertEqual(snippet.code, "コード")
        self.assertEqual(snippet.description, "解説")


class SnippetDetailTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test", email="test@example.com", password="top_secret_pass01"
        )
        self.snippet = Snippet.objects.create(
            title="タイトル", code="print('hello')", description="説明", created_by=self.user
        )

    def test_should_use_expected_template(self):
        response = self.client.get(f"/snippets/{self.snippet.id}/")
        self.assertTemplateUsed(response, "snippets/detail.html")

    def test_detail_page_returns_200_and_expected_heading(self):
        response = self.client.get(f"/snippets/{self.snippet.id}/")
        self.assertContains(response, self.snippet.title, status_code=200)


class EditSnippetTest(TestCase):
    def test_should_resolve_snippet_edit(self):
        found = resolve("/snippets/1/edit/")
        self.assertEqual(snippet_edit, found.func)
