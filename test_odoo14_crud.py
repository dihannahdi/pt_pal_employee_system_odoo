#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""End-to-End CRUD Test for PT PAL Employee Management on Odoo 14"""
import xmlrpc.client
import sys

URL = 'http://localhost:8014'
DB = 'ptpal14'
USERNAME = 'admin'
PASSWORD = 'admin'

print('=== Odoo 14 E2E CRUD Test for PT PAL Employee Management ===')
print('')

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(URL))
version = common.version()
print('Server version: {}'.format(version.get('server_version', 'unknown')))

uid = common.authenticate(DB, USERNAME, PASSWORD, {})
if not uid:
    print('FAIL: Authentication failed')
    sys.exit(1)
print('Authenticated as uid={}'.format(uid))

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL))

# Assign admin to Human Capital Manager group
group_ids = models.execute_kw(DB, uid, PASSWORD, 'res.groups', 'search',
    [[['category_id.name', '=', 'PT PAL Human Capital'], ['name', '=', 'Human Capital Manager']]])
if group_ids:
    models.execute_kw(DB, uid, PASSWORD, 'res.users', 'write', [[uid], {'groups_id': [(4, group_ids[0])]}])
    print('Admin assigned to Human Capital Manager group (id={})'.format(group_ids[0]))

# ==================== CREATE ====================
print('')
print('=== TEST 1: CREATE ===')
test_data = [
    {
        'name': 'Budi Santoso',
        'nik_karyawan': 'PAL-2024-001',
        'nik_ktp': '3578012345670001',
        'department': 'shipbuilding',
        'position': 'Welder Senior',
        'join_date': '2020-03-01',
        'bpjs_kesehatan': '0001234567890',
        'bpjs_ketenagakerjaan': 'JKN-001234567',
        'employee_status': 'permanent',
        'active': True,
        'notes': 'Divisi Shipbuilding, pengalaman 4 tahun',
    },
    {
        'name': 'Siti Rahayu',
        'nik_karyawan': 'PAL-2024-002',
        'nik_ktp': '3578012345670002',
        'department': 'human_capital_services',
        'position': 'HR Staff',
        'join_date': '2021-06-15',
        'bpjs_kesehatan': '0001234567891',
        'bpjs_ketenagakerjaan': 'JKN-001234568',
        'employee_status': 'permanent',
        'active': True,
    },
    {
        'name': 'Ahmad Fauzi',
        'nik_karyawan': 'PAL-2024-003',
        'nik_ktp': '3578012345670003',
        'department': 'naval_architecture',
        'position': 'Naval Architect Junior',
        'join_date': '2024-01-10',
        'bpjs_kesehatan': '0001234567892',
        'bpjs_ketenagakerjaan': 'JKN-001234569',
        'employee_status': 'contract',
        'active': True,
    },
    {
        'name': 'Dewi Lestari',
        'nik_karyawan': 'PAL-2024-004',
        'nik_ktp': '3578012345670004',
        'department': 'quality_assurance',
        'position': 'QA Inspector',
        'join_date': '2023-08-20',
        'bpjs_kesehatan': '0001234567893',
        'bpjs_ketenagakerjaan': 'JKN-001234570',
        'employee_status': 'permanent',
        'active': True,
    },
    {
        'name': 'Riko Pratama',
        'nik_karyawan': 'PAL-2024-005',
        'nik_ktp': '3578012345670005',
        'department': 'mro',
        'position': 'Magang Teknisi MRO',
        'join_date': '2024-09-01',
        'employee_status': 'intern',
        'active': True,
    },
]

created_ids = []
for rec in test_data:
    rid = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'create', [rec])
    created_ids.append(rid)
    print('  CREATED: id={}, name={}, NIK={}, dept={}'.format(rid, rec['name'], rec['nik_karyawan'], rec['department']))
print('  Total created: {} records'.format(len(created_ids)))
print('  RESULT: PASS')

# ==================== READ ====================
print('')
print('=== TEST 2: READ ===')
records = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'search_read',
    [[['id', 'in', created_ids]]],
    {'fields': ['name', 'nik_karyawan', 'department', 'position', 'employee_status', 'nik_ktp', 'bpjs_kesehatan', 'join_date']})
for r in records:
    print('  READ id={}: {} | NIK={} | {} | {} | {} | joined={}'.format(
        r['id'], r['name'], r['nik_karyawan'], r['department'], r['position'], r['employee_status'], r['join_date']))
assert len(records) == 5, 'Expected 5 records, got {}'.format(len(records))
print('  Total read: {} records'.format(len(records)))
print('  RESULT: PASS')

