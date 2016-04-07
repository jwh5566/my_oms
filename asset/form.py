from django import forms
from .models import HostList

class HostsListForm(forms.ModelForm):

    class Meta:
        model = HostList
        fields = ('ip', 'hostname', 'product', 'application', 'idc_jg', 'status', 'remark')
        widgets = {
          'ip': forms.TextInput(attrs={'class': 'form-control'}),
          'hostname': forms.TextInput(attrs={'class': 'form-control'}),
          'product': forms.TextInput(attrs={'class': 'form-control'}),
          'application': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_jg': forms.TextInput(attrs={'class': 'form-control'}),
          'status': forms.TextInput(attrs={'class': 'form-control'}),
          'remark': forms.TextInput(attrs={'class': 'form-control'}),
        }
