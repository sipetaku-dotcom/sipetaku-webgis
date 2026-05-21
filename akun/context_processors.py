def info_operator(request):

    data = {
        'sekolah_login': None,
        'sidebar_total_guru': 0,
        'sidebar_total_murid': 0,
        'sidebar_total_prestasi': 0,
        'sidebar_total_aset': 0,
    }

    if request.user.is_authenticated and not request.user.is_superuser:

        try:
            sekolah = request.user.sekolah_operator

            data['sekolah_login'] = sekolah
            data['sidebar_total_guru'] = sekolah.guru.count()
            data['sidebar_total_murid'] = sekolah.murid.count()
            data['sidebar_total_prestasi'] = sekolah.prestasi.count()
            data['sidebar_total_aset'] = sekolah.aset.count()

        except:
            pass

    return data