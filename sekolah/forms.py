from django import forms

from .models import Sekolah
from .wilayah import DATA_WILAYAH


class SekolahForm(forms.ModelForm):

    kecamatan = forms.ChoiceField(
        choices=[],
        label='Kecamatan',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'id_kecamatan',
            }
        )
    )

    desa = forms.ChoiceField(
        choices=[],
        label='Desa',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'id_desa',
            }
        )
    )


    class Meta:

        model = Sekolah

        fields = [
            'nama',
            'npsn',
            'kategori',
            'status',
            'kecamatan',
            'desa',
            'alamat',
            'zona_utm',
            'x_utm',
            'y_utm',
            'foto',
        ]


        labels = {

            'nama':
                'Nama Sekolah',

            'npsn':
                'NPSN',

            'kategori':
                'Kategori Sekolah',

            'status':
                'Status Sekolah',

            'alamat':
                'Alamat',

            'zona_utm':
                'Zona UTM',

            'x_utm':
                'Koordinat X UTM',

            'y_utm':
                'Koordinat Y UTM',

            'foto':
                'Foto Sekolah',
        }


        widgets = {

            'nama':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Masukkan nama sekolah'
                        ),
                    }
                ),

            'npsn':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Masukkan NPSN'
                        ),
                    }
                ),

            'kategori':
                forms.Select(
                    attrs={
                        'class': 'form-select',
                    }
                ),

            'status':
                forms.Select(
                    attrs={
                        'class': 'form-select',
                    }
                ),

            'alamat':
                forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'rows': 2,
                        'placeholder': (
                            'Masukkan alamat sekolah'
                        ),
                    }
                ),

            'zona_utm':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Contoh: 50N'
                        ),
                    }
                ),

            'x_utm':
                forms.NumberInput(
                    attrs={
                        'class': 'form-control',
                        'step': '0.001',
                        'placeholder': (
                            'Contoh: 555123.456'
                        ),
                    }
                ),

            'y_utm':
                forms.NumberInput(
                    attrs={
                        'class': 'form-control',
                        'step': '0.001',
                        'placeholder': (
                            'Contoh: 123456.789'
                        ),
                    }
                ),

            'foto':
                forms.ClearableFileInput(
                    attrs={
                        'class': 'form-control',
                        'accept': (
                            '.jpg,.jpeg,.png'
                        ),
                    }
                ),
        }


    # =========================================================
    # INITIAL FORM
    # =========================================================

    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )


        # =====================================================
        # PILIHAN KECAMATAN
        # =====================================================

        self.fields[
            'kecamatan'
        ].choices = [

            (
                '',
                'Pilih Kecamatan'
            )

        ] + [

            (
                kecamatan,
                kecamatan
            )

            for kecamatan
            in DATA_WILAYAH.keys()

        ]


        # =====================================================
        # PILIHAN DESA
        # =====================================================

        semua_desa = []


        for daftar_desa in (
            DATA_WILAYAH.values()
        ):

            for desa in daftar_desa:

                semua_desa.append(
                    (
                        desa,
                        desa
                    )
                )


        self.fields[
            'desa'
        ].choices = [

            (
                '',
                'Pilih Desa'
            )

        ] + semua_desa



    # =========================================================
    # VALIDASI FOTO
    # =========================================================

    def clean_foto(
        self
    ):

        foto = (
            self.cleaned_data
            .get(
                'foto'
            )
        )


        if foto:


            # =================================================
            # UKURAN MAKSIMAL 2 MB
            # =================================================

            maksimal_ukuran = (
                2
                * 1024
                * 1024
            )


            if (
                foto.size
                > maksimal_ukuran
            ):

                raise forms.ValidationError(
                    'Ukuran foto maksimal 2 MB.'
                )



            # =================================================
            # FORMAT FILE
            # =================================================

            ekstensi_valid = [
                'jpg',
                'jpeg',
                'png',
            ]


            ekstensi = (
                foto.name
                .split('.')[-1]
                .lower()
            )


            if (
                ekstensi
                not in ekstensi_valid
            ):

                raise forms.ValidationError(
                    (
                        'Format foto harus '
                        'JPG, JPEG, atau PNG.'
                    )
                )


        return foto