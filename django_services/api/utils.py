# -*- coding:utf-8 -*-

from django.utils.safestring import mark_safe
from rest_framework.utils import formatting
from rest_framework.compat import smart_text


def get_filter_fields(view):
    filter_fields = list(getattr(view, 'filter_fields', []))
    for filter_backend in getattr(view, 'filter_backends', []):
        if hasattr(filter_backend, 'filter_field'):
            filter_fields.append(filter_backend.filter_field)
    return filter_fields


def get_view_doc(view, html=True):
    """
    Build view documentation. Return in html format.
    If you want in markdown format, use html=False
    """
    try:
        description = view.__doc__ or ''
        description = formatting.dedent(smart_text(description))

        # include filters in description
        filter_fields = get_filter_fields(view)
        if filter_fields:
            filter_doc = ['\n\n\n## Filters', '']
            for f in filter_fields:
                filter_doc.append('- `%s`' % f)
            description += '\n'.join(filter_doc)

        # replace {api_url} by current base url
        api_url = "/api"
        description = description.replace('{api_url}', api_url)
        if html:
            description = formatting.markup_description(description)
        return description
    except:
        import traceback
        traceback.print_exc()
        raise


def wrap_accordion(text_body_list):
    """
    Wrap text_body_list in twitter bootstrap accordion. text_body_list must be list with tuple with title and body
    """
    html = ['<div class="accordion" id="accordion2">']

    for i, item in enumerate(text_body_list):
        params = {
            'index': i,
            'title': item[0],
            'body': item[1]
        }

        html.append('''
<div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse%(index)d">
        %(title)s
      </a>
    </div>
    <div id="collapse%(index)d" class="accordion-body collapse">
      <div class="accordion-inner">
        %(body)s
      </div>
    </div>
  </div>
  <br/>
''' % params)
    return mark_safe('\n'.join(html))
