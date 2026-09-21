from murid.models import TahunAjaran
from .models import (
    AsetSekolah,
    DataRombel,
    BidangTanahSekolah,
    JenisAset,
)


NILAI_KONDISI = {
    'BAIK': 100,
    'RUSAK_RINGAN': 60,
    'RUSAK_BERAT': 20,
}


def nilai_satu_aset(
    data_aset
):

    if (
        data_aset.ketersediaan
        == 'TIDAK_ADA'
    ):

        return 0

    jumlah_total = (
        data_aset.jumlah_total
    )

    if jumlah_total <= 0:
        return 0

    nilai_baik = (
        data_aset.jumlah_baik
        * NILAI_KONDISI['BAIK']
    )

    nilai_rusak_ringan = (
        data_aset.jumlah_rusak_ringan
        * NILAI_KONDISI[
            'RUSAK_RINGAN'
        ]
    )

    nilai_rusak_berat = (
        data_aset.jumlah_rusak_berat
        * NILAI_KONDISI[
            'RUSAK_BERAT'
        ]
    )

    nilai = (
        nilai_baik
        + nilai_rusak_ringan
        + nilai_rusak_berat
    ) / jumlah_total

    return round(
        nilai,
        2
    )


def status_prioritas(
    skor_prioritas
):

    if skor_prioritas >= 80:

        return {
            'nama': 'Sangat Mendesak',
            'warna': 'danger',
            'ikon': (
                'bi-exclamation-octagon'
            ),
        }

    if skor_prioritas >= 60:

        return {
            'nama': 'Mendesak',
            'warna': 'warning',
            'ikon': (
                'bi-exclamation-triangle'
            ),
        }

    if skor_prioritas >= 40:

        return {
            'nama': 'Perlu Perhatian',
            'warna': 'info',
            'ikon': 'bi-info-circle',
        }

    if skor_prioritas >= 20:

        return {
            'nama': 'Cukup',
            'warna': 'primary',
            'ikon': 'bi-tools',
        }

    return {
        'nama': 'Baik',
        'warna': 'success',
        'ikon': 'bi-check-circle',
    }


