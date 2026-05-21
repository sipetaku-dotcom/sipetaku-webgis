from django.db import models
from sekolah.models import Sekolah


class Aset(models.Model):

    KONDISI = (
        ('Baik', 'Baik'),
        ('Rusak Ringan', 'Rusak Ringan'),
        ('Rusak Berat', 'Rusak Berat'),
    )

    sekolah = models.ForeignKey(
        Sekolah,
        on_delete=models.CASCADE,
        related_name='aset'
    )

    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=100)
    jumlah = models.IntegerField(default=0)
    kondisi = models.CharField(max_length=30, choices=KONDISI)
    keterangan = models.TextField(blank=True, null=True)

    foto = models.ImageField(
        upload_to='aset/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama