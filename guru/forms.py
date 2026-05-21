from django import forms
from .models import Guru


class GuruForm(forms.ModelForm):
    class Meta:
        model = Guru

        fields = [
            'nama',
            'nip',
            'nik',
            'jenis_kelamin',
            'tempat_lahir',
            'tanggal_lahir',
            'jabatan',
            'status_pegawai',
            'mata_pelajaran',
            'tanggal_pensiun',
            'alamat',
            'no_hp',
        ]

        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'nip': forms.TextInput(attrs={'class': 'form-control'}),
            'nik': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-select'}),
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_lahir': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control'}),
            'status_pegawai': forms.Select(attrs={'class': 'form-select'}),
            'mata_pelajaran': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_pensiun': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nip(self):
        nip = self.cleaned_data.get('nip')

        if nip:
            nip = nip.strip()

            qs = Guru.objects.filter(nip=nip)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    'NIP ini sudah digunakan oleh guru lain.'
                )

        return nip

    def clean_nik(self):
        nik = self.cleaned_data.get('nik')

        if nik:
            nik = nik.strip()

            qs = Guru.objects.filter(nik=nik)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    'NIK ini sudah digunakan oleh guru lain.'
                )

        return nik