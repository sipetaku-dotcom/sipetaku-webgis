from django import forms
from .models import Aset


class AsetForm(forms.ModelForm):
    class Meta:
        model = Aset

        fields = [
            'nama',
            'kategori',
            'jumlah',
            'kondisi',
            'keterangan',
            'foto',
        ]

        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'kategori': forms.TextInput(attrs={'class': 'form-control'}),
            'jumlah': forms.NumberInput(attrs={'class': 'form-control'}),
            'kondisi': forms.Select(attrs={'class': 'form-select'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_nama(self):
        nama = self.cleaned_data.get('nama')

        if nama:
            nama = nama.strip()

            if len(nama) < 3:
                raise forms.ValidationError(
                    'Nama aset terlalu pendek.'
                )

        return nama


    def clean_kategori(self):
        kategori = self.cleaned_data.get('kategori')

        if kategori:
            kategori = kategori.strip()

        return kategori


    def clean_jumlah(self):
        jumlah = self.cleaned_data.get('jumlah')

        if jumlah is not None:
            if jumlah <= 0:
                raise forms.ValidationError(
                    'Jumlah aset harus lebih dari 0.'
                )

        return jumlah
    

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