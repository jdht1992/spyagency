from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from accounts.forms import (HitModelForm, HitUpdateModelForm, CustomUserModelForm, CustomUserCreationForm,
                            UpdateHitBulkModelForm)
from accounts.models import Hit, CustomUser
from accounts.permissions import HitCreationsPermissionsMixin, HitMenListPermissionsMixin


class HomePageView(TemplateView):
    template_name = 'home.html'


class SignupPageView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


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
        if hit.hitman:
            hit.status = Hit.Status.ASSIGNED
        hit.author = self.request.user
        hit.save()
        return super(HitCreateView, self).form_valid(form)


class HitListView(LoginRequiredMixin, ListView):
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


class HitUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Hit
    template_name = 'hit/update-hit.html'
    form_class = HitUpdateModelForm
    success_message = " was update successfully"

    def get_form_kwargs(self):
        kwargs = super(HitUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse_lazy('update_hit', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        hit = form.save(commit=False)
        if hit.hitman and hit.status == hit.Status.OPEN:
            hit.status = Hit.Status.ASSIGNED
        elif not hit.hitman:
            hit.status = Hit.Status.OPEN
        hit.save()
        return super(HitUpdateView, self).form_valid(form)
    #

def post_hitlbul(request):
    hitbulkFormSet = modelformset_factory(Hit, form=UpdateHitBulkModelForm, extra=3)
    if request.method == 'POST':

        formset = hitbulkFormSet(request.POST, queryset=Hit.objects.none())

        if formset.is_valid():
            for form in formset.cleaned_data:
                hitman = form['hitman']
                description = form['description']
                target_name = form['target_name']
                status = form['status']
                hit = Hit(hitman=hitman, description=description, target_name=target_name, status=status)
                hit.save()
                # messages.success(request, "Posted!")
            return HttpResponseRedirect("/")
        else:
            print(formset.errors)
    else:
        formset = hitbulkFormSet(queryset=Hit.objects.all())
    return render(request, 'hit/update-hit-bulk.html', {'formset': formset})


class HitmanDetailView(HitMenListPermissionsMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'hitman/detail-hitman.html'
    form_class = CustomUserModelForm
    success_message = " was update successfully"

    def get_object(self):
        return CustomUser.objects.get(id=self.kwargs.get('id'))

    def get_form_kwargs(self):
        kwargs = super(HitmanDetailView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse_lazy('detail_hitman', kwargs={'id': self.object.id})


class HitmanListView(HitMenListPermissionsMixin, LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'hitman/list-hitman.html'
    context_object_name = 'men'

    def get_queryset(self):
        user = self.request.user

        if user.is_boss():
            queryset = CustomUser.objects.all()
        elif user.is_manager():
            queryset = user.lackeys.all()

        return queryset
