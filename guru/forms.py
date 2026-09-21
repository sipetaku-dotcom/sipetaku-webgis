from django import forms

from .models import (
    Pegawai,
    RiwayatPegawai,
)

from sekolah.models import Sekolah


# =========================================================
# FORM PEGAWAI
# =========================================================

class PegawaiForm(forms.ModelForm):

    class Meta:

        model = Pegawai

        fields = [
            'nama',
            'nip',
            'nik',
            'nuptk',
            'jenis_kelamin',
            'tempat_lahir',
            'tanggal_lahir',
            'alamat',
            'no_hp',
        ]

        widgets = {

            'nama':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Nama lengkap pegawai'
                    }
                ),

            'nip':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'NIP jika tersedia'
                        )
                    }
                ),

            'nik':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'NIK'
                    }
                ),

            'nuptk':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'NUPTK jika tersedia'
                        )
                    }
                ),

            'jenis_kelamin':
                forms.Select(
                    attrs={
                        'class': 'form-select'
                    }
                ),

            'tempat_lahir':
                forms.TextInput(
                    attrs={
                        'class': 'form-control'
                    }
                ),

            'tanggal_lahir':
                forms.DateInput(
                    format='%Y-%m-%d',
                    attrs={
                        'class': 'form-control',
                        'type': 'date'
                    }
                ),

            'alamat':
                forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'rows': 2
                    }
                ),

            'no_hp':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Nomor HP / WhatsApp'
                        )
                    }
                ),
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
            'tanggal_lahir'
        ].input_formats = [
            '%Y-%m-%d'
        ]


    # =====================================================
    # NIP
    # =====================================================

    def clean_nip(self):

        nip = (
            self.cleaned_data
            .get('nip')
        )

        if nip:

            nip = nip.strip()

            qs = (
                Pegawai.objects
                .filter(
                    nip=nip
                )
            )

            if self.instance.pk:

                qs = qs.exclude(
                    pk=self.instance.pk
                )

            if qs.exists():

                raise forms.ValidationError(
                    'NIP ini sudah digunakan '
                    'oleh pegawai lain.'
                )

            return nip

        return None


    # =====================================================
    # NIK
    # =====================================================

    def clean_nik(self):

        nik = (
            self.cleaned_data
            .get('nik')
        )

        if nik:

            nik = nik.strip()

            qs = (
                Pegawai.objects
                .filter(
                    nik=nik
                )
            )

            if self.instance.pk:

                qs = qs.exclude(
                    pk=self.instance.pk
                )

            if qs.exists():

                raise forms.ValidationError(
                    'NIK ini sudah digunakan '
                    'oleh pegawai lain.'
                )

            return nik

        return None


    # =====================================================
    # NUPTK
    # =====================================================

    def clean_nuptk(self):

        nuptk = (
            self.cleaned_data
            .get('nuptk')
        )

        if nuptk:

            nuptk = nuptk.strip()

            qs = (
                Pegawai.objects
                .filter(
                    nuptk=nuptk
                )
            )

            if self.instance.pk:

                qs = qs.exclude(
                    pk=self.instance.pk
                )

            if qs.exists():

                raise forms.ValidationError(
                    'NUPTK ini sudah digunakan '
                    'oleh pegawai lain.'
                )

            return nuptk

        return None



# =========================================================
# FORM RIWAYAT PEGAWAI
# =========================================================

