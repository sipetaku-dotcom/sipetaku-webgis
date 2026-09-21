from django.core.exceptions import ValidationError
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

    nama = models.CharField(
        max_length=255
    )

    kategori = models.CharField(
        max_length=100
    )

    jumlah = models.IntegerField(
        default=0
    )

    kondisi = models.CharField(
        max_length=30,
        choices=KONDISI
    )

    keterangan = models.TextField(
        blank=True,
        null=True
    )

    foto = models.ImageField(
        upload_to='aset/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nama


class JenisAset(models.Model):

    KATEGORI = (
        ('BANGUNAN', 'Bangunan dan Ruangan'),
        ('SANITASI', 'Sanitasi dan Lingkungan'),
        ('PERLENGKAPAN', 'Barang dan Perlengkapan'),
    )

    kode = models.SlugField(
        max_length=100,
        unique=True
    )

    nama = models.CharField(
        max_length=150,
        unique=True
    )

    kategori = models.CharField(
        max_length=30,
        choices=KATEGORI
    )

    satuan = models.CharField(
        max_length=30,
        default='unit'
    )

    aset_kritis = models.BooleanField(
        default=False,
        help_text=(
            'Aset yang sangat memengaruhi '
            'prioritas bantuan sekolah.'
        )
    )

    urutan = models.PositiveSmallIntegerField(
        default=0
    )

    aktif = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = (
            'kategori',
            'urutan',
            'nama'
        )

        verbose_name = 'jenis aset'
        verbose_name_plural = 'master jenis aset'

    def __str__(self):
        return self.nama


class AsetSekolah(models.Model):

    KETERSEDIAAN = (
        ('ADA', 'Ada'),
        ('TIDAK_ADA', 'Tidak Ada'),
    )

    sekolah = models.ForeignKey(
        Sekolah,
        on_delete=models.CASCADE,
        related_name='inventaris_aset'
    )

    jenis_aset = models.ForeignKey(
        JenisAset,
        on_delete=models.PROTECT,
        related_name='data_sekolah'
    )

    ketersediaan = models.CharField(
        max_length=15,
        choices=KETERSEDIAAN,
        default='TIDAK_ADA'
    )

    jumlah_baik = models.PositiveIntegerField(
        default=0
    )

    jumlah_rusak_ringan = models.PositiveIntegerField(
        default=0
    )

    jumlah_rusak_berat = models.PositiveIntegerField(
        default=0
    )

    keterangan = models.TextField(
        blank=True
    )

    sudah_diisi = models.BooleanField(
        default=False,
        verbose_name='Sudah Diisi'
    )

    diperbarui_pada = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = (
            'jenis_aset__kategori',
            'jenis_aset__urutan'
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    'sekolah',
                    'jenis_aset'
                ),
                name='unik_aset_per_sekolah'
            ),

            models.CheckConstraint(
                condition=(
                    models.Q(
                        ketersediaan='TIDAK_ADA',
                        jumlah_baik=0,
                        jumlah_rusak_ringan=0,
                        jumlah_rusak_berat=0
                    )
                    |
                    (
                        models.Q(
                            ketersediaan='ADA'
                        )
                        &
                        (
                            models.Q(
                                jumlah_baik__gt=0
                            )
                            |
                            models.Q(
                                jumlah_rusak_ringan__gt=0
                            )
                            |
                            models.Q(
                                jumlah_rusak_berat__gt=0
                            )
                        )
                    )
                ),
                name='ketersediaan_sesuai_jumlah_aset'
            ),
        ]

        verbose_name = 'aset sekolah'
        verbose_name_plural = 'aset sekolah'

    @property
    def jumlah_total(self):

        return (
            self.jumlah_baik
            + self.jumlah_rusak_ringan
            + self.jumlah_rusak_berat
        )

    def clean(self):

        super().clean()

        if (
            self.ketersediaan == 'TIDAK_ADA'
            and self.jumlah_total > 0
        ):

            raise ValidationError(
                'Jumlah kondisi harus 0 apabila '
                'aset dipilih Tidak Ada.'
            )

        if (
            self.ketersediaan == 'ADA'
            and self.jumlah_total == 0
        ):

            raise ValidationError(
                'Isi sedikitnya satu jumlah kondisi '
                'apabila aset dipilih Ada.'
            )

    def __str__(self):

        return (
            f'{self.sekolah} - '
            f'{self.jenis_aset}'
        )
    

def lokasi_foto_aset(instance, filename):

    sekolah_id = (
        instance.aset_sekolah.sekolah_id
    )

    kode_aset = (
        instance.aset_sekolah.jenis_aset.kode
    )

    return (
        f'aset/{sekolah_id}/'
        f'{kode_aset}/{filename}'
    )


class FotoAset(models.Model):

    aset_sekolah = models.ForeignKey(
        AsetSekolah,
        on_delete=models.CASCADE,
        related_name='foto_dokumentasi'
    )

    foto = models.ImageField(
        upload_to=lokasi_foto_aset
    )

    urutan = models.PositiveSmallIntegerField(
        default=1
    )

    keterangan = models.CharField(
        max_length=255,
        blank=True
    )

    diunggah_pada = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = (
            'urutan',
            'id'
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    'aset_sekolah',
                    'urutan'
                ),
                name='unik_urutan_foto_aset'
            ),

            models.CheckConstraint(
                condition=models.Q(
                    urutan__gte=1,
                    urutan__lte=3
                ),
                name='urutan_foto_aset_1_sampai_3'
            ),
        ]

        verbose_name = 'foto aset'
        verbose_name_plural = 'foto aset'

    def clean(self):

        super().clean()

        if (
            self.aset_sekolah_id
            and
            self.aset_sekolah.ketersediaan
            == 'TIDAK_ADA'
        ):

            raise ValidationError(
                'Aset yang dipilih Tidak Ada '
                'tidak dapat memiliki foto.'
            )

        jumlah_foto = (
            FotoAset.objects
            .filter(
                aset_sekolah_id=(
                    self.aset_sekolah_id
                )
            )
            .exclude(pk=self.pk)
            .count()
        )

        if jumlah_foto >= 3:

            raise ValidationError(
                'Maksimal 3 foto untuk '
                'setiap aset.'
            )

    def __str__(self):

        return (
            f'Foto {self.urutan} - '
            f'{self.aset_sekolah}'
        )
    


class DataRombel(models.Model):

    TINGKAT_KELAS = (
        (1, 'Kelas 1'),
        (2, 'Kelas 2'),
        (3, 'Kelas 3'),
        (4, 'Kelas 4'),
        (5, 'Kelas 5'),
        (6, 'Kelas 6'),
        (7, 'Kelas 7'),
        (8, 'Kelas 8'),
        (9, 'Kelas 9'),
    )

    sekolah = models.ForeignKey(
        Sekolah,
        on_delete=models.CASCADE,
        related_name='data_rombel'
    )

    tahun_ajaran = models.ForeignKey(
        'murid.TahunAjaran',
        on_delete=models.PROTECT,
        related_name='data_rombel'
    )

    nama_kelas = models.CharField(
        max_length=50
    )

    tingkat = models.PositiveSmallIntegerField(
        choices=TINGKAT_KELAS,
        blank=True,
        null=True,
        verbose_name='Tingkat Kelas'
    )

    jumlah_rombel = models.PositiveSmallIntegerField(
        default=1
    )

    jumlah_siswa = models.PositiveIntegerField(
        default=0
    )

    kapasitas_ideal = models.PositiveIntegerField(
        default=0
    )

    keterangan = models.TextField(
        blank=True
    )

    class Meta:

        ordering = (
            'nama_kelas',
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    'sekolah',
                    'nama_kelas',
                    'tahun_ajaran'
                ),
                name=(
                    'unik_nama_kelas_'
                    'per_sekolah_tahun'
                )
            ),
        ]

        verbose_name = (
            'data rombongan belajar'
        )

        verbose_name_plural = (
            'data rombongan belajar'
        )

    @property
    def kapasitas_total(self):

        return (
            self.jumlah_rombel
            * self.kapasitas_ideal
        )


    @property
    def jumlah_siswa_aktif(self):

        return (
            self.riwayat_murid
            .filter(
                status_akhir='AKTIF'
            )
            .count()
        )


    @property
    def kekurangan_kapasitas(self):

        if (
            self.kapasitas_total > 0
            and
            self.jumlah_siswa_aktif
            > self.kapasitas_total
        ):

            return (
                self.jumlah_siswa_aktif
                - self.kapasitas_total
            )

        return 0


    @property
    def melebihi_kapasitas(self):

        return (
            self.kekurangan_kapasitas > 0
        )

    def clean(self):

        super().clean()

        if self.jumlah_rombel < 1:

            raise ValidationError({
                'jumlah_rombel': (
                    'Jumlah rombel minimal 1.'
                )
            })

    def __str__(self):

        if self.tahun_ajaran:

            return (
                f'{self.sekolah} - '
                f'{self.nama_kelas} - '
                f'{self.tahun_ajaran.nama}'
            )

        return (
            f'{self.sekolah} - '
            f'{self.nama_kelas}'
        )



# =========================================================
# BIDANG TANAH SEKOLAH
# =========================================================

