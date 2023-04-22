"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from .forms import FeedbackForm, CommentForm, ArticleForm
from .models import Blog, Comment


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': u'Главная',
            'year':datetime.now().year,
        }
    )


def videopost(request):
    return render(
        request,
        "app/videopost.html",
        {
            "title": "Видео",
            "year": datetime.now().year,
        },
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': u'О козерогах',
            'year':datetime.now().year,
        }
    )


def more(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title': u'Полезные источники',
            'year': datetime.now().year,
        }
    )


def pool(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {
        '1': 'Мужчина',
        '2': 'Женщина',
    }
    rate = {
        '1': 'Плохо',
        '2': 'Нормально',
        '3': 'Отлично',
    }

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = {}
            data['username'] = form.cleaned_data['username']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['corn'] = 'Да' if form.cleaned_data['corn'] else 'Нет'
            data['rate'] = rate[form.cleaned_data['rate']]
            data['feedback'] = form.cleaned_data['feedback']
            form = None
    else:
        form = FeedbackForm()

    return render(
        request,
        'app/pool.html',
        {
            'title': u'Обратная связь',
            'form': form,
            'data': data,
        }
    )


def registration(request):
    """Renders the registration page."""

    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()

            regform.save()

            return redirect('home')
    else:
        regform = UserCreationForm()

        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/registration.html',
            {
                'title': u'Регистрация',
                'regform': regform,
                'year': datetime.now().year,
            }
        )


def newpost(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.posted = datetime.now()
            article.save()
            return redirect("home")
    else:
        form = ArticleForm()

    return render(
        request,
        "app/newpost.html",
        {
            "title": "Добавить статью блога",
            "articleForm": form,
            "year": datetime.now().year,
        },
    )


def blog(request):
    posts = Blog.objects.all()
    return render(
        request,
        "app/blog.html",
        {
            "title": "Блог",
            "posts": posts,
            "year": datetime.now().year,
        },
    )


def article(request, parametr):
    post = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.date = datetime.now()
            comment.post = Blog.objects.get(id=parametr)
            comment.save()
            return redirect("article", parametr=post.id)
    else:
        form = CommentForm()

    return render(
        request,
        "app/article.html",
        {
            "title": post.title,
            "post": post,
            "comments": comments,
            "form": form,
            "year": datetime.now().year,
        },
    )
