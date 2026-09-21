from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(
        'ubah-password/',
        views.ubah_password,
        name='ubah_password'
    ),
    path(
        'dashboard-sekolah/',
        views.dashboard_operator,
        name='dashboard_operator'
    ),
    path(
        'monitoring-kesiapan-tahun-ajaran/',
        views.monitoring_kesiapan_tahun_ajaran,
        name='monitoring_kesiapan_tahun_ajaran'
    ),
    path(
        'kelola-tahun-ajaran/',
        views.kelola_tahun_ajaran,
        name='kelola_tahun_ajaran'
    ),
    path('profil-sekolah/', views.profil_sekolah, name='profil_sekolah'),
    path(
        'data-pegawai/',
        views.data_pegawai,
        name='data_pegawai'
    ),
    path(
        'tambah-pegawai/',
        views.tambah_pegawai,
        name='tambah_pegawai'
    ),
    path(
        'edit-pegawai/<int:id>/',
        views.edit_pegawai,
        name='edit_pegawai'
    ),
    path(
        'riwayat-pegawai/<int:id>/',
        views.riwayat_pegawai,
        name='riwayat_pegawai'
    ),
    path(
        'mutasi-pegawai/<int:id>/',
        views.mutasi_pegawai,
        name='mutasi_pegawai'
    ),
    path(
        'akhiri-pegawai/<int:id>/',
        views.akhiri_pegawai,
        name='akhiri_pegawai'
    ),
    path(
        'download-template-pegawai/',
        views.download_template_pegawai,
        name='download_template_pegawai'
    ),
    path(
        'import-pegawai/',
        views.import_pegawai_excel,
        name='import_pegawai_excel'
    ),
    path(
        'arsip-pegawai/',
        views.arsip_pegawai,
        name='arsip_pegawai'
    ),
    path('data-murid/', views.data_murid, name='data_murid'),
    path('tambah-murid/', views.tambah_murid, name='tambah_murid'),
    path(
        'ubah-status-murid/<int:id>/',
        views.ubah_status_murid,
        name='ubah_status_murid'
    ),
    path(
        'pulihkan-status-murid/<int:id>/',
        views.pulihkan_status_murid,
        name='pulihkan_status_murid'
    ),
    path(
        'import-murid/',
        views.import_murid_excel,
        name='import_murid_excel'
    ),
    path(
        'download-template-murid/',
        views.download_template_murid,
        name='download_template_murid'
    ),
    path(
        'persiapan-tahun-ajaran/',
        views.persiapan_tahun_ajaran,
        name='persiapan_tahun_ajaran'
    ),
    path(
        'tambah-rombel-tahun-berikutnya/<int:tahun_id>/',
        views.tambah_rombel_tahun_berikutnya,
        name='tambah_rombel_tahun_berikutnya'
    ),
    path(
        'rombel-tahun-berikutnya/<int:id>/edit/',
        views.edit_rombel_tahun_berikutnya,
        name='edit_rombel_tahun_berikutnya'
    ),
    path(
        'rombel-tahun-berikutnya/<int:id>/hapus/',
        views.hapus_rombel_tahun_berikutnya,
        name='hapus_rombel_tahun_berikutnya'
    ),
    path(
        'proses-akhir-tahun/',
        views.proses_akhir_tahun,
        name='proses_akhir_tahun'
    ),
    path(
        'aktifkan-tahun-ajaran/<int:tahun_id>/',
        views.aktifkan_tahun_ajaran,
        name='aktifkan_tahun_ajaran'
    ),
    path(
        'riwayat-murid/<int:id>/',
        views.riwayat_murid,
        name='riwayat_murid'
    ),
    path(
        'arsip-lulusan/',
        views.arsip_lulusan,
        name='arsip_lulusan'
    ),
    path(
        'arsip-siswa-keluar/',
        views.arsip_siswa_keluar,
        name='arsip_siswa_keluar'
    ),
    path('data-aset/', views.data_aset, name='data_aset'),
    path(
        'tanah-legalitas/',
        views.tanah_legalitas_sekolah,
        name='tanah_legalitas_sekolah'
    ),

    path(
        'tanah-legalitas/bidang/tambah/',
        views.tambah_bidang_tanah,
        name='tambah_bidang_tanah'
    ),

    path(
        'tanah-legalitas/bidang/<int:id>/',
        views.detail_bidang_tanah,
        name='detail_bidang_tanah'
    ),

    path(
        'tanah-legalitas/bidang/<int:id>/edit/',
        views.edit_bidang_tanah,
        name='edit_bidang_tanah'
    ),

    path(
        'tanah-legalitas/bidang/<int:id>/hapus/',
        views.hapus_bidang_tanah,
        name='hapus_bidang_tanah'
    ),

    path(
        'tanah-legalitas/bidang/<int:bidang_id>/legalitas/tambah/',
        views.tambah_legalitas_tanah,
        name='tambah_legalitas_tanah'
    ),

    path(
        'tanah-legalitas/legalitas/<int:id>/edit/',
        views.edit_legalitas_tanah,
        name='edit_legalitas_tanah'
    ),

    path(
        'tanah-legalitas/legalitas/<int:id>/hapus/',
        views.hapus_legalitas_tanah,
        name='hapus_legalitas_tanah'
    ),

    path(
        'tanah-legalitas/legalitas/<int:legalitas_id>/lampiran/tambah/',
        views.tambah_lampiran_legalitas,
        name='tambah_lampiran_legalitas'
    ),

    path(
        'tanah-legalitas/lampiran/<int:id>/hapus/',
        views.hapus_lampiran_legalitas,
        name='hapus_lampiran_legalitas'
    ),
    path(
        'data-aset/isi/<int:jenis_id>/',
        views.isi_aset_sekolah,
        name='isi_aset_sekolah'
    ),
    path(
        'data-rombel/',
        views.data_rombel_sekolah,
        name='data_rombel_sekolah'
    ),

    path(
        'data-rombel/tambah/',
        views.tambah_rombel_sekolah,
        name='tambah_rombel_sekolah'
    ),

    path(
        'data-rombel/<int:id>/edit/',
        views.edit_rombel_sekolah,
        name='edit_rombel_sekolah'
    ),

    path(
        'data-rombel/<int:id>/hapus/',
        views.hapus_rombel_sekolah,
        name='hapus_rombel_sekolah'
    ),
    path(
        'prioritas-bantuan/',
        views.prioritas_bantuan_sekolah,
        name='prioritas_bantuan_sekolah'
    ),
    path(
        'prioritas-bantuan/<int:id>/',
        views.detail_prioritas_sekolah,
        name='detail_prioritas_sekolah'
    ),
    path('tambah-aset/', views.tambah_aset, name='tambah_aset'),
    path('edit-murid/<int:id>/', views.edit_murid, name='edit_murid'),
    path('hapus-murid/<int:id>/', views.hapus_murid, name='hapus_murid'),
    path('edit-aset/<int:id>/', views.edit_aset, name='edit_aset'),
    path('hapus-aset/<int:id>/', views.hapus_aset, name='hapus_aset'),
    path('data-prestasi/', views.data_prestasi, name='data_prestasi'),
    path('tambah-prestasi/', views.tambah_prestasi, name='tambah_prestasi'),
    path('edit-prestasi/<int:id>/', views.edit_prestasi, name='edit_prestasi'),
    path('hapus-prestasi/<int:id>/', views.hapus_prestasi, name='hapus_prestasi'),
    path('tambah-sekolah/', views.tambah_sekolah, name='tambah_sekolah'),
    path('edit-sekolah/<int:id>/', views.edit_sekolah, name='edit_sekolah'),
    path('hapus-sekolah/<int:id>/', views.hapus_sekolah, name='hapus_sekolah'),    
    path('data-sekolah/', views.data_sekolah, name='data_sekolah'),
    path('tambah-user-operator/', views.tambah_user_operator, name='tambah_user_operator'),
    path('data-operator/', views.data_operator, name='data_operator'),
    path('tambah-user-admin-kecamatan/', views.tambah_user_admin_kecamatan, name='tambah_user_admin_kecamatan'),
    path('data-admin-kecamatan/', views.data_admin_kecamatan, name='data_admin_kecamatan'),
    path('tambah-user-admin-kabupaten/', views.tambah_user_admin_kabupaten, name='tambah_user_admin_kabupaten'),
    path('edit-operator/<int:id>/', views.edit_operator, name='edit_operator'),
    path('hapus-operator/<int:id>/', views.hapus_operator, name='hapus_operator'),
    path('edit-admin-kecamatan/<int:id>/', views.edit_admin_kecamatan, name='edit_admin_kecamatan'),
    path('hapus-admin-kecamatan/<int:id>/', views.hapus_admin_kecamatan, name='hapus_admin_kecamatan'),
    path('data-admin-kabupaten/', views.data_admin_kabupaten, name='data_admin_kabupaten'),
    path('edit-admin-kabupaten/<int:id>/', views.edit_admin_kabupaten, name='edit_admin_kabupaten'),
    path('hapus-admin-kabupaten/<int:id>/', views.hapus_admin_kabupaten, name='hapus_admin_kabupaten'),
]