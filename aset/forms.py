from django import forms
from .models import (
    Aset,
    AsetSekolah,
    DataRombel,
    BidangTanahSekolah,
    LegalitasTanah,
    DokumenTanah,
)


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
    


class AsetSekolahForm(
    forms.ModelForm
):

    foto_1 = forms.ImageField(
        required=False,
        label='Foto 1',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'accept': (
                    'image/jpeg,'
                    'image/png'
                )
            }
        )
    )

    foto_2 = forms.ImageField(
        required=False,
        label='Foto 2',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'accept': (
                    'image/jpeg,'
                    'image/png'
                )
            }
        )
    )

    foto_3 = forms.ImageField(
        required=False,
        label='Foto 3',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'accept': (
                    'image/jpeg,'
                    'image/png'
                )
            }
        )
    )

    class Meta:

        model = AsetSekolah

        fields = [
            'ketersediaan',
            'jumlah_baik',
            'jumlah_rusak_ringan',
            'jumlah_rusak_berat',
            'keterangan',
        ]

        widgets = {

            'ketersediaan': forms.Select(
                attrs={
                    'class': (
                        'form-select '
                        'pilihan-ketersediaan'
                    )
                }
            ),

            'jumlah_baik': forms.NumberInput(
                attrs={
                    'class': (
                        'form-control '
                        'jumlah-kondisi'
                    ),
                    'min': 0
                }
            ),

            'jumlah_rusak_ringan':
                forms.NumberInput(
                    attrs={
                        'class': (
                            'form-control '
                            'jumlah-kondisi'
                        ),
                        'min': 0
                    }
                ),

            'jumlah_rusak_berat':
                forms.NumberInput(
                    attrs={
                        'class': (
                            'form-control '
                            'jumlah-kondisi'
                        ),
                        'min': 0
                    }
                ),

            'keterangan': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': (
                        'Tambahkan keterangan '
                        'apabila diperlukan'
                    )
                }
            ),
        }

        labels = {
            'ketersediaan':
                'Ketersediaan',

            'jumlah_baik':
                'Kondisi Baik',

            'jumlah_rusak_ringan':
                'Rusak Ringan',

            'jumlah_rusak_berat':
                'Rusak Berat',

            'keterangan':
                'Keterangan',
        }

    def clean_file_foto(
        self,
        foto
    ):

        if not foto:
            return foto

        maksimal_ukuran = (
            2 * 1024 * 1024
        )

        if foto.size > maksimal_ukuran:

            raise forms.ValidationError(
                'Ukuran setiap foto '
                'maksimal 2 MB.'
            )

        ekstensi_valid = [
            'jpg',
            'jpeg',
            'png'
        ]

        ekstensi = (
            foto.name
            .split('.')[-1]
            .lower()
        )

        if ekstensi not in ekstensi_valid:

            raise forms.ValidationError(
                'Format foto harus '
                'JPG, JPEG, atau PNG.'
            )

        return foto

    def clean_foto_1(self):

        return self.clean_file_foto(
            self.cleaned_data.get(
                'foto_1'
            )
        )

    def clean_foto_2(self):

        return self.clean_file_foto(
            self.cleaned_data.get(
                'foto_2'
            )
        )

    def clean_foto_3(self):

        return self.clean_file_foto(
            self.cleaned_data.get(
                'foto_3'
            )
        )

    def clean(self):

        cleaned_data = super().clean()

        ketersediaan = (
            cleaned_data.get(
                'ketersediaan'
            )
        )

        jumlah_baik = (
            cleaned_data.get(
                'jumlah_baik'
            )
            or 0
        )

        jumlah_rusak_ringan = (
            cleaned_data.get(
                'jumlah_rusak_ringan'
            )
            or 0
        )

        jumlah_rusak_berat = (
            cleaned_data.get(
                'jumlah_rusak_berat'
            )
            or 0
        )

        jumlah_total = (
            jumlah_baik
            + jumlah_rusak_ringan
            + jumlah_rusak_berat
        )

        foto_baru = [
            cleaned_data.get(
                'foto_1'
            ),
            cleaned_data.get(
                'foto_2'
            ),
            cleaned_data.get(
                'foto_3'
            ),
        ]

        if (
            ketersediaan
            == 'TIDAK_ADA'
            and jumlah_total > 0
        ):

            raise forms.ValidationError(
                'Jumlah kondisi harus 0 '
                'apabila aset dipilih '
                'Tidak Ada.'
            )

        if (
            ketersediaan
            == 'TIDAK_ADA'
            and any(foto_baru)
        ):

            raise forms.ValidationError(
                'Foto tidak dapat diunggah '
                'apabila aset dipilih '
                'Tidak Ada.'
            )

        if (
            ketersediaan == 'ADA'
            and jumlah_total == 0
        ):

            raise forms.ValidationError(
                'Isi sedikitnya satu jumlah '
                'kondisi apabila aset '
                'dipilih Ada.'
            )

        return cleaned_data
    

