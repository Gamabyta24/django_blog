from django import forms


class DeleteForm(forms.Form):
    """Форма для подтверждения удаления."""

    confirm = forms.BooleanField(
        required=True,
        label="Подтвердите удаление",
        widget=forms.HiddenInput(),
    )
