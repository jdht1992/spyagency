from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from accounts.models import CustomUser, Hit


# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm):
#         model = CustomUser
#         fields = UserCreationForm.Meta.fields
#
#
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = UserChangeForm.Meta.fields


class HitModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(HitModelForm, self).__init__(*args, **kwargs)
        self.fields['hitman'].queryset = CustomUser.objects.filter(
            is_active=True).exclude(email=self.request.user)

    class Meta:
        model = Hit
        fields = ("hitman", "description", "target_name", "status",)
