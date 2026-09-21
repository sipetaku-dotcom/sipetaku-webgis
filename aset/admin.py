from django.contrib import admin

from .models import (
    Aset,
    AsetSekolah,
    DataRombel,
    BidangTanahSekolah,
    LegalitasTanah,
    DokumenTanah,
    FotoAset,
    JenisAset,
)


@admin.register(Aset)
class AsetLamaAdmin(admin.ModelAdmin):

    list_display = (
        'nama',
        'sekolah',
        'kategori',
        'jumlah',
        'kondisi'
    )

    list_filter = (
        'kategori',
        'kondisi'
    )

    search_fields = (
        'nama',
        'sekolah__nama',
        'sekolah__npsn'
    )


@admin.register(JenisAset)
class JenisAsetAdmin(admin.ModelAdmin):

    list_display = (
        'nama',
        'kategori',
        'satuan',
        'aset_kritis',
        'aktif',
        'urutan'
    )

    list_filter = (
        'kategori',
        'aset_kritis',
        'aktif'
    )

    search_fields = (
        'nama',
        'kode'
    )

    ordering = (
        'kategori',
        'urutan'
    )

    list_editable = (
        'aset_kritis',
        'aktif'
    )


class FotoAsetInline(
    admin.TabularInline
):

    model = FotoAset

    extra = 0

    max_num = 3

    fields = (
        'urutan',
        'foto',
        'keterangan'
    )


@admin.register(AsetSekolah)
class AsetSekolahAdmin(
    admin.ModelAdmin
):

    list_display = (
        'sekolah',
        'jenis_aset',
        'ketersediaan',
        'jumlah_baik',
        'jumlah_rusak_ringan',
        'jumlah_rusak_berat',
        'tampilkan_jumlah_total',
        'diperbarui_pada'
    )

    list_filter = (
        'ketersediaan',
        'jenis_aset__kategori',
        'jenis_aset__aset_kritis'
    )

    search_fields = (
        'sekolah__nama',
        'sekolah__npsn',
        'jenis_aset__nama'
    )

    autocomplete_fields = (
        'sekolah',
        'jenis_aset'
    )

    readonly_fields = (
        'diperbarui_pada',
    )

    inlines = (
        FotoAsetInline,
    )

    @admin.display(
        description='Jumlah Total'
    )
    def tampilkan_jumlah_total(
        self,
        obj
    ):

        return obj.jumlah_total


# =========================================================
# LAMPIRAN LEGALITAS TANAH
# =========================================================

class DokumenTanahInline(
    admin.TabularInline
):

    model = DokumenTanah

    extra = 0

    fields = (
        'file',
        'nama_file',
        'keterangan',
        'diunggah_pada',
    )

    readonly_fields = (
        'diunggah_pada',
    )


# =========================================================
# LEGALITAS TANAH INLINE
# =========================================================

class LegalitasTanahInline(
    admin.TabularInline
):

    model = LegalitasTanah

    extra = 0

    fields = (
        'jenis_dokumen',
        'nama_dokumen',
        'nomor_dokumen',
        'tanggal_dokumen',
        'atas_nama',
    )

    show_change_link = True


# =========================================================
# BIDANG TANAH SEKOLAH
# =========================================================

@admin.register(BidangTanahSekolah)
class BidangTanahSekolahAdmin(
    admin.ModelAdmin
):

    list_display = (
        'sekolah',
        'nomor_bidang',
        'luas_bidang_m2',
        'status_kepemilikan',
        'tampilkan_jumlah_legalitas',
        'diperbarui_pada',
    )

    list_filter = (
        'status_kepemilikan',
        'sekolah__kategori',
        'sekolah__kecamatan',
    )

    search_fields = (
        'sekolah__nama',
        'sekolah__npsn',
        'keterangan',
    )

    autocomplete_fields = (
        'sekolah',
    )

    readonly_fields = (
        'dibuat_pada',
        'diperbarui_pada',
    )

    ordering = (
        'sekolah',
        'nomor_bidang',
    )

    inlines = (
        LegalitasTanahInline,
    )


    @admin.display(
        description='Legalitas'
    )
    def tampilkan_jumlah_legalitas(
        self,
        obj
    ):

        jumlah = (
            obj.legalitas.count()
        )

        if jumlah == 0:

            return 'Belum Ada'

        return (
            f'{jumlah} Dokumen'
        )


# =========================================================
# LEGALITAS TANAH
# =========================================================

@admin.register(LegalitasTanah)
class LegalitasTanahAdmin(
    admin.ModelAdmin
):

    list_display = (
        'tampilkan_sekolah',
        'tampilkan_bidang',
        'jenis_dokumen',
        'nomor_dokumen',
        'tanggal_dokumen',
        'atas_nama',
        'tampilkan_jumlah_lampiran',
    )

    list_filter = (
        'jenis_dokumen',
        'bidang_tanah__status_kepemilikan',
        'bidang_tanah__sekolah__kecamatan',
    )

    search_fields = (
        'bidang_tanah__sekolah__nama',
        'bidang_tanah__sekolah__npsn',
        'nomor_dokumen',
        'atas_nama',
        'nama_dokumen',
    )

    autocomplete_fields = (
        'bidang_tanah',
    )

    readonly_fields = (
        'dibuat_pada',
        'diperbarui_pada',
    )

    inlines = (
        DokumenTanahInline,
    )


    @admin.display(
        description='Sekolah'
    )
    def tampilkan_sekolah(
        self,
        obj
    ):

        return (
            obj.bidang_tanah.sekolah
        )


    @admin.display(
        description='Bidang'
    )
    def tampilkan_bidang(
        self,
        obj
    ):

        return (
            f'Bidang '
            f'{obj.bidang_tanah.nomor_bidang}'
        )


    @admin.display(
        description='Lampiran'
    )
    def tampilkan_jumlah_lampiran(
        self,
        obj
    ):

        jumlah = (
            obj.lampiran.count()
        )

        if jumlah == 0:

            return 'Belum Ada'

        return (
            f'{jumlah} File'
        )


@admin.register(DataRombel)
class DataRombelAdmin(
    admin.ModelAdmin
):

    list_display = (
        'sekolah',
        'nama_kelas',
        'jumlah_rombel',
        'jumlah_siswa',
        'kapasitas_ideal',
        'tampilkan_kekurangan',
        'tampilkan_status'
    )

    list_filter = (
        'sekolah__kategori',
        'sekolah__kecamatan'
    )

    search_fields = (
        'sekolah__nama',
        'sekolah__npsn',
        'nama_kelas'
    )

    autocomplete_fields = (
        'sekolah',
    )

    @admin.display(
        description='Kekurangan Kapasitas'
    )
    def tampilkan_kekurangan(
        self,
        obj
    ):

        return obj.kekurangan_kapasitas

    @admin.display(
        description='Status',
        boolean=True
    )
    def tampilkan_status(
        self,
        obj
    ):

        return not obj.melebihi_kapasitas