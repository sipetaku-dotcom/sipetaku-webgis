from django.contrib import admin

from .models import (
    KategoriSekolah,
    Sekolah,
)


@admin.register(KategoriSekolah)
class KategoriSekolahAdmin(
    admin.ModelAdmin
):

    list_display = (
        'nama',
        'warna_marker'
    )

    search_fields = (
        'nama',
    )


@admin.register(Sekolah)
class SekolahAdmin(
    admin.ModelAdmin
):

    list_display = (
        'nama',
        'npsn',
        'kategori',
        'status',
        'kecamatan',
        'desa'
    )

    list_filter = (
        'kategori',
        'status',
        'kecamatan'
    )

    search_fields = (
        'nama',
        'npsn',
        'kecamatan',
        'desa'
    )

    ordering = (
        'nama',
    )