from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sekolah.forms import SekolahForm
from guru.models import Guru
from guru.forms import GuruForm
from murid.models import Murid
from murid.forms import MuridForm
from aset.models import Aset
from aset.forms import AsetForm
from prestasi.models import Prestasi
from prestasi.forms import PrestasiForm
from django.contrib import messages
from .models import ProfilUser
import json
from sekolah.models import Sekolah
from sekolah.wilayah import DATA_WILAYAH
from django.contrib.auth.models import User


def ambil_profil_user(request):

    if not request.user.is_authenticated:
        return None

    try:
        return request.user.profil
    except:
        return None


def user_admin_kabupaten(request):

    profil = ambil_profil_user(request)

    if request.user.is_superuser:
        return True

    if profil and profil.role == 'admin_kabupaten':
        return True

    return False


def user_admin_kecamatan(request):
    profil = ambil_profil_user(request)

    if profil and profil.role == 'admin_kecamatan':
        return True

    return False


def user_operator_sekolah(request):
    profil = ambil_profil_user(request)

    if profil and profil.role == 'operator_sekolah':
        return True

    return False


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

        else:

            messages.error(
                request,
                'Username atau password anda salah'
            )

    return render(
        request,
        'akun/login.html'
    )


def logout_view(request):

    logout(request)

    return redirect('/login/')


@login_required
def tambah_sekolah(request):

    if not user_admin_kabupaten(request):
        return redirect('/')

    if request.method == 'POST':
        form = SekolahForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Data sekolah berhasil ditambahkan')
            return redirect('/tambah-sekolah/')

    else:
        form = SekolahForm()

    context = {
        'form': form,
        'data_wilayah': json.dumps(DATA_WILAYAH),
    }

    return render(request, 'akun/tambah_sekolah.html', context)


@login_required
def data_sekolah(request):

    if not user_admin_kabupaten(request):
        return redirect('/')

    sekolah = Sekolah.objects.all().order_by('nama')

    context = {
        'sekolah': sekolah,
    }

    return render(request, 'akun/data_sekolah.html', context)


@login_required
def edit_sekolah(request, id):

    if not user_admin_kabupaten(request):
        return redirect('/')

    sekolah = get_object_or_404(
        Sekolah,
        id=id
    )

    if request.method == 'POST':

        form = SekolahForm(
            request.POST,
            request.FILES,
            instance=sekolah
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Data sekolah berhasil diubah'
            )

            return redirect('/data-sekolah/')

    else:

        form = SekolahForm(instance=sekolah)

    context = {
        'form': form,
        'sekolah': sekolah,
        'data_wilayah': json.dumps(DATA_WILAYAH),
    }

    return render(
        request,
        'akun/edit_sekolah.html',
        context
    )


@login_required
def hapus_sekolah(request, id):

    if not user_admin_kabupaten(request):
        return redirect('/')

    sekolah = get_object_or_404(
        Sekolah,
        id=id
    )

    sekolah.delete()

    messages.success(
        request,
        'Data sekolah berhasil dihapus'
    )

    return redirect('/data-sekolah/')


@login_required
def tambah_user_operator(request):

    if not user_admin_kabupaten(request):
        return redirect('/')

    sekolah_list = Sekolah.objects.filter(
        user__isnull=True
    ).order_by('kecamatan', 'desa', 'nama')

    data_sekolah = []

    for sekolah in sekolah_list:
        data_sekolah.append({
            'id': sekolah.id,
            'nama': sekolah.nama,
            'npsn': sekolah.npsn,
            'kecamatan': sekolah.kecamatan,
            'desa': sekolah.desa,
        })

    if request.method == 'POST':

        nama_lengkap = request.POST.get('nama_lengkap')
        username = request.POST.get('username')
        password = request.POST.get('password')
        sekolah_id = request.POST.get('sekolah')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan')
            return redirect('/tambah-user-operator/')

        sekolah = Sekolah.objects.get(id=sekolah_id)

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=nama_lengkap
        )

        ProfilUser.objects.create(
            user=user,
            role='operator_sekolah',
            kecamatan=sekolah.kecamatan,
            sekolah=sekolah
        )

        sekolah.user = user
        sekolah.save()

        messages.success(request, 'User operator sekolah berhasil dibuat')
        return redirect('/tambah-user-operator/')

    context = {
        'data_wilayah': json.dumps(DATA_WILAYAH),
        'data_sekolah': json.dumps(data_sekolah),
    }

    return render(request, 'akun/tambah_user_operator.html', context)


