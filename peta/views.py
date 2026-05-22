from django.shortcuts import render
from sekolah.models import Sekolah, KategoriSekolah
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Count
from guru.models import Guru
from murid.models import Murid
from prestasi.models import Prestasi
from aset.models import Aset
from datetime import date, timedelta
from django.http import HttpResponse
from openpyxl import Workbook
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from akun.views import (ambil_profil_user, user_admin_kabupaten)
from django.template.loader import render_to_string
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


def user_admin_kabupaten(request):

    profil = ambil_profil_user(request)

    if request.user.is_superuser:
        return True

    if profil and profil.role == 'admin_kabupaten':
        return True

    return False


def index(request):

    profil = ambil_profil_user(request)

    if request.user.is_authenticated:

        if user_admin_kabupaten(request):
            sekolah = Sekolah.objects.annotate(
                total_prestasi=Count('prestasi', distinct=True),
                total_guru=Count('guru', distinct=True),
                total_murid=Count('murid', distinct=True)
            )

        elif profil and profil.role == 'admin_kecamatan':
            sekolah = Sekolah.objects.filter(
                kecamatan=profil.kecamatan
            ).annotate(
                total_prestasi=Count('prestasi', distinct=True),
                total_guru=Count('guru', distinct=True),
                total_murid=Count('murid', distinct=True)
            )

        else:
            sekolah = Sekolah.objects.filter(
                user=request.user
            ).annotate(
                total_prestasi=Count('prestasi', distinct=True),
                total_guru=Count('guru', distinct=True),
                total_murid=Count('murid', distinct=True)
            )

    else:
        sekolah = Sekolah.objects.annotate(
            total_prestasi=Count('prestasi', distinct=True),
            total_guru=Count('guru', distinct=True),
            total_murid=Count('murid', distinct=True)
        )

    kecamatan = request.GET.get('kecamatan')
    kategori = request.GET.get('kategori')
    status_prestasi = request.GET.get('status_prestasi')

    if kecamatan:
        sekolah = sekolah.filter(kecamatan=kecamatan)

    if kategori:
        sekolah = sekolah.filter(kategori_id=kategori)

    if status_prestasi == 'punya':
        sekolah = sekolah.filter(
            total_prestasi__gt=0
        )

    if status_prestasi == 'tidak':
        sekolah = sekolah.filter(
            total_prestasi=0
        )

    if user_admin_kabupaten(request):

        daftar_kecamatan = Sekolah.objects.values_list(
            'kecamatan',
            flat=True
        ).distinct().order_by('kecamatan')

    elif profil and profil.role == 'admin_kecamatan':

        daftar_kecamatan = Sekolah.objects.filter(
            kecamatan=profil.kecamatan
        ).values_list(
            'kecamatan',
            flat=True
        ).distinct().order_by('kecamatan')

    else:

        daftar_kecamatan = []

    daftar_kategori = KategoriSekolah.objects.all().order_by('nama')

    total_sekolah_tampil = sekolah.count()

    total_guru = sekolah.aggregate(
        total=Sum('total_guru')
    )['total'] or 0

    total_murid = sekolah.aggregate(
        total=Sum('total_murid')
    )['total'] or 0

    total_prestasi = sekolah.aggregate(
        total=Sum('total_prestasi')
    )['total'] or 0

    context = {
        'sekolah': sekolah,
        'daftar_kecamatan': daftar_kecamatan,
        'daftar_kategori': daftar_kategori,
        'status_prestasi': status_prestasi,
        'total_sekolah_tampil': total_sekolah_tampil,
        'total_guru': total_guru,
        'total_murid': total_murid,
        'total_prestasi': total_prestasi,
    }

    return render(request, 'peta/index.html', context)


