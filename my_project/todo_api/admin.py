from django.contrib import admin
from .models import Note


@admin.register(Note)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'state', 'author','importance','public','pubdate')
    fields = (('title','author'), 'content', ('state', 'public','importance'),'pubdate')
    search_fields = ('title', 'content')
    list_filter = ('author', 'importance', 'state', 'public')
    readonly_fields = ('author',)

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'author') or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
