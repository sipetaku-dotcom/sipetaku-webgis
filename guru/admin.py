from django.contrib import admin

from .models import (
    Pegawai,
    RiwayatPegawai,
)


@admin.register(Pegawai)
class PegawaiAdmin(admin.ModelAdmin):

    list_display = (
        'nama',
        'nip',
        'nik',
        'nuptk',
        'jenis_kelamin',
    )

    search_fields = (
        'nama',
        'nip',
        'nik',
        'nuptk',
    )

    list_filter = (
        'jenis_kelamin',
    )


@admin.register(RiwayatPegawai)
class RiwayatPegawaiAdmin(admin.ModelAdmin):

    list_display = (
        'pegawai',
        'sekolah',
        'tahun_ajaran',
        'jenis_pegawai',
        'jabatan',
        'status_pegawai',
        'status_akhir',
    )

    search_fields = (
        'pegawai__nama',
        'pegawai__nip',
        'pegawai__nik',
        'pegawai__nuptk',
        'sekolah__nama',
        'jabatan',
        'mata_pelajaran',
    )

    list_filter = (
        'jenis_pegawai',
        'status_pegawai',
        'status_akhir',
        'tahun_ajaran',
    )