class DataRombelForm(
    forms.ModelForm
):

    class Meta:

        model = DataRombel

        fields = [
            'tingkat',
            'nama_kelas',
            'jumlah_rombel',
            'kapasitas_ideal',
            'keterangan',
        ]

        widgets = {

            'tingkat':
                forms.Select(
                    attrs={
                        'class': 'form-select'
                    }
                ),

            'nama_kelas':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Contoh: Kelas 1A'
                        )
                    }
                ),

            'jumlah_rombel':
                forms.NumberInput(
                    attrs={
                        'class': 'form-control',
                        'min': 1
                    }
                ),

            'kapasitas_ideal':
                forms.NumberInput(
                    attrs={
                        'class': 'form-control',
                        'min': 1
                    }
                ),

            'keterangan':
                forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'rows': 3,
                        'placeholder': (
                            'Tambahkan keterangan '
                            'apabila diperlukan'
                        )
                    }
                ),
        }

        labels = {

            'tingkat':
                'Tingkat Kelas',

            'nama_kelas':
                'Nama Kelas',

            'jumlah_rombel':
                'Jumlah Rombel',

            'kapasitas_ideal':
                'Kapasitas Ideal',

            'keterangan':
                'Keterangan',
        }


    def __init__(
        self,
        *args,
        sekolah=None,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        # =====================================================
        # PILIHAN TINGKAT BERDASARKAN JENJANG SEKOLAH
        # =====================================================

        if sekolah:

            kategori = (
                sekolah.kategori.nama
                if sekolah.kategori
                else ''
            )

            kategori = (
                kategori.upper()
            )


            if kategori == 'SD':

                self.fields[
                    'tingkat'
                ].choices = [
                    ('', 'Pilih Tingkat Kelas'),
                    (1, 'Kelas 1'),
                    (2, 'Kelas 2'),
                    (3, 'Kelas 3'),
                    (4, 'Kelas 4'),
                    (5, 'Kelas 5'),
                    (6, 'Kelas 6'),
                ]


            elif kategori == 'SMP':

                self.fields[
                    'tingkat'
                ].choices = [
                    ('', 'Pilih Tingkat Kelas'),
                    (7, 'Kelas 7'),
                    (8, 'Kelas 8'),
                    (9, 'Kelas 9'),
                ]


            else:

                self.fields[
                    'tingkat'
                ].choices = [
                    (
                        '',
                        'Pilih Tingkat Kelas'
                    ),
                ]


    def clean_nama_kelas(self):

        nama_kelas = (
            self.cleaned_data
            .get('nama_kelas')
        )

        if nama_kelas:

            nama_kelas = (
                nama_kelas.strip()
            )

        return nama_kelas


    def clean(self):

        cleaned_data = super().clean()

        jumlah_rombel = (
            cleaned_data.get(
                'jumlah_rombel'
            )
            or 0
        )

        kapasitas_ideal = (
            cleaned_data.get(
                'kapasitas_ideal'
            )
            or 0
        )

        if jumlah_rombel < 1:

            self.add_error(
                'jumlah_rombel',
                'Jumlah rombel minimal 1.'
            )

        if kapasitas_ideal < 1:

            self.add_error(
                'kapasitas_ideal',
                'Kapasitas ideal minimal 1 siswa.'
            )

        return cleaned_data


# =========================================================
# FORM DATA ROMBEL
# =========================================================

class DataRombelForm(
    forms.ModelForm
):

    class Meta:

        model = DataRombel

        fields = [
            'tingkat',
            'nama_kelas',
            'jumlah_rombel',
            'kapasitas_ideal',
            'keterangan',
        ]

        widgets = {

            'tingkat':
                forms.Select(
                    attrs={
                        'class': 'form-select'
                    }
                ),

            'nama_kelas':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Contoh: Kelas 1A'
                        )
                    }
                ),

            'jumlah_rombel':
                forms.NumberInput(
                    attrs={
                        'class': 'form-control',
                        'min': 1
                    }
                ),

            'kapasitas_ideal':
                forms.NumberInput(
                    attrs={
                        'class': 'form-control',
                        'min': 1
                    }
                ),

            'keterangan':
                forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'rows': 3,
                        'placeholder': (
                            'Tambahkan keterangan '
                            'apabila diperlukan'
                        )
                    }
                ),
        }

        labels = {

            'tingkat':
                'Tingkat Kelas',

            'nama_kelas':
                'Nama Kelas',

            'jumlah_rombel':
                'Jumlah Rombel',

            'kapasitas_ideal':
                'Kapasitas Ideal',

            'keterangan':
                'Keterangan',
        }


    def __init__(
        self,
        *args,
        sekolah=None,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        # =====================================================
        # PILIHAN TINGKAT BERDASARKAN JENJANG SEKOLAH
        # =====================================================

        if sekolah:

            kategori = (
                sekolah.kategori.nama
                if sekolah.kategori
                else ''
            )

            kategori = (
                kategori.upper()
            )


            if kategori == 'SD':

                self.fields[
                    'tingkat'
                ].choices = [
                    ('', 'Pilih Tingkat Kelas'),
                    (1, 'Kelas 1'),
                    (2, 'Kelas 2'),
                    (3, 'Kelas 3'),
                    (4, 'Kelas 4'),
                    (5, 'Kelas 5'),
                    (6, 'Kelas 6'),
                ]


            elif kategori == 'SMP':

                self.fields[
                    'tingkat'
                ].choices = [
                    ('', 'Pilih Tingkat Kelas'),
                    (7, 'Kelas 7'),
                    (8, 'Kelas 8'),
                    (9, 'Kelas 9'),
                ]


            else:

                self.fields[
                    'tingkat'
                ].choices = [
                    (
                        '',
                        'Pilih Tingkat Kelas'
                    ),
                ]


    def clean_nama_kelas(self):

        nama_kelas = (
            self.cleaned_data
            .get('nama_kelas')
        )

        if nama_kelas:

            nama_kelas = (
                nama_kelas.strip()
            )

        return nama_kelas


    def clean(self):

        cleaned_data = super().clean()

        jumlah_rombel = (
            cleaned_data.get(
                'jumlah_rombel'
            )
            or 0
        )

        kapasitas_ideal = (
            cleaned_data.get(
                'kapasitas_ideal'
            )
            or 0
        )

        if jumlah_rombel < 1:

            self.add_error(
                'jumlah_rombel',
                'Jumlah rombel minimal 1.'
            )

        if kapasitas_ideal < 1:

            self.add_error(
                'kapasitas_ideal',
                'Kapasitas ideal minimal 1 siswa.'
            )

        return cleaned_data



# =========================================================
# BIDANG TANAH SEKOLAH
# =========================================================

class BidangTanahSekolahForm(
    forms.ModelForm
):

    class Meta:

        model = BidangTanahSekolah

        fields = [
            'luas_bidang_m2',
            'status_kepemilikan',
            'keterangan',
        ]

        widgets = {

            'luas_bidang_m2':
                forms.TextInput(
                    attrs={
                        'class': (
                            'form-control '
                            'input-luas-tanah'
                        ),
                        'inputmode': 'numeric',
                        'placeholder': (
                            'Contoh: 25.000'
                        ),
                    }
                ),

            'status_kepemilikan':
                forms.Select(
                    attrs={
                        'class': 'form-select'
                    }
                ),

            'keterangan':
                forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'rows': 3,
                        'placeholder': (
                            'Tambahkan keterangan '
                            'apabila diperlukan'
                        )
                    }
                ),
        }

        labels = {

            'luas_bidang_m2':
                'Luas Bidang (m²)',

            'status_kepemilikan':
                'Status Kepemilikan',

            'keterangan':
                'Keterangan',
        }


    def clean_luas_bidang_m2(self):

        luas = (
            self.cleaned_data.get(
                'luas_bidang_m2'
            )
        )

        if (
            luas is not None
            and luas <= 0
        ):

            raise forms.ValidationError(
                'Luas bidang harus lebih dari 0.'
            )

        return luas


