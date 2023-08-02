from rest_framework.decorators import authentication_classes

def jwt_optional(view_func):
    view_func = authentication_classes([])(view_func)
    return view_func