@login_required
def data_operator(request):

    if not user_admin_kabupaten(request):
        return redirect('/')

    operator = ProfilUser.objects.filter(
        role='operator_sekolah'
    ).select_related('user', 'sekolah').order_by('sekolah__nama')

    context = {
        'operator': operator,
    }

    return render(request, 'akun/data_operator.html', context)


@login_required
def tambah_user_admin_kecamatan(request):

    if not user_admin_kabupaten(request):
        return redirect('/')

    if request.method == 'POST':

        nama_lengkap = request.POST.get('nama_lengkap')
        username = request.POST.get('username')
        password = request.POST.get('password')
        kecamatan = request.POST.get('kecamatan')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan')
            return redirect('/tambah-user-admin-kecamatan/')

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=nama_lengkap
        )

        ProfilUser.objects.create(
            user=user,
            role='admin_kecamatan',
            kecamatan=kecamatan
        )

        messages.success(request, 'User admin kecamatan berhasil dibuat')
        return redirect('/tambah-user-admin-kecamatan/')

    context = {
        'data_wilayah': DATA_WILAYAH,
    }

    return render(request, 'akun/tambah_user_admin_kecamatan.html', context)


@login_required
def data_admin_kecamatan(request):

    if not user_admin_kabupaten(request):
        return redirect('/')

    admin_kecamatan = ProfilUser.objects.filter(
        role='admin_kecamatan'
    ).select_related('user').order_by('kecamatan')

    context = {
        'admin_kecamatan': admin_kecamatan,
    }

    return render(request, 'akun/data_admin_kecamatan.html', context)


@login_required
def tambah_user_admin_kabupaten(request):

    if not request.user.is_superuser:
        return redirect('/')

    if request.method == 'POST':

        nama_lengkap = request.POST.get('nama_lengkap')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan')
            return redirect('/tambah-user-admin-kabupaten/')

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=nama_lengkap
        )

        ProfilUser.objects.create(
            user=user,
            role='admin_kabupaten'
        )

        messages.success(request, 'User admin kabupaten berhasil dibuat')
        return redirect('/tambah-user-admin-kabupaten/')

    return render(request, 'akun/tambah_user_admin_kabupaten.html')


@login_required
def edit_operator(request, id):

    if not user_admin_kabupaten(request):
        return redirect('/')

    profil_operator = ProfilUser.objects.get(
        id=id,
        role='operator_sekolah'
    )

    if request.method == 'POST':

        nama_lengkap = request.POST.get('nama_lengkap')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = profil_operator.user

        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, 'Username sudah digunakan')
            return redirect(f'/edit-operator/{id}/')

        user.first_name = nama_lengkap
        user.username = username

        if password:
            user.set_password(password)

        user.save()

        messages.success(request, 'Data operator berhasil diubah')
        return redirect('/data-operator/')

    context = {
        'operator': profil_operator,
    }

    return render(request, 'akun/edit_operator.html', context)


@login_required
def hapus_operator(request, id):

    if not user_admin_kabupaten(request):
        return redirect('/')

    profil_operator = ProfilUser.objects.get(
        id=id,
        role='operator_sekolah'
    )

    sekolah = profil_operator.sekolah
    user = profil_operator.user

    if sekolah:
        sekolah.user = None
        sekolah.save()

    user.delete()

    messages.success(request, 'User operator berhasil dihapus')
    return redirect('/data-operator/')


@login_required
def edit_admin_kecamatan(request, id):

    if not user_admin_kabupaten(request):
        return redirect('/')

    profil_admin = ProfilUser.objects.get(
        id=id,
        role='admin_kecamatan'
    )

    if request.method == 'POST':

        nama_lengkap = request.POST.get('nama_lengkap')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = profil_admin.user

        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, 'Username sudah digunakan')
            return redirect(f'/edit-admin-kecamatan/{id}/')

        user.first_name = nama_lengkap
        user.username = username

        if password:
            user.set_password(password)

        user.save()

        messages.success(request, 'Data admin kecamatan berhasil diubah')
        return redirect('/data-admin-kecamatan/')

    context = {
        'admin_kecamatan': profil_admin,
    }

    return render(request, 'akun/edit_admin_kecamatan.html', context)


@login_required
def hapus_admin_kecamatan(request, id):

    if not user_admin_kabupaten(request):
        return redirect('/')

    profil_admin = ProfilUser.objects.get(
        id=id,
        role='admin_kecamatan'
    )

    user = profil_admin.user
    user.delete()

    messages.success(request, 'User admin kecamatan berhasil dihapus')
    return redirect('/data-admin-kecamatan/')


