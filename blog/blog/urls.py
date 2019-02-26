"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from posts.views import Listele, YeniYazi, goruntule, Giris, Kontrol,\
    Cikis, Kayit, UyeOl

urlpatterns = [
    path('', Listele.as_view(), name="anasayfa"),
    # Sadece template gösteriyorsak böyle bir kullanım da mümkün!
    # path('', TemplateView.as_view(template_name="blog.html")),
    path('yeni/', login_required(YeniYazi.as_view(), login_url="/giris/")),
    path('giris/', Giris.as_view(), name="giris-sayfasi"),
    path('kayit/', Kayit.as_view(), name="kayit-sayfasi"),
    path('uyeol/', UyeOl.as_view()),
    path('cik/', Cikis.as_view(), name="cikis-sayfasi"),
    path('kontrol/', Kontrol.as_view()),
    path('yazi/<int:post_id>', goruntule),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