def detail_sekolah(request, id):

    sekolah = get_object_or_404(
        Sekolah,
        id=id
    )

    profil = ambil_profil_user(request)

    if request.user.is_authenticated:

        if user_admin_kabupaten(request):
            pass

        elif profil and profil.role == 'admin_kecamatan':

            if sekolah.kecamatan != profil.kecamatan:
                return redirect('/')

        else:

            if sekolah.user != request.user:
                return redirect('/')

    daftar_guru = sekolah.guru.all()
    daftar_murid = sekolah.murid.all()
    daftar_aset = sekolah.aset.all()
    daftar_prestasi = sekolah.prestasi.all()

    total_guru = daftar_guru.count()
    total_murid = daftar_murid.count()
    total_aset = daftar_aset.count()
    total_prestasi = daftar_prestasi.count()

    prestasi_per_tahun = daftar_prestasi.values(
        'tahun'
    ).annotate(
        jumlah=Count('id')
    ).order_by('tahun')

    label_tahun_prestasi = []
    data_tahun_prestasi = []

    for p in prestasi_per_tahun:
        label_tahun_prestasi.append(p['tahun'])
        data_tahun_prestasi.append(p['jumlah'])

    aset_per_kondisi = daftar_aset.values(
        'kondisi'
    ).annotate(
        jumlah=Count('id')
    ).order_by('kondisi')

    label_kondisi_aset = []
    data_kondisi_aset = []

    for a in aset_per_kondisi:
        label_kondisi_aset.append(a['kondisi'])
        data_kondisi_aset.append(a['jumlah'])

    jumlah_laki = daftar_murid.filter(
        jenis_kelamin='L'
    ).count()

    jumlah_perempuan = daftar_murid.filter(
        jenis_kelamin='P'
    ).count()

    context = {
        'sekolah': sekolah,
        'daftar_guru': daftar_guru,
        'daftar_murid': daftar_murid,
        'daftar_aset': daftar_aset,
        'daftar_prestasi': daftar_prestasi,
        'total_guru': total_guru,
        'total_murid': total_murid,
        'total_aset': total_aset,
        'total_prestasi': total_prestasi,
        'jumlah_laki': jumlah_laki,
        'jumlah_perempuan': jumlah_perempuan,
        'label_tahun_prestasi': json.dumps(label_tahun_prestasi),
        'data_tahun_prestasi': json.dumps(data_tahun_prestasi),
        'label_kondisi_aset': json.dumps(label_kondisi_aset),
        'data_kondisi_aset': json.dumps(data_kondisi_aset),
    }

    return render(
        request,
        'peta/detail_sekolah.html',
        context
    )


