from django import forms
from .models import Prestasi
from datetime import date


class PrestasiForm(forms.ModelForm):
    class Meta:
        model = Prestasi
        fields = [
            'murid',
            'nama_lomba',
            'bidang_lomba',
            'tingkat',
            'juara',
            'tahun',
            'keterangan',
            'bukti_foto',
        ]

        widgets = {
            'murid': forms.Select(attrs={'class': 'form-select'}),
            'nama_lomba': forms.TextInput(attrs={'class': 'form-control'}),
            'bidang_lomba': forms.TextInput(attrs={'class': 'form-control'}),
            'tingkat': forms.Select(attrs={'class': 'form-select'}),
            'juara': forms.Select(attrs={'class': 'form-select'}),
            'tahun': forms.NumberInput(attrs={'class': 'form-control'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bukti_foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_tahun(self):
        tahun = self.cleaned_data.get('tahun')

        tahun_sekarang = date.today().year

        if tahun:

            if tahun > tahun_sekarang:
                raise forms.ValidationError(
                    'Tahun prestasi tidak boleh melebihi tahun sekarang.'
                )

            if tahun < 2000:
                raise forms.ValidationError(
                    'Tahun prestasi terlalu lama.'
                )

        return tahun
    
    def clean_nama_lomba(self):
        nama_lomba = self.cleaned_data.get('nama_lomba')

        if nama_lomba:
            nama_lomba = nama_lomba.strip()

            if len(nama_lomba) < 3:
                raise forms.ValidationError(
                    'Nama lomba terlalu pendek.'
                )

        return nama_lomba