# ==================== UPDATE ====================
print('')
print('=== TEST 3: UPDATE ===')
models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'write',
    [[created_ids[0]], {'position': 'Kepala Regu Welding', 'notes': 'Dipromosikan Maret 2026'}])
updated = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'read',
    [created_ids[0]], {'fields': ['name', 'position', 'notes']})
print('  UPDATED id={}: position="{}" notes="{}"'.format(created_ids[0], updated[0]['position'], updated[0]['notes']))
assert updated[0]['position'] == 'Kepala Regu Welding'
print('  RESULT: PASS')

# ==================== ARCHIVE (Soft Delete) ====================
print('')
print('=== TEST 4: ARCHIVE (Soft Delete) ===')
models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'write',
    [[created_ids[4]], {'active': False}])
archived = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'read',
    [created_ids[4]], {'fields': ['name', 'active']})
print('  ARCHIVED id={}: name={}, active={}'.format(created_ids[4], archived[0]['name'], archived[0]['active']))
assert archived[0]['active'] == False

visible = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'search_count',
    [[['id', 'in', created_ids]]])
print('  Visible (active only): {} of 5 (expected 4)'.format(visible))
assert visible == 4
print('  RESULT: PASS')

# ==================== UNARCHIVE ====================
print('')
print('=== TEST 5: UNARCHIVE ===')
models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'write',
    [[created_ids[4]], {'active': True}])
restored = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'read',
    [created_ids[4]], {'fields': ['name', 'active']})
print('  RESTORED id={}: name={}, active={}'.format(created_ids[4], restored[0]['name'], restored[0]['active']))
assert restored[0]['active'] == True
print('  RESULT: PASS')

# ==================== HARD DELETE ====================
print('')
print('=== TEST 6: HARD DELETE ===')
models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'unlink', [[created_ids[4]]])
remaining = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'search_count',
    [[['id', '=', created_ids[4]], ['active', 'in', [True, False]]]])
print('  Deleted id={}. Remaining with that id: {} (expected 0)'.format(created_ids[4], remaining))
assert remaining == 0
print('  RESULT: PASS')

# ==================== VALIDATION: NIK KTP ====================
print('')
print('=== TEST 7: VALIDATION - NIK KTP (must be 16 digits) ===')
try:
    bad = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'create', [{
        'name': 'Test Bad', 'nik_karyawan': 'PAL-BAD-001', 'nik_ktp': '12345',
        'department': 'shipbuilding', 'employee_status': 'permanent',
    }])
    models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'unlink', [[bad]])
    print('  FAIL: Should have raised validation error for 5-digit NIK')
    sys.exit(1)
except Exception as e:
    print('  Correctly rejected: short NIK KTP')
    print('  RESULT: PASS')

# ==================== VALIDATION: UNIQUE NIK KARYAWAN ====================
print('')
print('=== TEST 8: VALIDATION - Unique NIK Karyawan ===')
try:
    dup = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'create', [{
        'name': 'Duplicate NIK', 'nik_karyawan': 'PAL-2024-001',
        'department': 'mro', 'employee_status': 'contract',
    }])
    print('  FAIL: Should have raised unique constraint error')
    sys.exit(1)
except Exception as e:
    print('  Correctly rejected: duplicate NIK Karyawan')
    print('  RESULT: PASS')

# ==================== SEARCH FILTERS ====================
print('')
print('=== TEST 9: SEARCH & FILTER ===')
permanent = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'search_count',
    [[['employee_status', '=', 'permanent']]])
contract = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'search_count',
    [[['employee_status', '=', 'contract']]])
shipbuilding = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'search_count',
    [[['department', '=', 'shipbuilding']]])
print('  Permanent employees: {} (expected 3)'.format(permanent))
print('  Contract employees: {} (expected 1)'.format(contract))
print('  Shipbuilding dept: {} (expected 1)'.format(shipbuilding))
assert permanent == 3
assert contract == 1
assert shipbuilding == 1
print('  RESULT: PASS')

# ==================== CLEANUP ====================
print('')
print('=== CLEANUP ===')
remaining_ids = created_ids[:4]
models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'unlink', [remaining_ids])
final = models.execute_kw(DB, uid, PASSWORD, 'employee.management', 'search_count',
    [[['active', 'in', [True, False]]]])
print('  Cleaned up {} records. Total remaining: {}'.format(len(remaining_ids), final))

print('')
print('=' * 55)
print('  ALL 9 TESTS PASSED on Odoo 14!')
print('  Server: {}'.format(version.get('server_version', 'unknown')))
print('  Database: {}'.format(DB))
print('  Module: employee_management v14.0.1.0.0')
print('=' * 55)
