from django.db import models
from django.contrib.auth.models import User


class ProfilUser(models.Model):

    ROLE = (
        ('admin_kabupaten', 'Admin Kabupaten'),
        ('admin_kecamatan', 'Admin Kecamatan'),
        ('operator_sekolah', 'Operator Sekolah'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil'
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE
    )

    kecamatan = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"