from django.db import models
from sekolah.models import Sekolah


class Guru(models.Model):

    JENIS_KELAMIN = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )

    STATUS_PEGAWAI = (
        ('PNS', 'PNS'),
        ('PPPK', 'PPPK'),
        ('Honorer', 'Honorer'),
        ('GTY', 'GTY'),
        ('GTT', 'GTT'),
    )

    sekolah = models.ForeignKey(
        Sekolah,
        on_delete=models.CASCADE,
        related_name='guru'
    )

    nama = models.CharField(max_length=255)
    nip = models.CharField(max_length=50, blank=True, null=True)
    nik = models.CharField(max_length=30, blank=True, null=True)

    jenis_kelamin = models.CharField(
        max_length=1,
        choices=JENIS_KELAMIN
    )

    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()

    jabatan = models.CharField(max_length=100)
    status_pegawai = models.CharField(
        max_length=30,
        choices=STATUS_PEGAWAI
    )

    mata_pelajaran = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    tanggal_pensiun = models.DateField(
        blank=True,
        null=True
    )

    alamat = models.TextField(blank=True, null=True)
    no_hp = models.CharField(max_length=30, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama