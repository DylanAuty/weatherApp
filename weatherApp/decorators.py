from django.utils.decorators import available_attrs
from django.views.decorators.cache import cache_page

def cache_page_vary_on_locationString(func):
    def wrapper(request, *args, **kwargs):
        if 'locationString' in request.session:
            cached = cache_page(60 * 15, key_prefix=request.session['locationString'])(func)
        else:
            request.session['locationString'] = "/q/zmw:00000.1.03772"  # For London, UK
            cached = cache_page(60 * 15, key_prefix=request.session['locationString'])(func)
        return cached(request, *args, **kwargs)
    return wrapper
