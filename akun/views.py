from django.shortcuts import render, redirect
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


def ambil_profil_user(request):

    if not request.user.is_authenticated:
        return None

    try:
        return request.user.profil
    except:
        return None


def user_admin_kabupaten(request):
    return request.user.is_authenticated and request.user.is_superuser


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

    return render(request, 'akun/login.html')


def logout_view(request):

    logout(request)

    return redirect('/login/')


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