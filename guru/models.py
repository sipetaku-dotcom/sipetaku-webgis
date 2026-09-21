from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from sekolah.models import Sekolah


# =========================================================
# PEGAWAI
# =========================================================

class Pegawai(models.Model):

    JENIS_KELAMIN = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )


    # =====================================================
    # IDENTITAS
    # =====================================================

    nama = models.CharField(
        max_length=255
    )

    nip = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )

    nik = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        unique=True
    )

    nuptk = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        unique=True
    )


    # =====================================================
    # DATA PRIBADI
    # =====================================================

    jenis_kelamin = models.CharField(
        max_length=1,
        choices=JENIS_KELAMIN
    )

    tempat_lahir = models.CharField(
        max_length=100
    )

    tanggal_lahir = models.DateField()

    alamat = models.TextField(
        blank=True,
        null=True
    )

    no_hp = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )


    # =====================================================
    # TIMESTAMP
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    # =====================================================
    # META
    # =====================================================

    class Meta:

        ordering = (
            'nama',
        )

        verbose_name = (
            'pegawai'
        )

        verbose_name_plural = (
            'pegawai'
        )


    # =====================================================
    # VALIDASI / NORMALISASI
    # =====================================================

    def clean(self):

        super().clean()


        # ---------------------------------------------
        # NAMA
        # ---------------------------------------------

        if self.nama:

            self.nama = (
                self.nama.strip()
            )


        # ---------------------------------------------
        # NIP
        # ---------------------------------------------

        if self.nip:

            self.nip = (
                self.nip.strip()
            )

        else:

            self.nip = None


        # ---------------------------------------------
        # NIK
        # ---------------------------------------------

        if self.nik:

            self.nik = (
                self.nik.strip()
            )

        else:

            self.nik = None


        # ---------------------------------------------
        # NUPTK
        # ---------------------------------------------

        if self.nuptk:

            self.nuptk = (
                self.nuptk.strip()
            )

        else:

            self.nuptk = None


        # ---------------------------------------------
        # TEMPAT LAHIR
        # ---------------------------------------------

        if self.tempat_lahir:

            self.tempat_lahir = (
                self.tempat_lahir.strip()
            )


        # ---------------------------------------------
        # NO HP
        # ---------------------------------------------

        if self.no_hp:

            self.no_hp = (
                self.no_hp.strip()
            )

        else:

            self.no_hp = None


        # ---------------------------------------------
        # ALAMAT
        # ---------------------------------------------

        if self.alamat:

            self.alamat = (
                self.alamat.strip()
            )

        else:

            self.alamat = None


    # =====================================================
    # SAVE
    # =====================================================

    def save(
        self,
        *args,
        **kwargs
    ):

        self.full_clean()

        super().save(
            *args,
            **kwargs
        )


    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return self.nama



# =========================================================
# RIWAYAT PEGAWAI
# =========================================================