@login_required
def data_admin_kabupaten(request):

    if not request.user.is_superuser:
        return redirect('/')

    admin_kabupaten = ProfilUser.objects.filter(
        role='admin_kabupaten',
        user__is_superuser=False
    ).select_related('user').order_by('user__first_name')

    context = {
        'admin_kabupaten': admin_kabupaten,
    }

    return render(request, 'akun/data_admin_kabupaten.html', context)


@login_required
def edit_admin_kabupaten(request, id):

    if not request.user.is_superuser:
        return redirect('/')

    profil_admin = ProfilUser.objects.get(
        id=id,
        role='admin_kabupaten'
    )

    if request.method == 'POST':

        nama_lengkap = request.POST.get('nama_lengkap')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = profil_admin.user

        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, 'Username sudah digunakan')
            return redirect(f'/edit-admin-kabupaten/{id}/')

        user.first_name = nama_lengkap
        user.username = username

        if password:
            user.set_password(password)

        user.save()

        messages.success(request, 'Data admin kabupaten berhasil diubah')
        return redirect('/data-admin-kabupaten/')

    context = {
        'admin_kabupaten': profil_admin,
    }

    return render(request, 'akun/edit_admin_kabupaten.html', context)


@login_required
def hapus_admin_kabupaten(request, id):

    if not request.user.is_superuser:
        return redirect('/')

    profil_admin = ProfilUser.objects.get(
        id=id,
        role='admin_kabupaten'
    )

    user = profil_admin.user
    user.delete()

    messages.success(request, 'User admin kabupaten berhasil dihapus')
    return redirect('/data-admin-kabupaten/')


@login_required
def profil_sekolah(request):

    try:

        sekolah = ambil_sekolah_operator(request)

        if sekolah is None:
            return redirect('/')

    except:
        return render(request, 'akun/belum_terhubung.html')

    if request.method == 'POST':
        form = SekolahForm(
            request.POST,
            request.FILES,
            instance=sekolah
        )

        if form.is_valid():
            form.save()
            return redirect('/profil-sekolah/')

    else:
        form = SekolahForm(instance=sekolah)

    context = {
        'form': form,
        'sekolah': sekolah,
        'data_wilayah': json.dumps(DATA_WILAYAH),
    }

    return render(request, 'akun/profil_sekolah.html', context)


@login_required
def data_guru(request):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')
    
    guru = Guru.objects.filter(sekolah=sekolah)

    context = {
        'guru': guru,
        'sekolah': sekolah,
    }

    return render(request, 'akun/data_guru.html', context)


@login_required
def tambah_guru(request):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    if request.method == 'POST':
        form = GuruForm(request.POST)

        if form.is_valid():
            guru = form.save(commit=False)
            guru.sekolah = sekolah
            guru.save()

            messages.success(
                request,
                'Data guru berhasil ditambahkan'
            )

            return redirect('/data-guru/')

    else:
        form = GuruForm()

    context = {
        'form': form,
    }

    return render(request, 'akun/tambah_guru.html', context)


@login_required
def data_murid(request):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    murid = Murid.objects.filter(sekolah=sekolah)

    context = {
        'murid': murid,
        'sekolah': sekolah,
    }

    return render(request, 'akun/data_murid.html', context)


@login_required
def tambah_murid(request):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    if request.method == 'POST':
        form = MuridForm(request.POST)

        if form.is_valid():
            murid = form.save(commit=False)
            murid.sekolah = sekolah
            murid.save()
            messages.success(request, 'Data murid berhasil ditambahkan')

            return redirect('/data-murid/')

    else:
        form = MuridForm()

    context = {
        'form': form,
    }

    return render(request, 'akun/tambah_murid.html', context)


@login_required
def data_aset(request):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    aset = Aset.objects.filter(sekolah=sekolah)

    context = {
        'aset': aset,
        'sekolah': sekolah,
    }

    return render(request, 'akun/data_aset.html', context)


@login_required
def tambah_aset(request):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    if request.method == 'POST':

        form = AsetForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            aset = form.save(commit=False)
            aset.sekolah = sekolah
            aset.save()
            messages.success(request, 'Data aset berhasil ditambahkan')

            return redirect('/data-aset/')

    else:
        form = AsetForm()

    context = {
        'form': form,
    }

    return render(request, 'akun/tambah_aset.html', context)


