from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from website import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('galeri/', views.gallery, name='gallery'),
    path('iletisim/', views.contact, name='contact'),
    path('kvkk/', views.kvkk, name='kvkk'),
    path('cerez-politikasi/', views.cookie_policy, name='cookie_policy'),
    path('kullanim-kosullari/', views.terms_of_use, name='terms_of_use'),
    path('hakkimizda/', views.about, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)