@login_required
def dashboard(request):
    profil = ambil_profil_user(request)

    if user_admin_kabupaten(request):

        sekolah_qs = Sekolah.objects.all()

    elif profil and profil.role == 'admin_kecamatan':

        sekolah_qs = Sekolah.objects.filter(
            kecamatan=profil.kecamatan
        )

    else:

        return redirect('/')

    total_sekolah = sekolah_qs.count()

    total_guru = Guru.objects.filter(
        sekolah__in=sekolah_qs
    ).count()

    total_murid = Murid.objects.filter(
        sekolah__in=sekolah_qs
    ).count()

    total_aset = Aset.objects.filter(
        sekolah__in=sekolah_qs
    ).count()

    total_prestasi = Prestasi.objects.filter(
        sekolah__in=sekolah_qs
    ).count()

    total_kategori = KategoriSekolah.objects.count()

    sekolah_per_kategori = KategoriSekolah.objects.annotate(
        jumlah=Count('sekolah')
    )

    hari_ini = date.today()
    batas_pensiun = hari_ini + timedelta(days=365)

    guru_akan_pensiun = Guru.objects.filter(
        sekolah__in=sekolah_qs,
        tanggal_pensiun__isnull=False,
        tanggal_pensiun__gte=hari_ini,
        tanggal_pensiun__lte=batas_pensiun
    )

    total_guru_akan_pensiun = guru_akan_pensiun.count()

    guru_pensiun_per_kecamatan = guru_akan_pensiun.values(
        'sekolah__kecamatan'
    ).annotate(
        jumlah=Count('id')
    ).order_by('sekolah__kecamatan')

    prestasi_per_tingkat = Prestasi.objects.values(
        'tingkat'
    ).annotate(
        jumlah=Count('id')
    ).order_by('tingkat')

    label_prestasi = []
    data_prestasi = []

    for p in prestasi_per_tingkat:
        label_prestasi.append(p['tingkat'])
        data_prestasi.append(p['jumlah'])

    label_kategori = []
    data_kategori = []

    for k in sekolah_per_kategori:
        label_kategori.append(k.nama)
        data_kategori.append(k.jumlah)

    label_pensiun = []
    data_pensiun = []

    for g in guru_pensiun_per_kecamatan:
        label_pensiun.append(g['sekolah__kecamatan'])
        data_pensiun.append(g['jumlah'])

    tingkat = request.GET.get('tingkat')
    tahun = request.GET.get('tahun')

    kecamatan = request.GET.get('kecamatan')
    kategori = request.GET.get('kategori')

    daftar_prestasi = Prestasi.objects.filter(
        sekolah__in=sekolah_qs
    )

    if tingkat:
        daftar_prestasi = daftar_prestasi.filter(
            tingkat=tingkat
        )

    if tahun:
        daftar_prestasi = daftar_prestasi.filter(
            tahun=tahun
        )

    if kecamatan:
        daftar_prestasi = daftar_prestasi.filter(
            sekolah__kecamatan=kecamatan
        )

    if kategori:
        daftar_prestasi = daftar_prestasi.filter(
            sekolah__kategori_id=kategori
        )

    daftar_tahun = Prestasi.objects.values_list(
        'tahun',
        flat=True
    ).distinct().order_by('-tahun')

    if user_admin_kabupaten(request):

        daftar_kecamatan = Sekolah.objects.values_list(
            'kecamatan',
            flat=True
        ).distinct().order_by('kecamatan')

    elif profil and profil.role == 'admin_kecamatan':

        daftar_kecamatan = Sekolah.objects.filter(
            kecamatan=profil.kecamatan
        ).values_list(
            'kecamatan',
            flat=True
        ).distinct().order_by('kecamatan')

    else:

        daftar_kecamatan = []

    daftar_kategori = KategoriSekolah.objects.all().order_by('nama')

    sekolah_per_kecamatan = []

    daftar_kecamatan_dashboard = sekolah_qs.values_list(
        'kecamatan',
        flat=True
    ).distinct().order_by('kecamatan')

    for kec in daftar_kecamatan_dashboard:

        daftar_sekolah = sekolah_qs.filter(
            kecamatan=kec
        ).order_by('nama')

        jumlah_per_kategori = daftar_sekolah.values(
            'kategori__nama'
        ).annotate(
            jumlah=Count('id')
        ).order_by('kategori__nama')

        sekolah_per_kecamatan.append({
            'nama_kecamatan': kec,
            'jumlah_sekolah': daftar_sekolah.count(),
            'jumlah_per_kategori': jumlah_per_kategori,
        })

    ranking_sekolah = sekolah_qs.annotate(
        jumlah_prestasi=Count('prestasi')
    ).order_by('-jumlah_prestasi')[:10]

    context = {
        'total_sekolah': total_sekolah,
        'total_guru': total_guru,
        'total_murid': total_murid,
        'total_aset': total_aset,
        'total_kategori': total_kategori,
        'total_prestasi': total_prestasi,

        'sekolah_per_kategori': sekolah_per_kategori,
        'sekolah_per_kecamatan': sekolah_per_kecamatan,

        'guru_akan_pensiun': guru_akan_pensiun,
        'total_guru_akan_pensiun': total_guru_akan_pensiun,

        'prestasi_per_tingkat': prestasi_per_tingkat,
        'daftar_prestasi': daftar_prestasi,
        'daftar_tahun': daftar_tahun,

        'tingkat_terpilih': tingkat,
        'tahun_terpilih': tahun,

        'daftar_kecamatan': daftar_kecamatan,
        'daftar_kategori': daftar_kategori,
        'kecamatan_terpilih': kecamatan,
        'kategori_terpilih': kategori,

        'ranking_sekolah': ranking_sekolah,

        'label_prestasi': json.dumps(label_prestasi),
        'data_prestasi': json.dumps(data_prestasi),

        'label_kategori': json.dumps(label_kategori),
        'data_kategori': json.dumps(data_kategori),

        'label_pensiun': json.dumps(label_pensiun),
        'data_pensiun': json.dumps(data_pensiun),
    }

    return render(request, 'peta/dashboard.html', context)


