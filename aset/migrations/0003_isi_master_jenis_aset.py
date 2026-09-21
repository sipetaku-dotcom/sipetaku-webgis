from django.db import migrations


MASTER_ASET = [

    # Bangunan dan ruangan
    (
        'perumahan-dinas-guru',
        'Perumahan Dinas Guru',
        'BANGUNAN',
        'unit',
        False
    ),
    (
        'ruang-kepala-sekolah',
        'Ruang Kepala Sekolah',
        'BANGUNAN',
        'ruang',
        True
    ),
    (
        'ruang-guru',
        'Ruang Guru',
        'BANGUNAN',
        'ruang',
        True
    ),
    (
        'ruang-kelas',
        'Ruang Kelas',
        'BANGUNAN',
        'ruang',
        True
    ),
    (
        'ruang-uks',
        'Ruang UKS',
        'BANGUNAN',
        'ruang',
        True
    ),
    (
        'ruang-perpustakaan',
        'Ruang Perpustakaan',
        'BANGUNAN',
        'ruang',
        True
    ),
    (
        'ruang-tu',
        'Ruang Tata Usaha',
        'BANGUNAN',
        'ruang',
        False
    ),
    (
        'laboratorium-komputer',
        'Laboratorium Komputer',
        'BANGUNAN',
        'ruang',
        False
    ),
    (
        'laboratorium-ipas',
        'Laboratorium IPAS',
        'BANGUNAN',
        'ruang',
        False
    ),
    (
        'aula',
        'Aula',
        'BANGUNAN',
        'ruang',
        False
    ),
    (
        'ruang-media',
        'Ruang Media',
        'BANGUNAN',
        'ruang',
        False
    ),
    (
        'tempat-ibadah',
        'Tempat Ibadah/Musala',
        'BANGUNAN',
        'ruang',
        False
    ),
    (
        'ruang-bk',
        'Ruang Bimbingan Konseling (BK)',
        'BANGUNAN',
        'ruang',
        False
    ),
    (
        'ruang-osis',
        'Ruang OSIS',
        'BANGUNAN',
        'ruang',
        False
    ),
    (
        'ruang-pjok',
        'Ruang PJOK',
        'BANGUNAN',
        'ruang',
        False
    ),
    (
        'ruang-seni',
        'Ruang Seni',
        'BANGUNAN',
        'ruang',
        False
    ),
    (
        'gudang',
        'Gudang',
        'BANGUNAN',
        'ruang',
        False
    ),
    (
        'kantin',
        'Kantin',
        'BANGUNAN',
        'unit',
        False
    ),

    # Sanitasi dan lingkungan
    (
        'wastafel',
        'Wastafel',
        'SANITASI',
        'unit',
        True
    ),
    (
        'toilet',
        'Toilet/WC',
        'SANITASI',
        'unit',
        True
    ),
    (
        'lapangan',
        'Lapangan',
        'SANITASI',
        'unit',
        False
    ),
    (
        'tempat-parkir',
        'Tempat Parkir',
        'SANITASI',
        'area',
        False
    ),
    (
        'area-hijau',
        'Area Hijau',
        'SANITASI',
        'area',
        False
    ),
    (
        'pagar',
        'Pagar',
        'SANITASI',
        'meter',
        True
    ),

    # Barang dan perlengkapan
    (
        'meja-guru',
        'Meja Guru',
        'PERLENGKAPAN',
        'unit',
        True
    ),
    (
        'kursi-guru',
        'Kursi Guru',
        'PERLENGKAPAN',
        'unit',
        True
    ),
    (
        'meja-murid',
        'Meja Murid',
        'PERLENGKAPAN',
        'unit',
        True
    ),
    (
        'kursi-murid',
        'Kursi Murid',
        'PERLENGKAPAN',
        'unit',
        True
    ),
    (
        'lemari',
        'Lemari',
        'PERLENGKAPAN',
        'unit',
        False
    ),
    (
        'sofa',
        'Sofa',
        'PERLENGKAPAN',
        'unit',
        False
    ),
    (
        'loker',
        'Loker',
        'PERLENGKAPAN',
        'unit',
        False
    ),
    (
        'papan-tulis',
        'Papan Tulis',
        'PERLENGKAPAN',
        'unit',
        True
    ),
    (
        'papan-statistik',
        'Papan Statistik Sekolah',
        'PERLENGKAPAN',
        'unit',
        False
    ),
    (
        'kipas-angin',
        'Kipas Angin',
        'PERLENGKAPAN',
        'unit',
        False
    ),
    (
        'ac',
        'AC',
        'PERLENGKAPAN',
        'unit',
        False
    ),
    (
        'televisi',
        'Televisi',
        'PERLENGKAPAN',
        'unit',
        False
    ),
    (
        'komputer',
        'Komputer',
        'PERLENGKAPAN',
        'unit',
        True
    ),
    (
        'lampu',
        'Lampu',
        'PERLENGKAPAN',
        'unit',
        True
    ),
    (
        'buku-kelas',
        'Buku di Kelas',
        'PERLENGKAPAN',
        'eksemplar',
        True
    ),
    (
        'matras',
        'Matras',
        'PERLENGKAPAN',
        'unit',
        False
    ),
]


def isi_master_aset(apps, schema_editor):

    JenisAset = apps.get_model(
        'aset',
        'JenisAset'
    )

    urutan_per_kategori = {}

    for (
        kode,
        nama,
        kategori,
        satuan,
        aset_kritis
    ) in MASTER_ASET:

        urutan_per_kategori[kategori] = (
            urutan_per_kategori.get(
                kategori,
                0
            )
            + 1
        )

        JenisAset.objects.update_or_create(
            kode=kode,
            defaults={
                'nama': nama,
                'kategori': kategori,
                'satuan': satuan,
                'aset_kritis': aset_kritis,
                'urutan': (
                    urutan_per_kategori[
                        kategori
                    ]
                ),
                'aktif': True,
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        (
            'aset',
            '0002_jenisaset_asetsekolah_'
            'datatanahsekolah_datarombel_'
            'and_more'
        ),
    ]

    operations = [
        migrations.RunPython(
            isi_master_aset,
            migrations.RunPython.noop
        ),
    ]