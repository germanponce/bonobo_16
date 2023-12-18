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
    'name': 'Formato Presupuesto/Pedido - Grupo SLS',
    'category': 'Maeda',
    'description': """

        Agrega Modificaciones al Reporte: 
         * Presupuesto/Pedido

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
        'sale_view.xml',
        'report/sale_report_pdf.xml',
        ],
    'installable': True,
}