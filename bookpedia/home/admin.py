from django.contrib import admin
from matplotlib.pyplot import cla

#MY IMPORTS
from .models import Book, Category


class BookAdmin(admin.ModelAdmin):
    exclude = ('rating', 'slug',)


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
