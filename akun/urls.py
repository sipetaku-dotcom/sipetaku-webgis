from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profil-sekolah/', views.profil_sekolah, name='profil_sekolah'),
    path('data-guru/', views.data_guru, name='data_guru'),
    path('tambah-guru/', views.tambah_guru, name='tambah_guru'),
    path('data-murid/', views.data_murid, name='data_murid'),
    path('tambah-murid/', views.tambah_murid, name='tambah_murid'),
    path('data-aset/', views.data_aset, name='data_aset'),
    path('tambah-aset/', views.tambah_aset, name='tambah_aset'),
    path('edit-guru/<int:id>/', views.edit_guru, name='edit_guru'),
    path('hapus-guru/<int:id>/', views.hapus_guru, name='hapus_guru'),
    path('edit-murid/<int:id>/', views.edit_murid, name='edit_murid'),
    path('hapus-murid/<int:id>/', views.hapus_murid, name='hapus_murid'),
    path('edit-aset/<int:id>/', views.edit_aset, name='edit_aset'),
    path('hapus-aset/<int:id>/', views.hapus_aset, name='hapus_aset'),
    path('data-prestasi/', views.data_prestasi, name='data_prestasi'),
    path('tambah-prestasi/', views.tambah_prestasi, name='tambah_prestasi'),
    path('edit-prestasi/<int:id>/', views.edit_prestasi, name='edit_prestasi'),
    path('hapus-prestasi/<int:id>/', views.hapus_prestasi, name='hapus_prestasi'),
    
]