from django.http import HttpResponseForbidden


class HitCreationsPermissionsMixin:

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_boss() and not user.is_manager():
            return HttpResponseForbidden()
        return super().dispatch(request, * args, ** kwargs)

class HitMenListPermissionsMixin:

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_boss() and not user.is_manager():
            return HttpResponseForbidden()
        return super().dispatch(request, * args, ** kwargs)