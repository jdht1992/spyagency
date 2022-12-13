from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Select, CharField, BooleanField, CheckboxInput
from accounts.models import CustomUser, Hit, FAILED, COMPLETED


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)


class HitModelForm(ModelForm):
    @staticmethod
    def _get_hitman(user):
        queryset = CustomUser.objects.none()
        if user.is_boss():
            queryset = CustomUser.objects.filter(is_active=True).exclude(email=user.email)
        elif user.is_manager():
            queryset = user.lackeys.filter(is_active=True)

        return queryset

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(HitModelForm, self).__init__(*args, **kwargs)
        self.fields['hitman'].queryset = self._get_hitman(self.request.user)

    class Meta:
        model = Hit
        fields = ("hitman", "description", "target_name", "status",)


class HitUpdateModelForm(ModelForm):
    list_hitman = ["hitman", "description", "target_name", ]
    list_hitman_manager = ["description", "target_name", "status"]
    all_fields = ["hitman", "description", "target_name", "status"]

    @staticmethod
    def _get_hitman(user):
        queryset = CustomUser.objects.none()
        if user.is_boss():
            queryset = CustomUser.objects.filter(is_active=True).exclude(email=user.email)
        elif user.is_manager():
            queryset = user.lackeys.filter(is_active=True)

        return queryset

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(HitUpdateModelForm, self).__init__(*args, **kwargs)
        user = self.request.user

        self.fields['hitman'].queryset = self._get_hitman(user)

        readonly_fields = self.all_fields
        if self.instance.status in [FAILED, COMPLETED]:
            readonly_fields = self.all_fields
        else:
            if not self.instance.hitman.is_active:
                readonly_fields = []
            elif user.is_manager() or user.is_boss():
                readonly_fields = self.list_hitman_manager
            else:
                readonly_fields = self.list_hitman

        for key in readonly_fields:
            if isinstance(self.fields[f'{key}'].widget, Select):
                self.fields[f'{key}'].widget.attrs['disabled'] = True
            else:
                self.fields[f'{key}'].widget.attrs['readonly'] = True

    class Meta:
        model = Hit
        fields = ("hitman", "description", "target_name", "status",)


class UpdateHitBulkModelForm(ModelForm):
    list_hitman_manager = ["description", "target_name", "status"]

    def __init__(self, *args, **kwargs):
        super(UpdateHitBulkModelForm, self).__init__(*args, **kwargs)

        self.fields['hitman'].queryset = CustomUser.objects.filter(is_active=True).exclude(email='jdht1992@gmail.com')

        for key in self.list_hitman_manager:
            if isinstance(self.fields[f'{key}'].widget, Select):
                self.fields[f'{key}'].widget.attrs['disabled'] = True
            else:
                self.fields[f'{key}'].widget.attrs['readonly'] = True

    class Meta:
        model = Hit
        fields = ("hitman", "description", "target_name", "status",)


class CustomUserModelForm(ModelForm):
    first_name = CharField(label="Name")
    is_active = BooleanField(help_text="", required=False)
    all_fields = ["first_name", "email", "description", "is_active"]
    boos_fields = ["first_name", "email", "description"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CustomUserModelForm, self).__init__(*args, **kwargs)
        user = self.request.user

        readonly_fields = self.all_fields
        if user.is_boss() and self.instance.is_active:
            readonly_fields = self.boos_fields

        for key in readonly_fields:
            if isinstance(self.fields[f'{key}'].widget, CheckboxInput):
                self.fields[f'{key}'].widget.attrs['disabled'] = True
            else:
                self.fields[f'{key}'].widget.attrs['readonly'] = True

    class Meta:
        model = CustomUser
        fields = ("first_name", "email", "description", "is_active")
