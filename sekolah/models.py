from django.db import models
from pyproj import Transformer
from django.contrib.auth.models import User


class KategoriSekolah(models.Model):
    nama = models.CharField(max_length=100, unique=True)

    warna_marker = models.CharField(
        max_length=50,
        default='blue'
    )

    def __str__(self):
        return self.nama


class Sekolah(models.Model):

    STATUS = (
        ('Negeri', 'Negeri'),
        ('Swasta', 'Swasta'),
    )

    nama = models.CharField(max_length=255)
    npsn = models.CharField(max_length=50, unique=True)

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='sekolah_operator'
    )

    kategori = models.ForeignKey(
        KategoriSekolah,
        on_delete=models.CASCADE,
        related_name='sekolah'
    )

    status = models.CharField(max_length=20, choices=STATUS)

    alamat = models.TextField()
    kecamatan = models.CharField(max_length=100)
    desa = models.CharField(max_length=100)

    x_utm = models.FloatField(verbose_name="Easting / X UTM")
    y_utm = models.FloatField(verbose_name="Northing / Y UTM")
    zona_utm = models.CharField(max_length=10, default="50N")

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    jumlah_murid = models.IntegerField(default=0)
    jumlah_guru = models.IntegerField(default=0)

    foto = models.ImageField(upload_to='sekolah/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.x_utm and self.y_utm:
            transformer = Transformer.from_crs(
                "EPSG:32650",
                "EPSG:4326",
                always_xy=True
            )

            lon, lat = transformer.transform(self.x_utm, self.y_utm)

            self.longitude = lon
            self.latitude = lat

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama