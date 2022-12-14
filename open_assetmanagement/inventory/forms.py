import magic
from django import forms
from .models import Device, Product, ProductSupplier, Software
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = []


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class SupplierForm(forms.ModelForm):
    class Meta:
        model = ProductSupplier
        exclude = []


class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        exclude = []


class NetworkdiscoveryForm(forms.Form):
    ip_range = forms.CharField()
    type = forms.ChoiceField(
        choices=[
            (0, 'Very Careful - Only passive Arp Scan (Netdiscover)'),
            (1, 'Careful - Only active Arp Scan (Netdiscover)'),
            (2, "Medium - NMAP TCP-SYN Scan"),
            (3, "Os - NMAP OS Scan and CME Scan"),
            (4, "Full - Full Port Scan"),
        ]
    )
    timeout = forms.ChoiceField(
        choices=[
            (15, 'Very Fast - 15 Seconds'),
            (60, 'Fast - 1 Minute'),
            (300, "Medium - 5 Minutes"),
            (3600, "Slow - 1 Hour"),
        ]
    )


class S7discoveryForm(forms.Form):
    ip_range = forms.CharField()


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()
    delimiter = forms.ChoiceField(
        choices=[
            (',', 'Unknown - Or Exel File'),
            (";", "Semicolon ';'"),
            (",", "Comma ','"),
        ]
    )

    def clean_title(self):
        data = self.cleaned_data['title']
        if "bad" in data:
            raise ValidationError(_('Invalid name'))

        # Remember to always return the cleaned data.
        return data

    def clean_file(self):
        file = self.cleaned_data.get("file", False)
        filetype = magic.from_buffer(file.read())
        if "text" not in filetype and "Microsoft Excel" not in filetype:
            raise ValidationError("Filetype ist wrong, you tried uploading: '" + filetype + "' but should have "
                                                                                            "uploaded: CSV or XLSX")
        return file
