import operator
from functools import reduce

from django.db.models import Q

from .models import BlogPost

# On Which fields want to search at which model, Update SEARCH_MAP dict for searching with model name and fields name
SEARCH_MAP = {
    BlogPost: {'search_fields': ['author__first_name__icontains', 'author__last_name__icontains']}
}


def build_query(search_by, search_term):
    query = []
    if search_by:
        for key in search_by:
            query.append({key: search_term})
    return query


def get_search_fields(model):
    return SEARCH_MAP[model]['search_fields']


def global_search(search_term, model_name=None, limit=None):
    # get search fields for the above model
    search_fields = get_search_fields(model_name)
    # build query
    query = build_query(search_fields, search_term)
    results = model_name.objects.filter(reduce(operator.or_, [Q(**x) for x in query]))
    if limit:
        results = results[:limit]
    return results

