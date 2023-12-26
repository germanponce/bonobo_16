# -*- coding: utf-8 -*-

{
    'name': 'Stock Kardex Report',
    'version': '0.1.0',
    'category': 'Stock',
    'description': """
    Report that shows a specific product stock moves
    """,
    'author': 'German Ponce',
    'maintainer':"german.ponce@outlook.com",
    'website': 'http://poncesoft.blogspot.com',
    'depends': [
        "stock_account",
        "purchase_stock",
        "stock_picking_report_sls",
        # "stock_landed_costs",
        # "l10n_mx_edi_landing",
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'wizard/kardex_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
