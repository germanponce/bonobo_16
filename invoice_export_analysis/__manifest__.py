# -*- coding: utf-8 -*-

{
    'name': 'Exportar Facturas',
    'version': '0.1.0',
    'category': 'Accounting',
    'description': """
    Report that shows a specific moves
    """,
    'author': 'German Ponce',
    'maintainer':"german.ponce@outlook.com",
    'website': 'http://poncesoft.blogspot.com',
    'depends': [
        "stock_account",
        "purchase_stock",
        "account",
        # "stock_landed_costs",
        # "l10n_mx_edi_landing",
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/invoice_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
