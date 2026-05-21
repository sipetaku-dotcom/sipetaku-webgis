from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sekolah/<int:id>/', views.detail_sekolah, name='detail_sekolah'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export/sekolah/', views.export_sekolah_excel, name='export_sekolah_excel'),
    path('export/guru/', views.export_guru_excel, name='export_guru_excel'),
    path('export/murid/', views.export_murid_excel, name='export_murid_excel'),
    path('export/prestasi/', views.export_prestasi_excel, name='export_prestasi_excel'),
    path('export/aset/', views.export_aset_excel, name='export_aset_excel'),
    path('export/guru-pensiun/', views.export_guru_pensiun_excel, name='export_guru_pensiun_excel'),
    path('sekolah/<int:id>/pdf/', views.export_detail_sekolah_pdf, name='export_detail_sekolah_pdf'),
]