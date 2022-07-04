from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)

    return wrapper_func

def allowed_users(allowed_users=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            role = request.user.groups.all()[0].name
            if role not in allowed_users:
                return redirect('home')
            else:
                return view_func(request,*args,**kwargs)

        return wrapper_func
    return decorator