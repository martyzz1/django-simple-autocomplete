import simplejson

from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType

from simple_autocomplete.monkey import _simple_autocomplete_queryset_cache

def get_json(request, token, fieldname):
    """Return matching results as JSON"""
    result = []
    searchtext = request.GET['q']
    if len(searchtext) >= 3:
        queryset = _simple_autocomplete_queryset_cache.get(int(token), None)
        if queryset is not None:
            di = {'%s__istartswith' % fieldname:searchtext}
            items = queryset.filter(**di).order_by(fieldname)[:10]
            for item in items:
                result.append((item.id, getattr(item, fieldname)))
        else:
            result = 'CACHE_MISS'
        print result            
    return HttpResponse(simplejson.dumps(result))
