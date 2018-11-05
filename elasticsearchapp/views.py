# python imports

# third party imports
from rest_framework import (
    status
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# local imports
from .global_search import *
from .serializers import BlogPostSerializer


class BlogPostView(ModelViewSet):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    http_method_names = ('get',)

    def list(self, request, *args, **kwargs):
        search_term = request.GET.get('search_term', None)
        message = dict()
        message.update({"details": False})
        status_code = status.HTTP_400_BAD_REQUEST
        if search_term:
            blog_post_qs = global_search(search_term, model_name=BlogPost)
            serializer = self.serializer_class(blog_post_qs, many=True).data
            status_code = status.HTTP_200_OK
            return Response(serializer, status=status_code)
        return Response(message, status=status_code)