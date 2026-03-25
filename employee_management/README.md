# PT PAL Employee Management - Odoo 14 Custom Module

## Deskripsi

Modul manajemen karyawan (Employee Management) untuk **PT PAL Indonesia (Persero)** — perusahaan manufaktur maritim terbesar di Indonesia yang bergerak di bidang pembangunan kapal perang, kapal niaga, general engineering, dan MRO.

Modul ini digunakan oleh **Divisi Human Capital** (Human Capital Services, Human Capital Development, dan Organization Development) untuk mengelola data karyawan secara aman dan efisien.

## Fitur

- **CRUD Lengkap** — Create, Read, Update, Delete data karyawan
- **Nomor Induk Karyawan** — Unik per karyawan dengan constraint SQL
- **NIK KTP** — Validasi 16 digit angka
- **Departemen** — Sesuai struktur organisasi PT PAL (Shipbuilding, Naval Architecture, MRO, dll.)
- **Status Karyawan** — Tetap, Kontrak, Magang
- **Data BPJS** — BPJS Kesehatan & Ketenagakerjaan
- **Hak Akses** — Dua level: Human Capital User & Human Capital Manager
- **Arsip** — Soft-delete dengan field Active
- **Pencarian & Filter** — Filter berdasarkan status, grup berdasarkan departemen

## Struktur Direktori

```
employee_management/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   └── employee_management.py
├── security/
│   ├── security.xml
│   └── ir.model.access.csv
├── static/
│   └── description/
│       └── icon.png
└── views/
    ├── employee_management_views.xml
    └── employee_management_menus.xml
```

## Persyaratan

- **Odoo 14 Community/Enterprise**
- **Python 3.6+**
- **PostgreSQL 10+**

## Instalasi

1. Salin folder `employee_management` ke direktori addons Odoo:
   ```bash
   cp -r employee_management /path/to/odoo/addons/
   ```

2. Restart service Odoo:
   ```bash
   sudo systemctl restart odoo
   ```

3. Aktifkan **Developer Mode** di Odoo:
   - Settings → Activate Developer Mode

4. Update daftar modul:
   - Apps → Update Apps List → Update

5. Cari dan install modul:
   - Apps → Cari "PT PAL Employee Management" → Install

## Pengujian CRUD (End-to-End)

### CREATE (Tambah Karyawan Baru)

1. Buka menu **PT PAL Employee Management → Human Capital → Data Karyawan**
2. Klik tombol **Create**
3. Isi data berikut:
   - **Nama**: Budi Santoso
   - **NIK Karyawan**: PAL-2024-001
   - **NIK KTP**: 3578012345670001
   - **Departemen**: Shipbuilding / Production
   - **Jabatan**: Welder Senior
   - **Tanggal Bergabung**: 01/03/2020
   - **Status**: Tetap (Permanent)
   - **BPJS Kesehatan**: 0001234567890
   - **BPJS Ketenagakerjaan**: JKN-001234567
4. Klik **Save**

### READ (Lihat Data)

1. Kembali ke daftar karyawan (breadcrumb atau menu)
2. Data yang baru dibuat akan muncul di Tree/List View
3. Klik pada nama karyawan untuk melihat detail di Form View
4. Gunakan filter dan search bar untuk mencari berdasarkan nama, NIK, atau departemen

### UPDATE (Ubah Data)

1. Buka record karyawan yang ingin diubah
2. Klik tombol **Edit**
3. Ubah field yang diinginkan (misal: ubah Jabatan menjadi "Kepala Regu Welding")
4. Klik **Save**

### DELETE (Hapus Data)

**Soft Delete (Arsip):**
1. Buka record karyawan
2. Klik **Action → Archive**
3. Karyawan tidak akan muncul di daftar default (gunakan filter "Archived" untuk melihat)

**Hard Delete:**
1. Dari Tree/List View, centang karyawan yang ingin dihapus
2. Klik **Action → Delete**
3. Konfirmasi penghapusan

## Hak Akses

| Group                  | Read | Write | Create | Delete |
|------------------------|------|-------|--------|--------|
| Human Capital User     | ✅   | ✅    | ✅     | ✅     |
| Human Capital Manager  | ✅   | ✅    | ✅     | ✅     |

## Kontributor

- **PT PAL Indonesia (Persero)** — Human Capital Division
- Dibuat untuk kebutuhan internal pengelolaan data karyawan

## Lisensi

LGPL-3 (GNU Lesser General Public License v3)
