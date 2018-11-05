# from elasticsearch import Elasticsearch
# from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch_dsl.connections import connections

# from .models import BlogPost

connections.create_connection()


class BlogPostIndex(DocType):
    author = Text()
    posted_date = Date()
    title = Text()
    text = Text()

    class Meta:
        index = 'blogpost-index'


# def bulk_indexing():
#     BlogPostIndex.init()
#     es = Elasticsearch()
#     bulk(client=es, actions=(b.indexing() for b in BlogPost.objects.all().iterator()))


def search(author):
    s = Search().filter('term', author=author)
    response = s.execute()
    return response
