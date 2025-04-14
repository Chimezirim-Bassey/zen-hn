from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView as _LogoutView
from django.views.generic.edit import UpdateView, CreateView
from .forms import CreateUserForm
from .models import User
from base.scripts.get_images import pick_random_image
from base.utils import BreadCrumb


class LogoutView(_LogoutView):
    http_method_names = _LogoutView.http_method_names + ['get']


class UserCreateView(CreateView):
    template_name = 'registration/signup.html'

    # CreateUserForm, a subclass of in-built UserCreationForm, effectively handles user creation
    form_class = CreateUserForm
    model = User # this must be specified, even though the form class is a model form
    success_url = reverse_lazy('login')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    login_url = reverse_lazy('account_login')
    success_url = reverse_lazy('user_profile')
    fields = ("about", "avatar", "profile_picture")
    template_name = 'user_account/user_update_form.html'

    def get_object(self, queryset=None):
        # if the user is not authenticated, redirect to login page
        if not self.request.user.is_authenticated:
            return reverse_lazy('account_login')
        self.kwargs.update(pk=self.request.user.username)
        return super().get_object(queryset=queryset)

    def test_func(self):
        return self.request.user == self.get_object()

    # def get_success_url(self):
    #     return reverse_lazy('profile', kwargs={'slug': self.object.username})


class UserDetailView(DetailView):
    model = User
    template_name = 'user_account/profile.html'
    context_object_name = 'me'
    slug_field = "username"
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated and not self.kwargs.get(self.slug_url_kwarg):
            self.kwargs.update(pk=self.request.user.username)
        return super().get_object(queryset=queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # alls = self.object.stories.all().order_by('created')
        # rated = self.object.stories.order_by('-score')[0]
        context["breadcrumbs"] = [BreadCrumb(name="Home", url=reverse_lazy('home'))]
        context["title"] = "Profile"
        context["person"] = pick_random_image('persons')
        # context['rated'] = rated
        # context['count'] = len(alls)
        # context['recent'] = alls[0]
        return context
