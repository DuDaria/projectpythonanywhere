from django.contrib.auth import login, authenticate
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.views.generic import (View, ListView, 
    CreateView, DeleteView, UpdateView, DetailView
)
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (Post, Comment, Profile, 
    CategoryPost, FavoritePost, Review, Message
)
from .forms import (PostForm, CommentForm, 
    MessageForm, ReviewForm
)


def users_counter():
    users =  Profile.objects.all()
    return len(users)


def paginate(posts, request):
    paginate_by = 6
    paginator = Paginator(posts, paginate_by)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    return page, is_paginated, prev_url, next_url


class IndexView(ListView):
    posts = Post.objects.all()
    categories = CategoryPost.objects.all()
    model = Post 
    template_name = 'advito/index.html'
    context_object_name ='posts'
    users_counter = users_counter()
    text = "Зарегистрировано: "

    def get(self, request):
        search_query = self.request.GET.get('q')
        if search_query:
            posts = Post.objects.filter(
                Q(name_descript__icontains=search_query) 
                | Q(description__icontains=search_query)
            )
        else:
            posts = Post.objects.all()

        page, is_paginated, prev_url, next_url = paginate(posts, request)

        context = {
            'page_object': page,
            'categories': self.categories,
            'users_counter': users_counter,
            'text': self.text,
            'is_paginated': is_paginated,
            'prev_url': prev_url,
            'next_url': next_url,
        }

        return render(request, self.template_name, context)


def support(request):
    template_name = 'advito/support.html'
    return render(request, template_name)


class PostDetailView(DetailView):
    categories = CategoryPost.objects.all()
    extra_context = {'categories':categories, }
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'advito/post_detail.html'
    comment_form_class = CommentForm
    context={}
    
    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        profile = Profile.objects.get(user=self.object.author)
        context = self.get_context_data(object=self.object)
        context['profile'] = profile
        context['comments'] = Comment.objects.filter(in_post__id=post_id).order_by('-date_publish')

        if request.user.is_authenticated:
            context['comment_form'] = self.comment_form_class()

        return self.render_to_response(context)
        
    @method_decorator(login_required(login_url='/advito/login/'))
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        form = self.comment_form_class(request.POST)

        if form.is_valid():
            print("Форма валидна!")
            comment = form.save(commit=False)
            comment.author = request.user
            comment.in_post = post
            comment.save()
            return redirect(request.META.get('HTTP_REFERER'), request)
        
        elif 'button_add_post' in request.POST:
            if request.user.user_profile:
                favpost_add, created = FavoritePost.objects.get_or_create(
                    post=post, 
                    author=request.user.user_profile
                )
                return redirect(request.META.get('HTTP_REFERER'), request)
        else:
            print("Форма не валидна!")
            return render(request, self.template_name, context={
                'comment_form': self.comment_form_class,
                'post': post,
                'comments': Comment.objects.filter(in_post__id=post_id).order_by('-date_publish')
            })


class PostEditView(UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'advito/post_edit.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied ("Вы не автор этого поста!!!")
        
        return super(PostEditView, self).dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        post_id = self.kwargs[self.pk_url_kwarg]
        return reverse('advito:post_detail', args=(post_id, ))


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = 'advito/post_create.html'
    
    @method_decorator(login_required(login_url='/advito/login/'))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            print("Форма валидна!")
            post_form = form.save(commit=False) 
            post_form.author = request.user 
            post_form.save()
            post_new_id = post_form.id
            post_new = Post.objects.get(id=post_new_id)
            context['post_was_created'] = True
            context['post_new'] = post_new
        else:
            print("Форма не валидна")
            context['post_with_errors'] = True
            context['form'] = form
        
        return render(request, self.template_name, context)


class PostDeleteView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'advito/post_delete.html'

    # переопределим метод (получение ссылки advito:post_delete_success)
    def get_success_url(self):
        post_id = self.kwargs[self.pk_url_kwarg]
        return reverse('advito:post_delete_success', args=(post_id, ))


class FavoritePostView(ListView):
    model = FavoritePost
    post_form_class = PostForm
    categories = CategoryPost.objects.all()
    template_name = 'advito/favorite_post.html'
    context_object_name ='add_posts'
    extra_context = {'categories':categories, }
    context = {}

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(
                post__date_pub__year=2021, 
                author=self.request.user.user_profile
            ).order_by('-post__date_pub')[:15]
        else:
            return []

    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        if 'button_dell_post' in request.POST:
            if request.user.user_profile:
                fav_post_delete = Post.objects.get(pk=post_id)
                FavoritePost.objects.filter(post=fav_post_delete).delete()

        return redirect(request.META.get('HTTP_REFERER'), request)


def category_post(request, category_id):
    counter = users_counter()
    posts = Post.objects.filter(category=category_id, date_pub__year=2021)
    categories= CategoryPost.objects.all()
    template_name = 'advito/index.html'
    text = "Зарегистрировано: "
    page, is_paginated, prev_url, next_url = paginate(posts, request)
    
    context = {
        'page_object': page,
        'categories': categories,
        'text': text,
        'users_counter': counter,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
    }
    
    return render(request, template_name, context)


class PostCreateMessageView(CreateView):
    model = Post
    pk_url_kwarg = 'post_id'
    categories = CategoryPost.objects.all()
    extra_context = {'categories':categories, }
    form_class = MessageForm
    template_name = 'advito/post_message.html'
    object = None

    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['name_descript'] = self.object.name_descript
        if request.user.is_authenticated:
            context['message_form'] = self.form_class()

        message_id = kwargs.get('message_id', None)
        if not message_id:
            context['author'] = self.object.author
        else:
            message = get_object_or_404(Message, id=message_id)
            context['author'] = message.author

        return self.render_to_response(context)

    @method_decorator(login_required(login_url='/advito/login/'))
    def post(self, request, post_id, message_id=None, *args, **kwargs):
        form = self.form_class(request.POST)
        self.object = self.get_object()
        context = {}
        
        if form.is_valid():
            print("Форма валидна!")
            message = form.save(commit=False)
            message.in_post = self.object
            message.author = request.user.user_profile

            if not message_id:
                message.to_whom = self.object.author
            else:
                replied_message = get_object_or_404(Message, pk=message_id)
                message.to_whom = replied_message.author.user

            message.save()
            context['author'] = self.object.author
            context['message_was_created'] = True
        else:
            print("Форма не валидна")
            context['message_with_errors'] = True
            context['form'] = form
        
        return render(request, self.template_name, context)


class ReviewCreateView(CreateView):
    review_form_class = ReviewForm
    model = Post 
    pk_url_kwarg = 'post_id'
    categories = CategoryPost.objects.all()
    template_name = 'advito/review.html'
    context = {}

    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        reviews = Review.objects.filter(to_whom=self.object.author).order_by('-date_pub')

        self.context['reviews'] = reviews
        self.context['author'] = self.object.author
        self.context['categories'] = self.categories

        if request.user.is_authenticated:
            self.context['review_form'] = self.review_form_class()

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.review_form_class(request.POST)
        self.object = self.get_object()
        rating = request.POST.get('rating')

        if form.is_valid():
            print("Форма валидна!")
            review = form.save(commit=False)
            review.to_whom_id = self.object.author.id
            review.author_id = request.user.user_profile.id
            review.rating = rating
            review.save()
            return redirect(request.META.get('HTTP_REFERER'), request)
        else:
            print("Форма не валидна!")
            return render(request, self.template_name, context={
                'review_form': self.review_form_class,
                'reviews': Review.objects.filter(to_whom=self.object.author).order_by('-date_pub')
            })      
        