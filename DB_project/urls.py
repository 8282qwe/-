"""DB_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from Movie.views import movie_view, login_view, signup_view, logout_view, \
    schedule_view, modify_view, account_view, ticketing_view, delete_view,\
    ticketing_search_view, board_view, search_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', movie_view, name='home'),
                  path('board/', board_view, name='board'),
                  path('login/', login_view, name='login'),
                  path('singup/', signup_view, name='signup'),
                  path('logout/', logout_view, name='logout'),
                  path('schedule/', schedule_view, name='schedule'),
                  path('account/', account_view, name='account'),
                  path('account/modify.html', modify_view, name='modify'),
                  path('delete/', delete_view, name='delete'),
                  path('ticketing_view/', ticketing_search_view, name='ticketing_view'),
                  path('schedule/ticketing/', ticketing_view, name='ticketing'),
                  path('search/', search_view, name='search'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
