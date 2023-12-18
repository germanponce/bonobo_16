# -*- coding: utf-8 -*-
##############################################################################
#
# # Creado por :
# # German Ponce Dominguez - german.ponce@outlook.com
#
##############################################################################


from odoo import api, fields, models, _, tools, release
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class PurchaseOrder(models.Model):
    _name = 'purchase.order.line'
    _inherit ='purchase.order.line'

    wo_id = fields.Many2one('picking.work.order', 'Albaran de Trabajo')

class PurchaseOrderLine(models.Model):
    _name = 'purchase.order.line'
    _inherit ='purchase.order.line'
    
    wo_id = fields.Many2one('picking.work.order', 'Albaran de Trabajo')
