from django.contrib import admin
from .models import Post, Profile, ChatMessage, ChatConversation, Skill


admin.site.register(Profile)
admin.site.register(ChatMessage)
admin.site.register(ChatConversation)
admin.site.register(Skill)


@admin.action(description="Publish selected posts")
def publish_posts(modeladmin, request, queryset):
    queryset.update(is_published=True)
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'created_at',
        'is_published'
    )

    search_fields = (
        'title',
        'author__username'
    )

    list_filter = (
        'is_published',
        'created_at'
    )
    actions = [publish_posts]

admin.site.site_header = "Programmer Hub Admin"
admin.site.site_title = "Programmer Hub"
admin.site.index_title = "Dashboard"


    