from django import forms


class AddressForm(forms.Form):
    # A form to input user geo-address
    place = forms.CharField(label="Place")


class RadiusForm(forms.Form):
    radius = forms.CharField(label="Radius", widget=forms.TextInput(attrs={'placeholder': 'in km'}))
