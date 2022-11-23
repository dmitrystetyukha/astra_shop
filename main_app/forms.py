import django.forms as forms


class CallBackOrderForUnauthorizedUsers(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Олег"}),
        max_length=30,
        required=True,
        label="Ваше имя:",
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder": "oleg@mail.ru"}),
        required=True,
        label="Ваш e-mail:",
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "+7(312)123-12-12",
            }
        ),
        max_length=17,
        required=False,
        label="Ваш номер телефона (необязательно):",
    )
    comment = forms.CharField(
        max_length=350,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Ваш комментарий к заявке здесь...",
                "rows": "3",
            }
        ),
        label="Комментарий:",
        required=False,
    )
    preferred_communication_method = forms.CharField(
        required=False,
        label="Предпочитаемый способ связи",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Например, WhatsApp, после 17:00",
            }
        ),
    )


class CallBackOrderForAuthorizedUsers(forms.Form):
    comment = forms.CharField(
        max_length=350,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Ваш комментарий к заявке здесь...",
                "rows": "3",
            }
        ),
        label="Комментарий:",
        required=False,
    )
    preferred_communication_method = forms.CharField(
        required=False,
        label="Предпочитаемый способ связи",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Например, WhatsApp, после 17:00",
            }
        ),
    )
