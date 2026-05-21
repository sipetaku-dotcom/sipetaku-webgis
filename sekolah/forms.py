from django import forms
from .models import Sekolah


class SekolahForm(forms.ModelForm):
    class Meta:
        model = Sekolah
        fields = [
            'nama',
            'npsn',
            'kategori',
            'status',
            'alamat',
            'kecamatan',
            'desa',
            'x_utm',
            'y_utm',
            'zona_utm',
            'jumlah_murid',
            'jumlah_guru',
            'foto',
        ]

        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'npsn': forms.TextInput(attrs={'class': 'form-control'}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'kecamatan': forms.TextInput(attrs={'class': 'form-control'}),
            'desa': forms.TextInput(attrs={'class': 'form-control'}),
            'x_utm': forms.NumberInput(attrs={'class': 'form-control'}),
            'y_utm': forms.NumberInput(attrs={'class': 'form-control'}),
            'zona_utm': forms.TextInput(attrs={'class': 'form-control'}),
            'jumlah_murid': forms.NumberInput(attrs={'class': 'form-control'}),
            'jumlah_guru': forms.NumberInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')

        if foto:
            maksimal_ukuran = 2 * 1024 * 1024  # 2MB

            if foto.size > maksimal_ukuran:
                raise forms.ValidationError(
                    'Ukuran foto maksimal 2MB.'
                )

            ekstensi_valid = ['jpg', 'jpeg', 'png']
            ekstensi = foto.name.split('.')[-1].lower()

            if ekstensi not in ekstensi_valid:
                raise forms.ValidationError(
                    'Format foto harus JPG, JPEG, atau PNG.'
                )

        return foto