class RiwayatPegawai(models.Model):


    # =====================================================
    # JENIS PEGAWAI
    # =====================================================

    JENIS_PEGAWAI = (

        (
            'PENDIDIK',
            'Guru / Pendidik'
        ),

        (
            'TENAGA_KEPENDIDIKAN',
            'Tenaga Kependidikan'
        ),
    )


    # =====================================================
    # STATUS KEPEGAWAIAN
    # =====================================================

    STATUS_PEGAWAI = (

        (
            'PNS',
            'PNS'
        ),

        (
            'PPPK',
            'PPPK'
        ),

        (
            'HONORER',
            'Honorer'
        ),

        (
            'GTY',
            'GTY'
        ),

        (
            'GTT',
            'GTT'
        ),
    )


    # =====================================================
    # STATUS AKHIR RIWAYAT
    # =====================================================

    STATUS_AKHIR = (

        (
            'AKTIF',
            'Aktif'
        ),

        (
            'MUTASI',
            'Mutasi'
        ),

        (
            'PENSIUN',
            'Pensiun'
        ),

        (
            'BERHENTI',
            'Berhenti'
        ),

        (
            'MENINGGAL',
            'Meninggal'
        ),
    )


    # =====================================================
    # RELASI
    # =====================================================

    pegawai = models.ForeignKey(
        Pegawai,
        on_delete=models.CASCADE,
        related_name='riwayat_penempatan'
    )

    sekolah = models.ForeignKey(
        Sekolah,
        on_delete=models.PROTECT,
        related_name='riwayat_pegawai'
    )

    tahun_ajaran = models.ForeignKey(
        'murid.TahunAjaran',
        on_delete=models.PROTECT,
        related_name='riwayat_pegawai'
    )


    # =====================================================
    # DATA PENEMPATAN
    # =====================================================

    jenis_pegawai = models.CharField(
        max_length=30,
        choices=JENIS_PEGAWAI
    )

    jabatan = models.CharField(
        max_length=100
    )

    mata_pelajaran = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    status_pegawai = models.CharField(
        max_length=30,
        choices=STATUS_PEGAWAI
    )

    status_akhir = models.CharField(
        max_length=30,
        choices=STATUS_AKHIR,
        default='AKTIF'
    )


    # =====================================================
    # PERIODE
    # =====================================================

    tanggal_mulai = models.DateField(
        blank=True,
        null=True
    )

    tanggal_selesai = models.DateField(
        blank=True,
        null=True
    )

    tanggal_pensiun = models.DateField(
        blank=True,
        null=True
    )


    # =====================================================
    # KETERANGAN
    # =====================================================

    keterangan = models.TextField(
        blank=True
    )


    # =====================================================
    # TIMESTAMP
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    # =====================================================
    # META
    # =====================================================

    class Meta:

        ordering = (
            '-tahun_ajaran__nama',
            'sekolah__nama',
            'pegawai__nama',
        )


        constraints = [

            models.UniqueConstraint(

                fields=(
                    'pegawai',
                    'tahun_ajaran'
                ),

                condition=Q(
                    status_akhir='AKTIF'
                ),

                name=(
                    'unik_pegawai_aktif_'
                    'per_tahun_ajaran'
                )
            ),

        ]


        verbose_name = (
            'riwayat pegawai'
        )

        verbose_name_plural = (
            'riwayat pegawai'
        )


    # =====================================================
    # VALIDASI
    # =====================================================

    def clean(self):

        super().clean()


        # ---------------------------------------------
        # JABATAN WAJIB
        # ---------------------------------------------

        if self.jabatan:

            self.jabatan = (
                self.jabatan.strip()
            )


        # ---------------------------------------------
        # TENAGA KEPENDIDIKAN TIDAK PUNYA MAPEL
        # ---------------------------------------------

        if (
            self.jenis_pegawai
            == 'TENAGA_KEPENDIDIKAN'
        ):

            self.mata_pelajaran = None


        # ---------------------------------------------
        # NORMALISASI MAPEL
        # ---------------------------------------------

        elif self.mata_pelajaran:

            self.mata_pelajaran = (
                self.mata_pelajaran.strip()
            )


        # ---------------------------------------------
        # VALIDASI TANGGAL
        # ---------------------------------------------

        if (
            self.tanggal_mulai
            and
            self.tanggal_selesai
            and
            self.tanggal_selesai
            < self.tanggal_mulai
        ):

            raise ValidationError({

                'tanggal_selesai':
                    (
                        'Tanggal selesai tidak boleh '
                        'lebih awal dari tanggal mulai.'
                    )

            })


        # ---------------------------------------------
        # STATUS AKTIF TIDAK BOLEH SUDAH SELESAI
        # ---------------------------------------------

        if (
            self.status_akhir == 'AKTIF'
            and
            self.tanggal_selesai
        ):

            raise ValidationError({

                'tanggal_selesai':
                    (
                        'Riwayat yang masih aktif '
                        'tidak boleh memiliki '
                        'tanggal selesai.'
                    )

            })


        # ---------------------------------------------
        # STATUS SELESAI
        # ---------------------------------------------

        if (
            self.status_akhir
            in (
                'MUTASI',
                'PENSIUN',
                'BERHENTI',
                'MENINGGAL',
            )
            and
            not self.tanggal_selesai
        ):

            raise ValidationError({

                'tanggal_selesai':
                    (
                        'Tanggal selesai wajib diisi '
                        'untuk riwayat yang sudah '
                        'tidak aktif.'
                    )

            })


        # ---------------------------------------------
        # PENSIUN
        # ---------------------------------------------

        if (
            self.status_akhir == 'PENSIUN'
            and
            not self.tanggal_pensiun
        ):

            raise ValidationError({

                'tanggal_pensiun':
                    (
                        'Tanggal pensiun wajib diisi '
                        'jika status akhir Pensiun.'
                    )

            })


    # =====================================================
    # SAVE
    # =====================================================

    def save(
        self,
        *args,
        **kwargs
    ):

        self.full_clean()

        super().save(
            *args,
            **kwargs
        )


    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return (
            f'{self.pegawai.nama} - '
            f'{self.sekolah.nama} - '
            f'{self.tahun_ajaran.nama}'
        )