@login_required
def export_sekolah_excel(request):

    wb = Workbook()
    ws = wb.active
    ws.title = "Data Sekolah"

    ws.append([
        'No',
        'Nama Sekolah',
        'NPSN',
        'Kategori',
        'Status',
        'Kecamatan',
        'Desa',
        'Alamat',
        'Latitude',
        'Longitude',
    ])

    profil = ambil_profil_user(request)

    if user_admin_kabupaten(request):
        sekolah = Sekolah.objects.all()

    elif profil and profil.role == 'admin_kecamatan':
        sekolah = Sekolah.objects.filter(
            kecamatan=profil.kecamatan
        )

    else:
        return redirect('/')

    for no, s in enumerate(sekolah, start=1):
        ws.append([
            no,
            s.nama,
            s.npsn,
            s.kategori.nama,
            s.status,
            s.kecamatan,
            s.desa,
            s.alamat,
            s.latitude,
            s.longitude,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=data_sekolah.xlsx'

    wb.save(response)

    return response


@login_required
def export_guru_excel(request):

    wb = Workbook()
    ws = wb.active
    ws.title = "Data Guru"

    ws.append([
        'No',
        'Nama Guru',
        'NIP',
        'NIK',
        'Jenis Kelamin',
        'Sekolah',
        'Kecamatan',
        'Jabatan',
        'Status Pegawai',
        'Mata Pelajaran',
        'Tanggal Lahir',
        'Tanggal Pensiun',
        'No HP',
    ])

    profil = ambil_profil_user(request)

    if user_admin_kabupaten(request):

        guru = Guru.objects.select_related(
            'sekolah'
        ).all()

    elif profil and profil.role == 'admin_kecamatan':

        guru = Guru.objects.select_related(
            'sekolah'
        ).filter(
            sekolah__kecamatan=profil.kecamatan
        )

    else:

        return redirect('/')

    for no, g in enumerate(guru, start=1):
        ws.append([
            no,
            g.nama,
            g.nip,
            g.nik,
            g.jenis_kelamin,
            g.sekolah.nama,
            g.sekolah.kecamatan,
            g.jabatan,
            g.status_pegawai,
            g.mata_pelajaran,
            g.tanggal_lahir,
            g.tanggal_pensiun,
            g.no_hp,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=data_guru.xlsx'

    wb.save(response)

    return response


@login_required
def export_murid_excel(request):

    wb = Workbook()
    ws = wb.active
    ws.title = "Data Murid"

    ws.append([
        'No',
        'Nama Murid',
        'NISN',
        'NIK',
        'Jenis Kelamin',
        'Sekolah',
        'Kecamatan',
        'Kelas',
        'Tanggal Lahir',
        'Alamat',
        'Prestasi',
    ])

    profil = ambil_profil_user(request)

    if user_admin_kabupaten(request):

        murid = Murid.objects.select_related(
            'sekolah'
        ).all()

    elif profil and profil.role == 'admin_kecamatan':

        murid = Murid.objects.select_related(
            'sekolah'
        ).filter(
            sekolah__kecamatan=profil.kecamatan
        )

    else:

        return redirect('/')

    for no, m in enumerate(murid, start=1):
        ws.append([
            no,
            m.nama,
            m.nisn,
            m.nik,
            m.jenis_kelamin,
            m.sekolah.nama,
            m.sekolah.kecamatan,
            m.kelas,
            m.tanggal_lahir,
            m.alamat,
            m.prestasi,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=data_murid.xlsx'

    wb.save(response)

    return response


@login_required
def export_prestasi_excel(request):

    tingkat = request.GET.get('tingkat')
    tahun = request.GET.get('tahun')
    kecamatan = request.GET.get('kecamatan')
    kategori = request.GET.get('kategori')

    profil = ambil_profil_user(request)

    if user_admin_kabupaten(request):

        prestasi = Prestasi.objects.select_related(
            'sekolah',
            'murid'
        ).all()

    elif profil and profil.role == 'admin_kecamatan':

        prestasi = Prestasi.objects.select_related(
            'sekolah',
            'murid'
        ).filter(
            sekolah__kecamatan=profil.kecamatan
        )

    else:

        return redirect('/')

    if tingkat:
        prestasi = prestasi.filter(tingkat=tingkat)

    if tahun:
        prestasi = prestasi.filter(tahun=tahun)

    if kecamatan:
        prestasi = prestasi.filter(sekolah__kecamatan=kecamatan)

    if kategori:
        prestasi = prestasi.filter(sekolah__kategori_id=kategori)

    wb = Workbook()
    ws = wb.active
    ws.title = "Data Prestasi"

    ws.append([
        'No',
        'Nama Murid',
        'Sekolah',
        'Kategori Sekolah',
        'Kecamatan',
        'Nama Lomba',
        'Bidang Lomba',
        'Tingkat',
        'Juara',
        'Tahun',
        'Keterangan',
    ])

    for no, p in enumerate(prestasi, start=1):
        ws.append([
            no,
            p.murid.nama,
            p.sekolah.nama,
            p.sekolah.kategori.nama,
            p.sekolah.kecamatan,
            p.nama_lomba,
            p.bidang_lomba,
            p.tingkat,
            p.juara,
            p.tahun,
            p.keterangan,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=data_prestasi_filter.xlsx'

    wb.save(response)

    return response


@login_required
def export_aset_excel(request):

    wb = Workbook()
    ws = wb.active
    ws.title = "Data Aset"

    ws.append([
        'No',
        'Nama Aset',
        'Kategori',
        'Jumlah',
        'Kondisi',
        'Sekolah',
        'Kecamatan',
        'Keterangan',
    ])

    profil = ambil_profil_user(request)

    if user_admin_kabupaten(request):

        aset = Aset.objects.select_related(
            'sekolah'
        ).all()

    elif profil and profil.role == 'admin_kecamatan':

        aset = Aset.objects.select_related(
            'sekolah'
        ).filter(
            sekolah__kecamatan=profil.kecamatan
        )

    else:

        return redirect('/')

    for no, a in enumerate(aset, start=1):
        ws.append([
            no,
            a.nama,
            a.kategori,
            a.jumlah,
            a.kondisi,
            a.sekolah.nama,
            a.sekolah.kecamatan,
            a.keterangan,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=data_aset.xlsx'

    wb.save(response)

    return response


@login_required
def export_guru_pensiun_excel(request):

    hari_ini = date.today()
    batas_pensiun = hari_ini + timedelta(days=365)

    profil = ambil_profil_user(request)

    if user_admin_kabupaten(request):

        guru = Guru.objects.select_related('sekolah').filter(
            tanggal_pensiun__isnull=False,
            tanggal_pensiun__gte=hari_ini,
            tanggal_pensiun__lte=batas_pensiun
        )

    elif profil and profil.role == 'admin_kecamatan':

        guru = Guru.objects.select_related('sekolah').filter(
            sekolah__kecamatan=profil.kecamatan,
            tanggal_pensiun__isnull=False,
            tanggal_pensiun__gte=hari_ini,
            tanggal_pensiun__lte=batas_pensiun
        )

    else:

        return redirect('/')

    wb = Workbook()
    ws = wb.active
    ws.title = "Guru Akan Pensiun"

    ws.append([
        'No',
        'Nama Guru',
        'Sekolah',
        'Kecamatan',
        'Jabatan',
        'Status Pegawai',
        'Tanggal Pensiun',
        'No HP',
    ])

    for no, g in enumerate(guru, start=1):
        ws.append([
            no,
            g.nama,
            g.sekolah.nama,
            g.sekolah.kecamatan,
            g.jabatan,
            g.status_pegawai,
            g.tanggal_pensiun,
            g.no_hp,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=guru_akan_pensiun.xlsx'

    wb.save(response)

    return response


def export_detail_sekolah_pdf(request, id):

    sekolah = Sekolah.objects.get(id=id)

    daftar_guru = Guru.objects.filter(
        sekolah=sekolah
    )

    daftar_murid = Murid.objects.filter(
        sekolah=sekolah
    )

    daftar_prestasi = Prestasi.objects.filter(
        murid__sekolah=sekolah
    )

    daftar_aset = Aset.objects.filter(
        sekolah=sekolah
    )

    total_guru = daftar_guru.count()
    total_murid = daftar_murid.count()
    total_prestasi = daftar_prestasi.count()
    total_aset = daftar_aset.count()

    template = get_template(
        'peta/pdf_detail_sekolah.html'
    )

    html = template.render({
        'sekolah': sekolah,
        'total_guru': total_guru,
        'total_murid': total_murid,
        'total_prestasi': total_prestasi,
        'total_aset': total_aset,
        'daftar_prestasi': daftar_prestasi[:10],
    })

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'filename="profil-{sekolah.nama}.pdf"'

    pisa_status = pisa.CreatePDF(
        html,
        dest=response
    )

    if pisa_status.err:
        return HttpResponse(
            'Terjadi kesalahan saat membuat PDF'
        )

    return response