# =========================================================
# LEGALITAS TANAH
# =========================================================

class LegalitasTanahForm(
    forms.ModelForm
):

    class Meta:

        model = LegalitasTanah

        fields = [
            'jenis_dokumen',
            'nama_dokumen',
            'nomor_dokumen',
            'tanggal_dokumen',
            'atas_nama',
            'keterangan',
        ]

        widgets = {

            'jenis_dokumen':
                forms.Select(
                    attrs={
                        'class': (
                            'form-select '
                            'pilihan-jenis-dokumen'
                        )
                    }
                ),

            'nama_dokumen':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Isi apabila memilih '
                            'Dokumen Lainnya'
                        )
                    }
                ),

            'nomor_dokumen':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Nomor dokumen'
                        )
                    }
                ),

            'tanggal_dokumen':
                forms.DateInput(
                    format='%Y-%m-%d',
                    attrs={
                        'class': 'form-control',
                        'type': 'date'
                    }
                ),

            'atas_nama':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Nama pemegang / '
                            'penerima hak'
                        )
                    }
                ),

            'keterangan':
                forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'rows': 3,
                        'placeholder': (
                            'Tambahkan keterangan '
                            'apabila diperlukan'
                        )
                    }
                ),
        }

        labels = {

            'jenis_dokumen':
                'Jenis Dokumen',

            'nama_dokumen':
                'Nama Dokumen Lainnya',

            'nomor_dokumen':
                'Nomor Dokumen',

            'tanggal_dokumen':
                'Tanggal Dokumen',

            'atas_nama':
                'Atas Nama',

            'keterangan':
                'Keterangan',
        }


    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        self.fields[
            'tanggal_dokumen'
        ].input_formats = [
            '%Y-%m-%d'
        ]


    def clean(self):

        cleaned_data = (
            super().clean()
        )

        jenis_dokumen = (
            cleaned_data.get(
                'jenis_dokumen'
            )
        )

        nama_dokumen = (
            cleaned_data.get(
                'nama_dokumen'
            )
        )


        # =============================================
        # DOKUMEN LAINNYA WAJIB DIJELASKAN
        # =============================================

        if (
            jenis_dokumen == 'LAINNYA'
            and not nama_dokumen
        ):

            self.add_error(
                'nama_dokumen',
                (
                    'Nama dokumen wajib diisi '
                    'apabila memilih '
                    'Dokumen Lainnya.'
                )
            )


        # =============================================
        # BERSIHKAN NAMA DOKUMEN
        # =============================================

        if nama_dokumen:

            cleaned_data[
                'nama_dokumen'
            ] = nama_dokumen.strip()


        return cleaned_data


