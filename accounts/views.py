from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView

from accounts.forms import HitModelForm
from accounts.models import Hit


class HomePageView(TemplateView):
    template_name = 'home.html'


class HitCreateView(LoginRequiredMixin, CreateView):
    model = Hit
    form_class = HitModelForm
    template_name = 'hit/create-hit.html'
    success_url = reverse_lazy('create_hit')

    def get_form_kwargs(self):
        kwargs = super(HitCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        hit = form.save(commit=False)
        hit.author = self.request.user
        hit.save()
        return super(HitCreateView, self).form_valid(form)


class HitListView(ListView):
    model = Hit
    template_name = 'hit/list-hit.html'
    context_object_name = 'hits'

    def get_queryset(self):
        kind = self.request.user.kind
        if kind=="hitman":
            queryset = Hit.objects.filter(hitman=self.request.user)
        else:
            queryset = Hit.objects.all()

        return queryset