class RiwayatPegawaiForm(
    forms.ModelForm
):

    class Meta:

        model = RiwayatPegawai

        fields = [
            'jenis_pegawai',
            'jabatan',
            'mata_pelajaran',
            'status_pegawai',
            'tanggal_mulai',
            'tanggal_pensiun',
            'keterangan',
        ]

        widgets = {

            'jenis_pegawai':
                forms.Select(
                    attrs={
                        'class': 'form-select'
                    }
                ),

            'jabatan':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Contoh: Kepala Sekolah, '
                            'Guru Matematika, Kepala TU'
                        )
                    }
                ),

            'mata_pelajaran':
                forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': (
                            'Isi jika pegawai '
                            'merupakan pendidik'
                        )
                    }
                ),

            'status_pegawai':
                forms.Select(
                    attrs={
                        'class': 'form-select'
                    }
                ),

            'tanggal_mulai':
                forms.DateInput(
                    format='%Y-%m-%d',
                    attrs={
                        'class': 'form-control',
                        'type': 'date'
                    }
                ),

            'tanggal_pensiun':
                forms.DateInput(
                    format='%Y-%m-%d',
                    attrs={
                        'class': 'form-control',
                        'type': 'date'
                    }
                ),

            'keterangan':
                forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'rows': 2,
                        'placeholder': (
                            'Keterangan tambahan '
                            'jika diperlukan'
                        )
                    }
                ),
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
            'tanggal_mulai'
        ].input_formats = [
            '%Y-%m-%d'
        ]

        self.fields[
            'tanggal_pensiun'
        ].input_formats = [
            '%Y-%m-%d'
        ]


    # =====================================================
    # VALIDASI
    # =====================================================

    def clean(self):

        cleaned_data = (
            super().clean()
        )

        jenis_pegawai = (
            cleaned_data.get(
                'jenis_pegawai'
            )
        )

        mata_pelajaran = (
            cleaned_data.get(
                'mata_pelajaran'
            )
        )


        # Tenaga kependidikan tidak memakai mapel.
        if (
            jenis_pegawai
            == 'TENAGA_KEPENDIDIKAN'
        ):

            cleaned_data[
                'mata_pelajaran'
            ] = None


        # Jika pendidik dan mapel diisi,
        # bersihkan spasi.
        elif mata_pelajaran:

            cleaned_data[
                'mata_pelajaran'
            ] = (
                mata_pelajaran.strip()
            )


        return cleaned_data


class MutasiPegawaiForm(forms.Form):

    sekolah_tujuan = forms.ModelChoiceField(
        queryset=Sekolah.objects.none(),
        required=True,
        label='Sekolah Tujuan',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    tanggal_mutasi = forms.DateField(
        required=True,
        label='Tanggal Mutasi',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    jenis_pegawai = forms.ChoiceField(
        choices=RiwayatPegawai.JENIS_PEGAWAI,
        required=True,
        label='Jenis Pegawai',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    jabatan = forms.CharField(
        max_length=100,
        required=True,
        label='Jabatan di Sekolah Tujuan',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    mata_pelajaran = forms.CharField(
        max_length=100,
        required=False,
        label='Mata Pelajaran',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    status_pegawai = forms.ChoiceField(
        choices=RiwayatPegawai.STATUS_PEGAWAI,
        required=True,
        label='Status Kepegawaian',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    keterangan = forms.CharField(
        required=False,
        label='Keterangan',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 2
            }
        )
    )


    def __init__(
        self,
        *args,
        sekolah_asal=None,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        queryset = (
            Sekolah.objects
            .all()
            .order_by(
                'kecamatan',
                'nama'
            )
        )

        if sekolah_asal:

            queryset = queryset.exclude(
                pk=sekolah_asal.pk
            )

        self.fields[
            'sekolah_tujuan'
        ].queryset = queryset

        self.fields[
            'tanggal_mutasi'
        ].input_formats = [
            '%Y-%m-%d'
        ]


    def clean(self):

        cleaned_data = super().clean()

        jenis_pegawai = (
            cleaned_data.get(
                'jenis_pegawai'
            )
        )

        mata_pelajaran = (
            cleaned_data.get(
                'mata_pelajaran'
            )
        )

        if (
            jenis_pegawai
            == 'TENAGA_KEPENDIDIKAN'
        ):

            cleaned_data[
                'mata_pelajaran'
            ] = None

        elif mata_pelajaran:

            cleaned_data[
                'mata_pelajaran'
            ] = (
                mata_pelajaran.strip()
            )

        return cleaned_data


class AkhiriPegawaiForm(forms.Form):

    STATUS_AKHIR = (
        ('PENSIUN', 'Pensiun'),
        ('BERHENTI', 'Berhenti'),
        ('MENINGGAL', 'Meninggal'),
    )

    status_akhir = forms.ChoiceField(
        choices=STATUS_AKHIR,
        required=True,
        label='Status Akhir',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    tanggal_selesai = forms.DateField(
        required=True,
        label='Tanggal Efektif',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    keterangan = forms.CharField(
        required=False,
        label='Keterangan',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': (
                    'Nomor SK, alasan berhenti, '
                    'atau keterangan lainnya'
                )
            }
        )
    )

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
            'tanggal_selesai'
        ].input_formats = [
            '%Y-%m-%d'
        ]