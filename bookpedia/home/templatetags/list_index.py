from django import template


register = template.Library()


# INDEX custom filter:
# this filter returns index of an element from a 
# list starting from 1 instead of 0 in order to allow 
# you to use it directly in your templates

def index(item, items_query):
    items_list = list(items_query)      # converting queryset to list inorder to
    return (items_list.index(item) + 1) # be able to use index() function

register.filter('index', index)