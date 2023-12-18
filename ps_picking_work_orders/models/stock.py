# -*- coding: utf-8 -*-
##############################################################################
#
# # Creado por :
# # German Ponce Dominguez - german.ponce@outlook.com
#
##############################################################################


from odoo import api, fields, models, _, tools, release
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit ='stock.picking'

    purchase_wo_id = fields.Many2one('picking.work.order', 'P. Albaran Trabajo')
    sale_wo_id = fields.Many2one('picking.work.order', 'V. Albaran Trabajo')

class StockMove(models.Model):
    _name = 'stock.move'
    _inherit ='stock.move'
    
    purchase_wo_id = fields.Many2one('picking.work.order', ' P. Albaran Trabajo')
    sale_wo_id = fields.Many2one('picking.work.order', 'V. Albaran Trabajo')
