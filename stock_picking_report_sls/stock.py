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

from odoo import api, fields, models, _, tools, SUPERUSER_ID
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta

import logging
_logger = logging.getLogger(__name__)

class BonoboOrigin(models.Model):
    _name = 'bonobo.origin'
    _description = 'Bonobo Origen'
    
    name = fields.Char('Descripcion', size=128, required=True)

class BonoboAgricultura(models.Model):
    _name = 'bonobo.agricultura'
    _description = 'Bonobo Agricultura'
    
    name = fields.Char('Descripcion', size=128, required=True)

class BonoboVariedad(models.Model):
    _name = 'bonobo.variedad'
    _description = 'Bonobo Variedad'
    
    name = fields.Char('Descripcion', size=128, required=True)


class BonoboCalibre(models.Model):
    _name = 'bonobo.calibre'
    _description = 'Bonobo Calibre'
    
    name = fields.Char('Descripcion', size=128, required=True)

    
    
    
class ProductTemplate(models.Model):
    _inherit ='product.template'

    bonobo_origin = fields.Many2one('bonobo.origin', 'Origen')
    bonobo_agricultrura = fields.Many2one('bonobo.agricultura', 'Agricultura')
    bonobo_variedad = fields.Many2one('bonobo.variedad', 'Variedad')
    bonobo_calibre = fields.Many2one('bonobo.calibre', 'Calibre')

# Crear campos extras a Odoo en la ficha de Productos, Campos que hay que añadir; Origen, Agricultura, variedad, calibre
# Doble unidad de medida para gestionar KG y Cajas

# Creación de informe KARDEX para generar balances de masas: campos en el informe Origen, Agricultura, variedad, calibre, kg vendidos, cajas, 
# vendidas Creación de informe en contabilidad para exportar en excel, adjunto es este email el ejemplo de que tiene que ser igual, 
# diferenciando los impuestos Instalación, configuración y parametrización del módulo de la Oca de Odoo Instractac pruebas y puesta en marcha, 
# Crear plantilla personalizada para enviar facturas y albaranes mediante el correo de Odoo automatizado


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit ='account.move'

    project_reference = fields.Char('Nombre de la Obra', size=128)

    def get_sale_order_name(self):
        sale_orders = ""
        for line in self.invoice_line_ids:
            if line.sale_line_ids:
                order_id = line.sale_line_ids[0].order_id
                if order_id.name not in sale_orders:
                    sale_orders = sale_orders+", "+order_id.name if sale_orders else order_id.name
        return sale_orders

    def get_payments_from_terms(self):
        payment_term_list = []
        date_ref = self.invoice_date or fields.Date.context_today(self)      
        to_compute_termns = self.invoice_payment_term_id.compute(self.amount_total, date_ref=date_ref, currency=self.currency_id)
        #print("############ to_compute_termns >>>>>>>>>>>> ", to_compute_termns)
        if to_compute_termns:
            return to_compute_termns
        return payment_term_list
