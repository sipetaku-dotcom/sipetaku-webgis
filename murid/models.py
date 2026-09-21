from django.db import models
from sekolah.models import Sekolah

class TahunAjaran(models.Model):

    nama = models.CharField(
        max_length=20,
        unique=True
    )

    aktif = models.BooleanField(
        default=False
    )

    tahun_sebelumnya = models.OneToOneField(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tahun_berikutnya'
    )

    tanggal_mulai = models.DateField(
        blank=True,
        null=True
    )

    tanggal_selesai = models.DateField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ('-nama',)

        verbose_name = 'tahun ajaran'
        verbose_name_plural = 'tahun ajaran'

    def save(self, *args, **kwargs):

        if self.aktif:

            TahunAjaran.objects.exclude(
                pk=self.pk
            ).update(
                aktif=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama


class Murid(models.Model):

    JENIS_KELAMIN = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )

    sekolah = models.ForeignKey(
        Sekolah,
        on_delete=models.CASCADE,
        related_name='murid'
    )

    nama = models.CharField(max_length=255)
    nisn = models.CharField(
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

    jenis_kelamin = models.CharField(
        max_length=1,
        choices=JENIS_KELAMIN
    )

    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()

    kelas = models.CharField(max_length=20)
    alamat = models.TextField(blank=True, null=True)

    prestasi = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama


class RiwayatMurid(models.Model):

    STATUS_MASUK = (
        ('SISWA_BARU', 'Siswa Baru'),
        ('NAIK_KELAS', 'Naik Kelas'),
        ('TINGGAL_KELAS', 'Tinggal Kelas'),
        ('PINDAHAN', 'Siswa Pindahan'),
        ('LANJUT', 'Lanjutan'),
    )

    STATUS_AKHIR = (
        ('AKTIF', 'Aktif'),
        ('NAIK_KELAS', 'Naik Kelas'),
        ('TINGGAL_KELAS', 'Tinggal Kelas'),
        ('LULUS', 'Lulus'),
        ('PINDAH', 'Pindah'),
        ('KELUAR', 'Keluar'),
    )

    murid = models.ForeignKey(
        Murid,
        on_delete=models.CASCADE,
        related_name='riwayat_akademik'
    )

    rombel = models.ForeignKey(
        'aset.DataRombel',
        on_delete=models.PROTECT,
        related_name='riwayat_murid'
    )

    tahun_ajaran = models.ForeignKey(
        TahunAjaran,
        on_delete=models.PROTECT,
        related_name='riwayat_murid'
    )

    status_masuk = models.CharField(
        max_length=30,
        choices=STATUS_MASUK,
        default='SISWA_BARU'
    )

    status_akhir = models.CharField(
        max_length=30,
        choices=STATUS_AKHIR,
        default='AKTIF'
    )

    tahun_lulus = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    keterangan = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = (
            '-tahun_ajaran__nama',
            'rombel__nama_kelas',
            'murid__nama',
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    'murid',
                    'tahun_ajaran'
                ),
                name='unik_murid_per_tahun_ajaran'
            ),
        ]

        verbose_name = 'riwayat murid'
        verbose_name_plural = 'riwayat murid'

    def clean(self):

        super().clean()

        if (
            self.rombel_id
            and
            self.tahun_ajaran_id
            and
            self.rombel.tahun_ajaran_id
            != self.tahun_ajaran_id
        ):

            from django.core.exceptions import ValidationError

            raise ValidationError(
                'Tahun ajaran riwayat harus sama '
                'dengan tahun ajaran rombel.'
            )

        if (
            self.rombel_id
            and
            self.murid_id
            and
            self.rombel.sekolah_id
            != self.murid.sekolah_id
        ):

            from django.core.exceptions import ValidationError

            raise ValidationError(
                'Rombel dan murid harus berasal '
                'dari sekolah yang sama.'
            )

    def __str__(self):

        return (
            f'{self.murid.nama} - '
            f'{self.rombel.nama_kelas} - '
            f'{self.tahun_ajaran.nama}'
        )