class BidangTanahSekolah(models.Model):

    STATUS_KEPEMILIKAN = (
        (
            'PEMDA',
            'Milik Pemerintah Daerah'
        ),
        (
            'PEMERINTAH_PUSAT',
            'Milik Pemerintah Pusat'
        ),
        (
            'YAYASAN',
            'Milik Yayasan'
        ),
        (
            'HIBAH_PEMDA',
            'Hibah kepada Pemerintah Daerah'
        ),
        (
            'HIBAH_SEKOLAH',
            'Hibah kepada Sekolah'
        ),
        (
            'PINJAM_PAKAI',
            'Pinjam Pakai'
        ),
        (
            'SEWA',
            'Sewa'
        ),
        (
            'PENGUASAAN',
            'Penguasaan'
        ),
        (
            'LAINNYA',
            'Lainnya'
        ),
    )


    sekolah = models.ForeignKey(
        Sekolah,
        on_delete=models.CASCADE,
        related_name='bidang_tanah'
    )


    nomor_bidang = models.PositiveIntegerField(
        verbose_name='Nomor Bidang'
    )


    luas_bidang_m2 = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name='Luas Bidang (m²)'
    )


    status_kepemilikan = models.CharField(
        max_length=30,
        choices=STATUS_KEPEMILIKAN,
        verbose_name='Status Kepemilikan'
    )


    keterangan = models.TextField(
        blank=True
    )


    dibuat_pada = models.DateTimeField(
        auto_now_add=True
    )


    diperbarui_pada = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        ordering = [
            'nomor_bidang'
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    'sekolah',
                    'nomor_bidang'
                ],
                name='unik_nomor_bidang_per_sekolah'
            )

        ]

        verbose_name = (
            'bidang tanah sekolah'
        )

        verbose_name_plural = (
            'bidang tanah sekolah'
        )


    def clean(self):

        super().clean()

        if (
            self.luas_bidang_m2 is not None
            and
            self.luas_bidang_m2 <= 0
        ):

            raise ValidationError({
                'luas_bidang_m2':
                    'Luas bidang harus lebih dari 0.'
            })


    def __str__(self):

        return (
            f'Bidang {self.nomor_bidang} '
            f'- {self.sekolah.nama}'
        )



# =========================================================
# LEGALITAS TANAH
# =========================================================

class LegalitasTanah(models.Model):

    JENIS_DOKUMEN = (
        (
            'SERTIFIKAT',
            'Sertifikat Tanah'
        ),
        (
            'SPPT',
            'Surat Pernyataan Penguasaan Tanah'
        ),
        (
            'HIBAH',
            'Surat Hibah'
        ),
        (
            'AKTA_HIBAH',
            'Akta Hibah'
        ),
        (
            'BAST',
            'Berita Acara Serah Terima'
        ),
        (
            'PINJAM_PAKAI',
            'Perjanjian Pinjam Pakai'
        ),
        (
            'SEWA',
            'Perjanjian Sewa'
        ),
        (
            'SKT',
            'Surat Keterangan Tanah'
        ),
        (
            'LAINNYA',
            'Dokumen Lainnya'
        ),
    )


    bidang_tanah = models.ForeignKey(
        BidangTanahSekolah,
        on_delete=models.CASCADE,
        related_name='legalitas'
    )


    jenis_dokumen = models.CharField(
        max_length=30,
        choices=JENIS_DOKUMEN
    )


    nama_dokumen = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Nama Dokumen'
    )


    nomor_dokumen = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Nomor Dokumen'
    )


    tanggal_dokumen = models.DateField(
        blank=True,
        null=True,
        verbose_name='Tanggal Dokumen'
    )


    atas_nama = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Atas Nama'
    )


    keterangan = models.TextField(
        blank=True
    )


    dibuat_pada = models.DateTimeField(
        auto_now_add=True
    )


    diperbarui_pada = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        ordering = [
            '-tanggal_dokumen',
            '-id'
        ]

        verbose_name = (
            'legalitas tanah'
        )

        verbose_name_plural = (
            'legalitas tanah'
        )


    def __str__(self):

        if self.nomor_dokumen:

            return (
                f'{self.get_jenis_dokumen_display()} '
                f'- {self.nomor_dokumen}'
            )

        return (
            self.get_jenis_dokumen_display()
        )


# =========================================================
# LAMPIRAN LEGALITAS TANAH
# =========================================================

def lokasi_dokumen_tanah(
    instance,
    filename
):

    sekolah_id = (
        instance.legalitas
        .bidang_tanah
        .sekolah_id
    )

    bidang_id = (
        instance.legalitas
        .bidang_tanah_id
    )

    legalitas_id = (
        instance.legalitas_id
    )

    return (
        f'legalitas_tanah/'
        f'{sekolah_id}/'
        f'bidang_{bidang_id}/'
        f'legalitas_{legalitas_id}/'
        f'{filename}'
    )


class DokumenTanah(models.Model):

    legalitas = models.ForeignKey(
        LegalitasTanah,
        on_delete=models.CASCADE,
        related_name='lampiran'
    )


    file = models.FileField(
        upload_to=lokasi_dokumen_tanah
    )


    nama_file = models.CharField(
        max_length=150,
        blank=True
    )


    keterangan = models.CharField(
        max_length=255,
        blank=True
    )


    diunggah_pada = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        ordering = [
            'id'
        ]

        verbose_name = (
            'dokumen tanah'
        )

        verbose_name_plural = (
            'dokumen tanah'
        )


    def __str__(self):

        if self.nama_file:

            return self.nama_file

        return (
            f'Dokumen {self.legalitas}'
        )