
# Python imports

# third party imports
from rest_framework import (
    serializers
)

# local imports
from .models import *


class BlogPostSerializer(serializers.ModelSerializer):
    """
    Details of blog post
    """

    class Meta:
        """
        Define fields for this serializer
        """
        model = BlogPost
        fields = '__all__'

