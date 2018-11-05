"""
authentication app urls
"""
# third party imports
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

# local imports
from . import views

router = DefaultRouter()
router.register(r'blog-search', views.BlogPostView, base_name='search_blog_post')

urlpatterns = [
    url(r'^', include(router.urls))
]
