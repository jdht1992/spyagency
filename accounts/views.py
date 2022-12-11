from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView

from accounts.forms import HitModelForm, HitUpdateModelForm
from accounts.models import Hit, CustomUser, BOSS
from accounts.permissions import HitCreationsPermissionsMixin


class HomePageView(TemplateView):
    template_name = 'home.html'


class HitCreateView(HitCreationsPermissionsMixin, LoginRequiredMixin, CreateView):
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
        user = self.request.user

        if user.is_boss():
            queryset = Hit.objects.all()
        elif user.is_manager():
            queryset = Hit.objects.filter(Q(hitman__in=user.lackeys.all()) | Q(hitman=user))
        else:
            queryset = Hit.objects.filter(hitman=user)

        return queryset


class HitUpdateView(LoginRequiredMixin, UpdateView):
    model = Hit
    template_name = 'hit/update-hit.html'
    form_class = HitUpdateModelForm

    def get_form_kwargs(self):
        kwargs = super(HitUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse_lazy('update_hit', kwargs={'pk': self.object.id})


class HitmanDetailView(DetailView):
    template_name = 'hitman/list-hitman.html'
    context_object_name = 'hitman'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, id=self.kwargs.get("id"))


class HitmanListView(ListView):
    model = Hit
    template_name = 'hitman/list-hitman.html'
    context_object_name = 'men'
