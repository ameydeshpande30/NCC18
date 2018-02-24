"""CTD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from NCC import views

views.set()
views.addsTime()
urlpatterns = [

    url(r'^coding',views.coding),
    url(r'^result',views.log_out),
    url(r'^questionhub',views.questionhub),
    url(r'^mysub',views.MySubmissions),
    url(r'^lbf',views.loadbuff),
    url(r'^leaderboard', views.leaderboard),
    url(r'^testp$',views.testp),
    url(r'^code',views.CodeSave),
    url(r'^test',views.test),
    url('admin/', admin.site.urls),
    url(r'^question',views.signup),
    url(r'^signup',views.signup),
    url(r'^$', views.start),

]
