from django.db import models
from sekolah.models import Sekolah
from murid.models import Murid


class Prestasi(models.Model):

    TINGKAT = (
        ('Sekolah', 'Sekolah'),
        ('Kecamatan', 'Kecamatan'),
        ('Kabupaten', 'Kabupaten'),
        ('Provinsi', 'Provinsi'),
        ('Nasional', 'Nasional'),
        ('Internasional', 'Internasional'),
    )

    JUARA = (
        ('Juara 1', 'Juara 1'),
        ('Juara 2', 'Juara 2'),
        ('Juara 3', 'Juara 3'),
        ('Harapan 1', 'Harapan 1'),
        ('Harapan 2', 'Harapan 2'),
        ('Harapan 3', 'Harapan 3'),
        ('Peserta', 'Peserta'),
    )

    sekolah = models.ForeignKey(
        Sekolah,
        on_delete=models.CASCADE,
        related_name='prestasi'
    )

    murid = models.ForeignKey(
        Murid,
        on_delete=models.CASCADE,
        related_name='daftar_prestasi'
    )

    nama_lomba = models.CharField(max_length=255)
    bidang_lomba = models.CharField(max_length=150)

    tingkat = models.CharField(max_length=50, choices=TINGKAT)
    juara = models.CharField(max_length=50, choices=JUARA)

    tahun = models.IntegerField()

    keterangan = models.TextField(blank=True, null=True)

    bukti_foto = models.ImageField(
        upload_to='prestasi/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.murid.nama} - {self.nama_lomba}"