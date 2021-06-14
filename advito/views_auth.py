from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView, UpdateView, ListView
from django.http.response import Http404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms_auth import LoginForm, SignUpForm, UpdateProfileForm
from .models import Profile, Post, CategoryPost, Comment, Message


class Login(LoginView):
    template_name = 'my_auth/login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # cleaned_data - словарь
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse('advito:index'), request)
        
        return render(request, self.template_name, context={'form':form})

@login_required
def logout_views(request):
    logout(request)
    return redirect(reverse("advito:index"))


class SignUpView(View):
    template_name = 'my_auth/signup.html'
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': self.form_class()})

    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        registered = False
        context = {}
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            registered = True
        else:
            context.update({'form': form})

        context.update({'registered': registered})
        return render(request, self.template_name, context=context)


class ProfileView(DetailView):
    model = Profile
    template_name = 'my_auth/profile.html'
    
    # Метод get_object Получит объект профиля и передаст его на страницу
    def get_object(self):
        return get_object_or_404(self.model, user__id=self.kwargs['user_id'])


class UpdateProfileView(UpdateView):
    model = Profile # модель для обновления
    form_class = UpdateProfileForm
    template_name = 'my_auth/profile_update.html'
    slug_field = "user_id"
    slug_url_kwarg = "user_id"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404("It's not your profile")
        return super(UpdateProfileView, self).dispatch(request, *args, **kwargs)

    # Перенаправление пользователя после выполенния всех действий
    def get_success_url(self):
        user_id = self.kwargs['user_id']
        return reverse('advito:profile', args=(user_id, ))


def profile_posts(request, user_id):
    posts = Post.objects.filter(author_id=user_id, date_pub__year=2021).order_by('-date_pub')
    paginate_by = 6
    paginator = Paginator(posts, paginate_by)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    categories = CategoryPost.objects.all()
    template_name = 'advito/index.html'

    if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'categories': categories,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
    }
    
    return render(request, template_name, context)


class ProfileMessageView(ListView):
    model = Message
    categories = CategoryPost.objects.all()
    template_name = 'my_auth/profile_message.html'
    extra_context = {'categories':categories, }
    context = {}

    def get(self, request, *args, **kwargs):
        profile_id = request.user.user_profile.id
        if self.request.user.is_authenticated:
            messages = Message.objects.filter(
                author=profile_id, 
                date_pub__year=2021
            ).order_by('-date_pub')

            self.context['messages'] = messages
        
        return render(request, self.template_name, self.context)


class ProfileCommentView(ListView):
    model = Comment
    categories = CategoryPost.objects.all()
    template_name = 'my_auth/profile_comment.html'
    extra_context = {'categories':categories, }
    context = {}

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        if self.request.user.is_authenticated:
            comments = Comment.objects.filter(
                author_id=user_id, 
                date_publish__year=2021
            ).order_by('-date_publish')

            self.context['comments'] = comments
        
        return render(request, self.template_name, self.context)


class MessageToProfileView(ListView):
    model = Message
    categories= CategoryPost.objects.all()
    template_name = 'my_auth/message_to_profile.html'
    extra_context = {'categories':categories, }
    context = {}

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        if self.request.user.is_authenticated:
            messages = self.model.objects.filter(
                to_whom=user_id, 
                date_pub__year=2021
            ).order_by('-date_pub')
            self.context['messages'] = messages
        
        return render(request, self.template_name, self.context)
    