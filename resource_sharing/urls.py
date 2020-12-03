"""resource_sharing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from authen import views
from django_email_verification import urls as mail_urls
from products import views as prodviews

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home, name='home'),
                  path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('signup/', views.signup, name='signup'),
                  path('buy/product/<int:myid>', prodviews.product, name='item'),
                  path('buy/sendrequest/<int:myid>', prodviews.sendrequest, name='request'),
                  path('buy/search/', prodviews.search, name='search'),
                  path('buy/category/<slug:category>', prodviews.buy, name='buy'),
                  path('buy/confirm/<int:pid>', prodviews.confirm, name='confirm'),
                  path('aboutus/', views.aboutus, name='aboutus'),
                  path('wishlist/<int:pid>', prodviews.create_wishlist),
                  path('yourorders/', prodviews.yourorders, name='yourorders'),
                  path('wishlist/', prodviews.wishlist, name='wishlist'),
                  path('yourads/', prodviews.yourads, name='yourads'),
                  path('yourads/<int:pid>', prodviews.deletead),
                  path('yourads/edit/<int:pid>', prodviews.editad),
                  path('profile/', views.profile, name='profile'),
                  path('profile/edit/general', views.editprofile, name='editprofile'),
                  path('profile/edit/password', views.editpassword, name='editpassword'),
                  path('sell/', prodviews.sell, name='sell'),
                  path('contact-us/', views.contactus, name='contactus'),
                  path('404/', views.error, name='404'),
                  path('email/', include(mail_urls)),
                  path('resend/<slug:username>', views.resend, name='resend'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = views.handler404
