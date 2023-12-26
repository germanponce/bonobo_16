# -*- coding: utf-8 -*-
# Coded by German Ponce Dominguez 
#     ▬▬▬▬▬.◙.▬▬▬▬▬  
#       ▂▄▄▓▄▄▂  
#    ◢◤█▀▀████▄▄▄▄▄▄ ◢◤  
#    █▄ █ █▄ ███▀▀▀▀▀▀▀ ╬  
#    ◥ █████ ◤  
#     ══╩══╩═  
#       ╬═╬  
#       ╬═╬ Dream big and start with something small!!!  
#       ╬═╬  
#       ╬═╬ You can do it!  
#       ╬═╬   Let's go...
#    ☻/ ╬═╬   
#   /▌  ╬═╬   
#   / \
# Cherman Seingalt - german.ponce@outlook.com

{
    'name': 'Formato albaran - Grupo SLS',
    'category': 'Maeda',
    'description': """

        Agrega Modificaciones al Reporte: 
         * Albaran

    """,
    'author': 'German Ponce Dominguez',
    'website': 'http://poncesoft.blogspot.mx',
    "support": "german.ponce@outlook.com",
    'depends': [
                    'base',
                    'stock',
                    'sale_stock',
                    'account',
                ],
    'data': [
        'security/ir.model.access.csv',
        'stock_view.xml',
        'report/stock_report_pdf.xml',
        'report/stock_report_convencional_pdf.xml',
        ],
    'installable': True,
}