@login_required
def edit_guru(request, id):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    guru = Guru.objects.get(
        id=id,
        sekolah=sekolah
    )

    if request.method == 'POST':
        form = GuruForm(request.POST, instance=guru)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Data guru berhasil diubah'
            )

            return redirect('/data-guru/')

    else:
        form = GuruForm(instance=guru)

    context = {
        'form': form,
        'guru': guru,
    }

    return render(request, 'akun/edit_guru.html', context)


@login_required
def hapus_guru(request, id):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    guru = Guru.objects.get(
        id=id,
        sekolah=sekolah
    )

    messages.success(
        request,
        'Data guru berhasil dihapus'
    )

    guru.delete()

    return redirect('/data-guru/')


@login_required
def edit_murid(request, id):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    murid = Murid.objects.get(
        id=id,
        sekolah=sekolah
    )

    if request.method == 'POST':

        form = MuridForm(
            request.POST,
            instance=murid
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Data murid berhasil diubah')

            return redirect('/data-murid/')

    else:
        form = MuridForm(instance=murid)

    context = {
        'form': form,
        'murid': murid,
    }

    return render(
        request,
        'akun/edit_murid.html',
        context
    )


@login_required
def hapus_murid(request, id):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    murid = Murid.objects.get(
        id=id,
        sekolah=sekolah
    )

    messages.success(request, 'Data murid berhasil dihapus')
    murid.delete()

    return redirect('/data-murid/')


@login_required
def edit_aset(request, id):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    aset = Aset.objects.get(
        id=id,
        sekolah=sekolah
    )

    if request.method == 'POST':

        form = AsetForm(
            request.POST,
            request.FILES,
            instance=aset
        )

        if form.is_valid():

            form.save()
            messages.success(request, 'Data aset berhasil diubah')

            return redirect('/data-aset/')

    else:
        form = AsetForm(instance=aset)

    context = {
        'form': form,
        'aset': aset,
    }

    return render(
        request,
        'akun/edit_aset.html',
        context
    )


@login_required
def hapus_aset(request, id):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    aset = Aset.objects.get(
        id=id,
        sekolah=sekolah
    )

    messages.success(request, 'Data aset berhasil dihapus')
    aset.delete()

    return redirect('/data-aset/')


@login_required
def data_prestasi(request):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    prestasi = Prestasi.objects.filter(sekolah=sekolah)

    context = {
        'prestasi': prestasi,
        'sekolah': sekolah,
    }

    return render(request, 'akun/data_prestasi.html', context)


@login_required
def tambah_prestasi(request):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    if request.method == 'POST':
        form = PrestasiForm(request.POST, request.FILES)

        form.fields['murid'].queryset = Murid.objects.filter(sekolah=sekolah)

        if form.is_valid():
            prestasi = form.save(commit=False)
            prestasi.sekolah = sekolah
            prestasi.save()
            messages.success(request, 'Data prestasi berhasil ditambahkan')

            return redirect('/data-prestasi/')

    else:
        form = PrestasiForm()
        form.fields['murid'].queryset = Murid.objects.filter(sekolah=sekolah)

    context = {
        'form': form,
    }

    return render(request, 'akun/tambah_prestasi.html', context)


@login_required
def edit_prestasi(request, id):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    prestasi = Prestasi.objects.get(
        id=id,
        sekolah=sekolah
    )

    if request.method == 'POST':
        form = PrestasiForm(
            request.POST,
            request.FILES,
            instance=prestasi
        )

        form.fields['murid'].queryset = Murid.objects.filter(sekolah=sekolah)

        if form.is_valid():
            form.save()
            messages.success(request, 'Data prestasi berhasil diubah')
            return redirect('/data-prestasi/')

    else:
        form = PrestasiForm(instance=prestasi)
        form.fields['murid'].queryset = Murid.objects.filter(sekolah=sekolah)

    context = {
        'form': form,
        'prestasi': prestasi,
    }

    return render(request, 'akun/edit_prestasi.html', context)


@login_required
def hapus_prestasi(request, id):

    sekolah = ambil_sekolah_operator(request)

    if sekolah is None:
        return redirect('/')

    prestasi = Prestasi.objects.get(
        id=id,
        sekolah=sekolah
    )

    messages.success(request, 'Data prestasi berhasil dihapus')
    prestasi.delete()

    return redirect('/data-prestasi/')


def ambil_sekolah_operator(request):
    if not request.user.is_authenticated:
        return None

    if request.user.is_superuser:
        return None

    try:
        return request.user.sekolah_operator
    except:
        return None