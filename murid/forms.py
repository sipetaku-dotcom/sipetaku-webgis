from django import forms

from .models import (
    Murid,
    TahunAjaran,
)
from aset.models import DataRombel


class MuridForm(forms.ModelForm):

    rombel = forms.ModelChoiceField(
        queryset=DataRombel.objects.none(),
        required=True,
        label='Kelas / Rombel',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    status_masuk = forms.ChoiceField(
        choices=(
            ('SISWA_BARU', 'Siswa Baru'),
            ('PINDAHAN', 'Siswa Pindahan'),
            ('LANJUT', 'Lanjutan'),
        ),
        required=True,
        label='Status Masuk',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    class Meta:
        model = Murid

        fields = [
            'nama',
            'nisn',
            'nik',
            'jenis_kelamin',
            'tempat_lahir',
            'tanggal_lahir',
            'alamat',
        ]

        labels = {
                'nama': 'Nama',
                'nisn': 'NISN',
                'nik': 'NIK',
                'jenis_kelamin': 'Jenis Kelamin',
                'tempat_lahir': 'Tempat Lahir',
                'tanggal_lahir': 'Tanggal Lahir',
                'alamat': 'Alamat',
            }

        widgets = {

            'nama': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'nisn': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'nik': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'jenis_kelamin': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'tempat_lahir': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'tanggal_lahir': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'alamat': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 1
                }
            ),

        }


    def __init__(
        self,
        *args,
        sekolah=None,
        tahun_ajaran=None,
        **kwargs
    ):

        super().__init__(*args, **kwargs)

        self.fields['tanggal_lahir'].input_formats = [
            '%Y-%m-%d'
        ]

        if sekolah and tahun_ajaran:

            self.fields['rombel'].queryset = (
                DataRombel.objects
                .filter(
                    sekolah=sekolah,
                    tahun_ajaran=tahun_ajaran
                )
                .order_by('nama_kelas')
            )

        else:

            self.fields['rombel'].queryset = (
                DataRombel.objects.none()
            )


    def clean_nisn(self):

        nisn = self.cleaned_data.get('nisn')

        if nisn:

            nisn = nisn.strip()

            qs = Murid.objects.filter(
                nisn=nisn
            )

            if self.instance.pk:

                qs = qs.exclude(
                    pk=self.instance.pk
                )

            if qs.exists():

                raise forms.ValidationError(
                    'NISN ini sudah digunakan '
                    'oleh murid lain.'
                )

        return nisn


    def clean_nik(self):

        nik = self.cleaned_data.get('nik')

        if nik:

            nik = nik.strip()

            qs = Murid.objects.filter(
                nik=nik
            )

            if self.instance.pk:

                qs = qs.exclude(
                    pk=self.instance.pk
                )

            if qs.exists():

                raise forms.ValidationError(
                    'NIK ini sudah digunakan '
                    'oleh murid lain.'
                )

        return nik


class TahunAjaranForm(forms.ModelForm):

    class Meta:

        model = TahunAjaran

        fields = [
            'nama',
            'tanggal_mulai',
            'tanggal_selesai',
        ]

        widgets = {

            'nama': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Contoh: 2028/2029'
                }
            ),

            'tanggal_mulai': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'tanggal_selesai': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }

        labels = {
            'nama': 'Tahun Ajaran',
            'tanggal_mulai': 'Tanggal Mulai',
            'tanggal_selesai': 'Tanggal Selesai',
        }


    def clean(self):

        cleaned_data = super().clean()

        nama = (
            cleaned_data.get('nama') or ''
        ).strip()

        tahun_sebelumnya = (
            cleaned_data.get('tahun_sebelumnya')
        )

        tanggal_mulai = (
            cleaned_data.get('tanggal_mulai')
        )

        tanggal_selesai = (
            cleaned_data.get('tanggal_selesai')
        )


        # =====================================================
        # VALIDASI FORMAT TAHUN AJARAN
        # =====================================================

        try:

            bagian = nama.split('/')

            if len(bagian) != 2:
                raise ValueError

            tahun_awal = int(
                bagian[0]
            )

            tahun_akhir = int(
                bagian[1]
            )

        except (ValueError, TypeError):

            self.add_error(
                'nama',
                'Format Tahun Ajaran harus seperti 2028/2029.'
            )

            return cleaned_data


        # =====================================================
        # TAHUN HARUS BERURUTAN
        # =====================================================

        if tahun_akhir != tahun_awal + 1:

            self.add_error(
                'nama',
                (
                    'Tahun Ajaran harus berurutan. '
                    'Contoh: 2028/2029.'
                )
            )

        # =====================================================
        # VALIDASI TANGGAL
        # =====================================================

        if (
            tanggal_mulai
            and tanggal_selesai
            and tanggal_selesai <= tanggal_mulai
        ):

            self.add_error(
                'tanggal_selesai',
                (
                    'Tanggal selesai harus lebih '
                    'besar dari tanggal mulai.'
                )
            )


        return cleaned_data