# Create your views here.
# search_term = request.GET.get('search_term', None)
# filter_value = request.GET.get('filter_value', None)
# context = dict()
# if search_term:
# vendors = search(search_term, content_type=Vendor).order_by('-created_at')

# python imports

# third party imports
from django.db.models import Q
from rest_framework import (
    status
)
from rest_framework.response import Response

# local imports
from .models import BlogPost
from .search import *


def search_blog_post(request):
    """
    Check email/username is exist in database or not

    :param : request data email/username
    :return: true/false
    :status: 200 or 400
    """
    email = request.GET.get('email', None)
    search_term = request.GET.get('search_term', None)
    context = dict()
    if search_term:
        blog_post_qs = global_search(search_term, content_type=BlogPost).order_by('-created_at')
    message = dict()
    status_code = status.HTTP_400_BAD_REQUEST
    if email:
        message.update({"is_user_exist": False})
        status_code = status.HTTP_200_OK
        if BlogPost.objects.filter(Q(email=email.lower()) | Q(username=email)).exists():
            message.update({"is_user_exist": True})
    return Response(message, status=status_code)
