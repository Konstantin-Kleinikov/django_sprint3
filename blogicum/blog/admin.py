from django.contrib import admin


from .models import Category, Location, Post


admin.site.empty_value_display = 'Не задано'


class PostInLine(admin.TabularInline):
    model = Post
    extra = 0
    readonly_fields = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at',
    )


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInLine,
    )
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = (
        'description',
        'slug',
        'is_published',
    )
    list_display_links = ('title',)
    list_filter = (
        'slug',
        'is_published',
    )


class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInLine,
    )
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    list_display_links = ('name',)
    list_filter = ('is_published',)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at',
    )
    list_editable = (
        'pub_date',
        'location',
        'category',
        'is_published',
    )
    search_fields = (
        'title',
        'text',
    )
    list_display_links = ('title',)
    list_select_related = (
        'author',
        'category',
        'location',
    )
    list_filter = (
        'author',
        'location',
        'category',
        'is_published'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
