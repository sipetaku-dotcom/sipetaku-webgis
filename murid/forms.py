from django import forms
from .models import Murid


class MuridForm(forms.ModelForm):
    class Meta:
        model = Murid
        fields = [
            'nama',
            'nisn',
            'nik',
            'jenis_kelamin',
            'tempat_lahir',
            'tanggal_lahir',
            'kelas',
            'alamat',
            'prestasi',
        ]

        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'nisn': forms.TextInput(attrs={'class': 'form-control'}),
            'nik': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-select'}),
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_lahir': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'kelas': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'prestasi': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 1,
                    'placeholder': 'Opsional'
                }
            ),
        }

    def clean_nisn(self):
        nisn = self.cleaned_data.get('nisn')

        if nisn:
            nisn = nisn.strip()

            qs = Murid.objects.filter(nisn=nisn)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    'NISN ini sudah digunakan oleh murid lain.'
                )

        return nisn

    def clean_nik(self):
        nik = self.cleaned_data.get('nik')

        if nik:
            nik = nik.strip()

            qs = Murid.objects.filter(nik=nik)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    'NIK ini sudah digunakan oleh murid lain.'
                )

        return nik