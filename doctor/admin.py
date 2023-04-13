from django.contrib import admin

# Register your models here.
from .models import Category,Post,Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','is_published','posted_at')
    list_filter = ('is_published','posted_at')
    list_editable = ('is_published',)
    



class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','is_resolved','commented_at')
    list_filter = ('is_resolved','commented_at')
    list_editable = ('is_resolved',)


admin.site.register(Category)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)