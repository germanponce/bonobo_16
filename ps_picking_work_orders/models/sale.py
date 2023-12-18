# -*- coding: utf-8 -*-
##############################################################################
#
# # Creado por :
# # German Ponce Dominguez - german.ponce@outlook.com
#
##############################################################################


from odoo import api, fields, models, _, tools, release
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class SaleOrder(models.Model):
    _name = 'sale.order.line'
    _inherit ='sale.order.line'

    wo_id = fields.Many2one('picking.work.order', 'Albaran de Trabajo')

class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit ='sale.order.line'
    
    wo_id = fields.Many2one('picking.work.order', 'Albaran de Trabajo')
