import operator
from functools import reduce

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch_dsl.connections import connections

from .models import BlogPost

connections.create_connection()

# On Which fields want to search at which model, Update SEARCH_MAP dict for searching with model name and fields name
SEARCH_MAP = {
    BlogPost: {'search_fields': ['author__first_name__icontains', 'author__last_name__icontains']}
}


class BlogPostIndex(DocType):
    author = Text()
    posted_date = Date()
    title = Text()
    text = Text()

    class Meta:
        index = 'blogpost-index'


def bulk_indexing():
    BlogPostIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in BlogPost.objects.all().iterator()))


def search(author):
    s = Search().filter('term', author=author)
    response = s.execute()
    return response


def build_query(search_by, search_term):
    query = []
    if search_by:
        for key in search_by:
            query.append({key: search_term})
    return query


def get_search_fields(model):
    return SEARCH_MAP[model]['search_fields']


def get_model_class(content_type):
    content_type = ContentType.objects.filter(model__iexact=content_type)
    if content_type:
        content_type = content_type.first()
        model = content_type.model_class()
        return model
    return None


def global_search(search_term, content_type=None, limit=None):
    # get the model name we are searching for
    model = content_type
    # get search fields for the above model
    search_fields = get_search_fields(model)
    # build query
    query = build_query(search_fields, search_term)
    results = model.objects.filter(reduce(operator.or_, [Q(**x) for x in query]))
    if limit:
        results = results[:limit]
    return results

