# -*- coding: utf-8 -*-
{
    'name': 'PT PAL Employee Management',
    'summary': 'Manajemen Data Karyawan PT PAL Indonesia (Persero)',
    'description': """
        Modul Manajemen Karyawan untuk PT PAL Indonesia (Persero)
        ==========================================================
        Modul ini digunakan oleh Divisi Human Capital untuk mengelola
        data karyawan secara aman dan efisien.

        Fitur:
        - CRUD data karyawan lengkap
        - Nomor Induk Karyawan (NIK Perusahaan)
        - NIK KTP
        - Departemen sesuai struktur organisasi PT PAL
        - Data BPJS Kesehatan & Ketenagakerjaan
        - Status Karyawan (Tetap, Kontrak, Magang)
        - Hak akses berbasis peran (User & Manager)
    """,
    'author': 'PT PAL Indonesia (Persero) - Human Capital Division',
    'website': 'https://www.integratedpal.com',
    'category': 'Human Resources',
    'version': '14.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/employee_management_views.xml',
        'views/employee_management_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
