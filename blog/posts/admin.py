from django.contrib import admin, messages

from posts.models import Category, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created']
    list_filter = ['category', 'status']
    actions = ["toplu_yayinla"]
    actions_on_bottom = True
    actions_on_top = False

    def toplu_yayinla(self, request, queryset):
        if queryset.exclude(status="y").count() != 0:
            queryset.update(status="y")
            # messages.add_message(request, messages.SUCCESS, "Yazılar yayınlandı")
            messages.success(request, "Yazılar yayınlandı")
        else:
            messages.info(request, "Hepsi zaten yayında")
    toplu_yayinla.short_description = "Yazıları toplu yayınla"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)