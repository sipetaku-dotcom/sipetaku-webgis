from django.db import models
from sekolah.models import Sekolah


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
    nisn = models.CharField(max_length=50, blank=True, null=True)
    nik = models.CharField(max_length=30, blank=True, null=True)

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