# =========================================================
# DOKUMEN / LAMPIRAN LEGALITAS
# =========================================================

class DokumenTanahForm(
    forms.ModelForm
):

    class Meta:

        model = DokumenTanah

        fields = [
            'file',
            'keterangan',
        ]

        widgets = {

            'file':
                forms.ClearableFileInput(
                    attrs={
                        'class': 'form-control',
                        'accept': (
                            '.pdf,.jpg,.jpeg,.png'
                        )
                    }
                ),

            'keterangan':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Keterangan lampiran '
                            '(opsional)'
                        )
                    }
                ),
        }

        labels = {

            'file':
                'File Dokumen',

            'keterangan':
                'Keterangan',
        }


    def clean_file(self):

        dokumen = (
            self.cleaned_data.get(
                'file'
            )
        )

        if not dokumen:

            return dokumen


        # =============================================
        # BATAS UKURAN 5 MB
        # =============================================

        maksimal_ukuran = (
            5 * 1024 * 1024
        )

        if (
            dokumen.size
            > maksimal_ukuran
        ):

            raise forms.ValidationError(
                'Ukuran dokumen maksimal 5 MB.'
            )


        # =============================================
        # FORMAT FILE
        # =============================================

        ekstensi_valid = [
            'pdf',
            'jpg',
            'jpeg',
            'png',
        ]

        ekstensi = (
            dokumen.name
            .split('.')[-1]
            .lower()
        )

        if (
            ekstensi
            not in ekstensi_valid
        ):

            raise forms.ValidationError(
                'Format dokumen harus PDF, '
                'JPG, JPEG, atau PNG.'
            )


        return dokumen