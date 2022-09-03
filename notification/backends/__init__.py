from django.utils import importlib
from django.core.exceptions import ImproperlyConfigured


# Name for use in settings file --> name of module in "backends" directory.
# Any backend scheme that is not in this dictionary is treated as a Python
# import path to a custom backend.
BACKENDS = {
    'email': 'email.EmailBackend',
    'facebook': 'fb.FacebookWallPostBackend',
    'web': 'web.WebBackend',
    'dummy': 'dummy.DummyBackend',
}

DEFAULT_BACKENDS = ['email', 'web']

def load_backend(backend):
    if backend in BACKENDS:
        path = 'notification.backends.%s' % BACKENDS[backend]
    else:
        path = backend

    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing notification backend %s: "%s"' % (module, e))
    except ValueError as e:
        raise ImproperlyConfigured('Error importing notification backends. Is NOTIFICATION_BACKENDS a correctly defined list or tuple?')
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" notification backend' % (module, attr))

    return cls()

def get_backends():
    try:
    	from django.conf import settings
    except ImportError:
        return set()
    backends = []
    for backend in getattr(settings, 'NOTIFICATION_BACKENDS', []):
        backends.append(load_backend(backend))
    if not backends:
        for backend in DEFAULT_BACKENDS:
            backends.append(load_backend(backend))
    return set(backends)

backends = get_backends()

def get_backend_field_choices():
    choices = []
    for backend in backends:
        name = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        choices.append((name, backend.display_name))
    return set(choices)

backend_field_choices = get_backend_field_choices()
