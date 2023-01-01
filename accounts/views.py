from django.contrib import messages
from django.contrib.auth import views as auth_views, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("top")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.add_message(self.request, messages.SUCCESS, "会員登録に成功しました。")
        self.object = user
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "会員登録に失敗しました。")
        return super().form_invalid(form)


signup = SignupView.as_view()


class LoginView(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "accounts/login.html"


login = LoginView.as_view()
