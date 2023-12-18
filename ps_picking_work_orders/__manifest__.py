# -*- encoding: utf-8 -*-
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
    "name": "Albaranes de Trabajo",
    "author": "German Ponce Dominguez",
    "website": "https://poncesoft.blogspot.com",
    "support": "german.ponce@outlook.com",
    "category": "Stock",
    "summary": "Permite gestionar los Albaranes de Trabajo.",
    "description": """

                   """,
    "version": "14.0.1",
    "depends": ['account'],
    "application": True,
    "data": [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/workorders_view.xml',
        'reports/report_wo_picking.xml',
    ],
    "auto_install": False,
    "installable": True,
}
