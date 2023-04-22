"""
Definition of urls for laba4.
"""

from datetime import datetime
from xml.etree.ElementInclude import include
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from app import forms, views
admin.autodiscover()

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    re_path(r'^(?P<parametr>\d+)/$', views.article, name='article'),
    path('about/', views.about, name='about'),
    path('more/', views.more, name='more'),
    path('videopost/', views.videopost, name='videopost'),
    path('newpost/', views.newpost, name='newpost'),
    path('pool/', views.pool, name='pool'),
    path('registration/', views.registration, name='registration'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': u'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
