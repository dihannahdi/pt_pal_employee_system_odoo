# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EmployeeManagement(models.Model):
    _name = 'employee.management'
    _description = 'Manajemen Karyawan PT PAL Indonesia'
    _order = 'nik_karyawan asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Nama Lengkap',
        required=True,
    )
    nik_karyawan = fields.Char(
        string='Nomor Induk Karyawan',
        required=True,
        copy=False,
        help='Nomor Induk Karyawan (NIK Perusahaan) yang unik untuk setiap karyawan PT PAL.',
    )
    nik_ktp = fields.Char(
        string='NIK (KTP)',
        size=16,
        help='Nomor Induk Kependudukan sesuai KTP (16 digit).',
    )
    department = fields.Selection(
        selection=[
            ('human_capital_services', 'Human Capital Services'),
            ('human_capital_development', 'Human Capital Development'),
            ('organization_development', 'Organization Development'),
            ('shipbuilding', 'Shipbuilding / Production'),
            ('naval_architecture', 'Naval Architecture & Engineering'),
            ('quality_assurance', 'Quality Assurance'),
            ('finance_risk', 'Finance & Risk Management'),
            ('general_engineering', 'General Engineering'),
            ('mro', 'Maintenance, Repair & Overhaul (MRO)'),
            ('procurement', 'Procurement & Supply Chain'),
            ('corporate_secretary', 'Corporate Secretary'),
            ('information_technology', 'Information Technology'),
            ('marketing', 'Marketing & Business Development'),
            ('hsse', 'Health, Safety, Security & Environment (HSSE)'),
            ('internal_audit', 'Internal Audit'),
            ('other', 'Lainnya'),
        ],
        string='Departemen',
        required=True,
    )
    position = fields.Char(
        string='Jabatan',
    )
    join_date = fields.Date(
        string='Tanggal Bergabung',
    )
    bpjs_kesehatan = fields.Char(
        string='No. BPJS Kesehatan',
    )
    bpjs_ketenagakerjaan = fields.Char(
        string='No. BPJS Ketenagakerjaan',
    )
    employee_status = fields.Selection(
        selection=[
            ('permanent', 'Tetap (Permanent)'),
            ('contract', 'Kontrak (Contract)'),
            ('intern', 'Magang (Intern)'),
        ],
        string='Status Karyawan',
        default='permanent',
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Jika tidak dicentang, karyawan dianggap non-aktif dan tidak akan muncul di daftar default.',
    )
    notes = fields.Text(
        string='Catatan',
    )

    _sql_constraints = [
        (
            'nik_karyawan_unique',
            'UNIQUE(nik_karyawan)',
            'Nomor Induk Karyawan harus unik! NIK ini sudah terdaftar.'
        ),
    ]

    @api.constrains('nik_ktp')
    def _check_nik_ktp(self):
        for record in self:
            if record.nik_ktp:
                if not record.nik_ktp.isdigit():
                    raise ValidationError('NIK KTP harus berupa angka!')
                if len(record.nik_ktp) != 16:
                    raise ValidationError('NIK KTP harus terdiri dari 16 digit!')
