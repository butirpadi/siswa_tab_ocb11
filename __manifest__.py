# -*- coding: utf-8 -*-
{
    'name': "Tabungan Siswa",

    'summary': """
        Aplikasi Pencatatan Transaksi Tabungan Siswa""",

    'description': """
        Aplikasi Pencatatan Transaksi Tabungan Siswa
    """,

    'author': "Tepat Guna Karya",
    'website': "http://www.tepatguna.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Education',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','siswa_ocb11'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/ir_default_data.xml',
        'views/tabungan.xml',
        'views/res_siswa.xml',
        'views/dashboard_tabungan.xml',
        'views/wizard_report_tabungan.xml',
        'views/wizard_saldo_tabungan.xml',
        'report/report_tabungan_template.xml',
        'report/report_saldo_tabungan.xml',
        'report/report_saldo_tabungan_detail.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}