def hitung_penilaian_sekolah(
    sekolah
):

    master_aset = list(
        JenisAset.objects
        .filter(aktif=True)
        .order_by(
            'kategori',
            'urutan'
        )
    )

    daftar_aset = list(
        AsetSekolah.objects
        .filter(
            sekolah=sekolah,
            jenis_aset__aktif=True,
            sudah_diisi=True
        )
        .select_related(
            'jenis_aset'
        )
    )

    aset_per_jenis = {
        data.jenis_aset_id: data
        for data in daftar_aset
    }

    jumlah_master = len(
        master_aset
    )

    jumlah_terisi = len(
        aset_per_jenis
    )

    if jumlah_master > 0:

        progres = round(
            (
                jumlah_terisi
                / jumlah_master
            )
            * 100
        )

    else:

        progres = 0

    total_nilai_tertimbang = 0
    total_bobot = 0

    aset_tidak_ada = []
    aset_rusak_berat = []
    aset_rusak_ringan = []

    for jenis in master_aset:

        data = aset_per_jenis.get(
            jenis.id
        )

        # Belum diisi tidak dianggap
        # sebagai aset tidak tersedia.
        if data is None:
            continue

        if jenis.aset_kritis:
            bobot = 3
        else:
            bobot = 1

        nilai = nilai_satu_aset(
            data
        )

        total_nilai_tertimbang += (
            nilai * bobot
        )

        total_bobot += bobot

        if (
            data.ketersediaan
            == 'TIDAK_ADA'
        ):

            aset_tidak_ada.append(
                jenis.nama
            )

        if (
            data.jumlah_rusak_berat
            > 0
        ):

            aset_rusak_berat.append({
                'nama': jenis.nama,
                'jumlah': (
                    data.jumlah_rusak_berat
                ),
                'kritis': (
                    jenis.aset_kritis
                ),
            })

        if (
            data.jumlah_rusak_ringan
            > 0
        ):

            aset_rusak_ringan.append({
                'nama': jenis.nama,
                'jumlah': (
                    data.jumlah_rusak_ringan
                ),
                'kritis': (
                    jenis.aset_kritis
                ),
            })

    if total_bobot > 0:

        skor_aset = round(
            total_nilai_tertimbang
            / total_bobot,
            2
        )

    else:

        skor_aset = None

    tahun_ajaran = (
        TahunAjaran.objects
        .filter(aktif=True)
        .first()
    )

    if tahun_ajaran:

        daftar_rombel = list(
            DataRombel.objects
            .filter(
                sekolah=sekolah,
                tahun_ajaran=tahun_ajaran
            )
        )

    else:

        daftar_rombel = []

    total_siswa = sum(
        data.jumlah_siswa_aktif
        for data in daftar_rombel
    )

    total_kapasitas = sum(
        data.kapasitas_total
        for data in daftar_rombel
    )

    total_kelebihan_siswa = sum(
        data.kekurangan_kapasitas
        for data in daftar_rombel
    )

    if total_siswa > 0:

        skor_kapasitas = min(
            100,
            round(
                (
                    total_kapasitas
                    / total_siswa
                )
                * 100,
                2
            )
        )

    else:

        skor_kapasitas = None

    komponen_nilai = []
    komponen_bobot = []

    if skor_aset is not None:

        komponen_nilai.append(
            skor_aset * 80
        )

        komponen_bobot.append(
            80
        )

    if skor_kapasitas is not None:

        komponen_nilai.append(
            skor_kapasitas * 20
        )

        komponen_bobot.append(
            20
        )

    if komponen_bobot:

        skor_kelayakan = round(
            sum(komponen_nilai)
            / sum(komponen_bobot),
            2
        )

        skor_prioritas = round(
            100 - skor_kelayakan,
            2
        )

    else:

        skor_kelayakan = None
        skor_prioritas = None

    # =====================================================
    # LEGALITAS TANAH
    # =====================================================

    daftar_bidang_tanah = list(
        BidangTanahSekolah.objects
        .filter(
            sekolah=sekolah
        )
        .prefetch_related(
            'legalitas'
        )
        .order_by(
            'nomor_bidang'
        )
    )


    jumlah_bidang_tanah = (
        len(
            daftar_bidang_tanah
        )
    )


    jumlah_bidang_berlegalitas = sum(
        1
        for bidang in daftar_bidang_tanah
        if bidang.legalitas.all()
    )


    jumlah_bidang_belum_berlegalitas = (
        jumlah_bidang_tanah
        - jumlah_bidang_berlegalitas
    )


    # =====================================================
    # STATUS LEGALITAS
    # =====================================================

    if jumlah_bidang_tanah == 0:

        status_legalitas = (
            'Data tanah belum diisi'
        )

        legalitas_aman = False


    elif jumlah_bidang_berlegalitas == 0:

        status_legalitas = (
            'Legalitas tanah belum tersedia'
        )

        legalitas_aman = False


    elif (
        jumlah_bidang_berlegalitas
        < jumlah_bidang_tanah
    ):

        status_legalitas = (
            'Legalitas tanah belum lengkap'
        )

        legalitas_aman = False


    else:

        status_legalitas = (
            'Legalitas tanah lengkap'
        )

        legalitas_aman = True

    alasan = []

    aset_kritis_tidak_ada = [
        jenis.nama
        for jenis in master_aset
        if (
            jenis.aset_kritis
            and jenis.id
            in aset_per_jenis
            and
            aset_per_jenis[
                jenis.id
            ].ketersediaan
            == 'TIDAK_ADA'
        )
    ]

    if aset_kritis_tidak_ada:

        alasan.append(
            'Aset penting belum tersedia: '
            + ', '.join(
                aset_kritis_tidak_ada[:5]
            )
        )

    rusak_berat_kritis = [
        data
        for data in aset_rusak_berat
        if data['kritis']
    ]

    if rusak_berat_kritis:

        rincian = [
            (
                f"{data['nama']} "
                f"({data['jumlah']} unit)"
            )
            for data
            in rusak_berat_kritis[:5]
        ]

        alasan.append(
            'Aset penting rusak berat: '
            + ', '.join(rincian)
        )

    if total_kelebihan_siswa > 0:

        alasan.append(
            (
                'Kapasitas kelas kurang untuk '
                f'{total_kelebihan_siswa} siswa'
            )
        )

    if not legalitas_aman:

        alasan.append(
            status_legalitas
        )

    if progres < 100:

        alasan.append(
            (
                'Pendataan aset baru '
                f'{progres}%'
            )
        )

    if not alasan:

        alasan.append(
            'Sarana dan kapasitas sekolah '
            'dalam kondisi baik.'
        )

    if skor_prioritas is not None:

        status = status_prioritas(
            skor_prioritas
        )

    else:

        status = {
            'nama': 'Belum Dinilai',
            'warna': 'secondary',
            'ikon': 'bi-hourglass',
        }

    penilaian_final = (
        progres == 100
        and skor_aset is not None
        and skor_kapasitas is not None
    )

    if not penilaian_final:

        status = {
            'nama': 'Data Belum Lengkap',
            'warna': 'secondary',
            'ikon': 'bi-hourglass-split',
        }

    return {
        'skor_aset':
            skor_aset,

        'skor_kapasitas':
            skor_kapasitas,

        'skor_kelayakan':
            skor_kelayakan,

        'skor_prioritas':
            skor_prioritas,

        'status':
            status,

        'progres':
            progres,

        'jumlah_master':
            jumlah_master,

        'jumlah_terisi':
            jumlah_terisi,

        'aset_tidak_ada':
            aset_tidak_ada,

        'aset_rusak_ringan':
            aset_rusak_ringan,

        'aset_rusak_berat':
            aset_rusak_berat,

        'total_siswa':
            total_siswa,

        'total_kapasitas':
            total_kapasitas,

        'total_kelebihan_siswa':
            total_kelebihan_siswa,

        'status_legalitas':
            status_legalitas,

        'legalitas_aman':
            legalitas_aman,

        'alasan':
            alasan,

        'penilaian_final':
            penilaian_final,
    }