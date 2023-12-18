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
