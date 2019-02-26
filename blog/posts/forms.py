from django import forms

from posts.models import Post, Category


class PostForm(forms.Form):
    title = forms.CharField(max_length=50, label="Başlık")
    content = forms.CharField(widget=forms.Textarea, label="İçerik")
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Kategori"
    )
    photo = forms.ImageField(label="Kapak Resmi")


class GirisForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)