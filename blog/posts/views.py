from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail, mail_admins, mail_managers
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, RedirectView, FormView

from posts.models import Category, Post
from posts.forms import PostForm, GirisForm


class Listele(TemplateView):
    template_name = "anasayfa.html"

    def get_context_data(self, **kwargs):
        context = super(Listele, self).get_context_data(**kwargs)
        sayfalanmis = Paginator(Post.published_posts.all(), 3)
        sayfa = self.request.GET.get("sayfa", 1)
        context["gonderiler"] = sayfalanmis.get_page(sayfa)
        return context


class YeniYazi(FormView):
    form_class = PostForm
    success_url = "/"
    template_name = "yeni_yazi.html"

    def get_context_data(self, **kwargs):
        context = super(YeniYazi, self).get_context_data(**kwargs)
        context["yazi_formu"] = PostForm()
        context["kategoriler"] = Category.objects.all()
        return context

    def form_valid(self, form):
        Post.objects.create(
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
            category=form.cleaned_data['category'],
            author=self.request.user,
            cover_photo=self.request.FILES["photo"]
        )
        send_mail(
            "Blog'da yeni yazı: " + form.cleaned_data["title"],
            form.cleaned_data['content'],
            "wolkan777@gmail.com",
            ["wolkan777@gmail.com"]
        )
        return super(YeniYazi, self).form_valid(form)


def goruntule(request):
    pass


class Giris(TemplateView):
    template_name = "giris.html"

    def get_context_data(self, **kwargs):
        context = super(Giris, self).get_context_data(**kwargs)
        context["form"] = GirisForm()
        context["next"] = self.request.GET.get("next")
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return super(Giris, self).dispatch(request, *args, **kwargs)


class Cikis(RedirectView):
    permanent = False
    pattern_name = "anasayfa"

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(Cikis, self).get_redirect_url(*args, **kwargs)


class Kontrol(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        form = GirisForm(self.request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user is not None:
                login(self.request, user)
                messages.add_message(self.request, messages.SUCCESS,
                                     "Başarıyla giriş yaptınız!")
                next_page = self.request.GET.get("next")
                if next_page is not None:
                    self.url = next_page
                else:
                    self.pattern_name = "anasayfa"
            else:
                self.pattern_name = "giris-sayfasi"
        else:
            self.pattern_name = "giris-sayfasi"
        return super(Kontrol, self).get_redirect_url(*args, **kwargs)


class Kayit(TemplateView):
    template_name = "kayit.html"

    def get_context_data(self, **kwargs):
        context = super(Kayit, self).get_context_data(**kwargs)
        context["form"] = GirisForm()
        context["next"] = self.request.GET.get("next")
        return context


class UyeOl(FormView):
    form_class = GirisForm
    success_url = "/"

    def form_valid(self, form):
        var = User.objects.filter(username=form.cleaned_data["username"]).exists()
        if not var:
            user = User.objects.create(username=form.cleaned_data["username"])
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(self.request, user)
        return super(UyeOl, self).form_valid(form)
