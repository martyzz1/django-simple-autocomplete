import pickle

from django.forms.widgets import Select, SelectMultiple
from django.utils.safestring import mark_safe
from django.db.models.query import QuerySet
from django.conf import settings
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse

from simple_autocomplete.monkey import _simple_autocomplete_queryset_cache
from simple_autocomplete.utils import get_search_fieldname, \
    get_threshold_for_model


class AutoCompleteWidget(Select):
    input_type = 'autocomplete'
    url = None
    initial_display = None
    token = None
    model = None

    class Media:
        css = {
            'all': ('simple_autocomplete/jquery-ui.css',)
        }
        js = (
            'simple_autocomplete/jquery-ui.js',
            'simple_autocomplete/simple_autocomplete.js',
        )


    def __init__(self, url=None, initial_display=None, token=None,
        model=None, *args, **kwargs):
        """
        url: a custom URL that returns JSON with format [(value, label),(value,
        label),...].

        initial_display: if url is provided then initial_display is the initial
        content of the autocomplete box, eg. "John Smith".

        token: an identifier to retrieve a cached queryset. Used internally.

        model: the model that the queryset objects are instances of. Used
        internally.
        """
        self.url = url
        self.initial_display = initial_display
        self.token = token
        self.model = model
        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        display = ''
        if self.url:
            url = self.url
            display = self.initial_display

        else:
            dc, dc, query = pickle.loads(
                _simple_autocomplete_queryset_cache[self.token]
            )
            queryset = QuerySet(model=self.model, query=query)
            threshold = get_threshold_for_model(self.model)
            if threshold and (queryset.count() < threshold):
                # Render the normal select widget if size below threshold
                return super(AutoCompleteWidget, self).render(
                    name, value, attrs
                )
            else:
                url = reverse('simple_autocomplete:simple-autocomplete', args=[self.token])
                if value:
                    obj = queryset.get(pk=value)
                    if hasattr(obj, "__unicode__"):
                        display = obj.__unicode__()
                    else:
                        display = str(value)

        html = u"""
<input id="id_%(name)s_helper" class="sa_autocompletewidget" type="text" value="%(display)s" data-url="%(url)s" />
<a href="#" title="Clear" onclick="django.jQuery('#id_%(name)s_helper').val(''); django.jQuery('#id_%(name)s_helper').focus(); django.jQuery('#id_%(name)s').val(''); return false;">x<small></small></a>
<input name="%(name)s" id="id_%(name)s" type="hidden" value="%(value)s" />""" % dict(name=name, url=url, display=display, value=value)
        return mark_safe(html)


class AutoCompleteMultipleWidget(SelectMultiple):
    input_type = 'autocomplete_multiple'
    url = None
    initial_display = None
    token = None
    model = None

    class Media:
        css = {
            'all': ('simple_autocomplete/jquery-ui.css',)
        }
        js = (
            'simple_autocomplete/jquery-ui.js',
            'simple_autocomplete/simple_autocomplete.js',
        )


    def __init__(self, url=None, initial_display=None, token=None,
        model=None, *args, **kwargs):
        """
        url: a custom URL that returns JSON with format [(value, label),(value,
        label),...].

        initial_display: if url is provided then initial_display is a
        dictionary containing the initial content of the autocomplete box, eg.
        {1:"John Smith", 2:"Sarah Connor"}. The key is the primary key of the
        referenced item.

        token: an identifier to retrieve a cached queryset. Used internally.

        model: the model that the queryset objects are instances of. Used
        internally.
        """
        self.url = url
        self.initial_display = initial_display
        self.token = token
        self.model = model
        super(AutoCompleteMultipleWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = []

        display = ''
        if self.url:
            url = self.url
            # todo: Display is not so simple in this case. Needs a lot of work.
            # Will probably have to be a dictionary.
            display = self.initial_display
        else:
            dc, dc, query = pickle.loads(
                _simple_autocomplete_queryset_cache[self.token]
            )
            queryset = QuerySet(model=self.model, query=query)
            threshold = get_threshold_for_model(self.model)
            if threshold and (queryset.count() < threshold):
                # Render the normal select widget if size below threshold
                return super(AutoCompleteMultipleWidget, self).render(
                    name, value, attrs
                )
            else:
                url = reverse('simple_autocomplete:simple-autocomplete', args=[self.token])

            html = u"""
<input id="id_%(name)s_helper" class=".sa_autocompletemultiplewidget" type="text" value="" data-url="%(url)s" data-name="%(name)s"  />
<input id="id_%(name)s" type="hidden" value="" />
<div class="autocomplete-placeholder">""" % dict(name=name, url=url)

            # Create html for existing values
            for v in value:
                if v is None: continue
                obj = queryset.get(pk=v)
                if hasattr(obj, "__unicode__"):
                    display = obj.__unicode__()
                else:
                    display = str(value)

                html += """<p><input name="%s" type="hidden" value="%s" />
%s <a href="#" title="Remove" onclick="django.jQuery(this).parent().remove(); django.jQuery('#id_%s_helper').val(''); django.jQuery('#id_%s_helper').focus(); return false;">x<small></small></a></p>""" % (name, v, display, name, name)

            html += "</div>"

            # Help with green plus icon alignment
            # todo: use css class
            html += """<div style="display: inline-block; width: 104px;">&nbsp;</div>"""

            return mark_safe(html)
