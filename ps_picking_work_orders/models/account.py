# -*- coding: utf-8 -*-
##############################################################################
#
# # Creado por :
# # German Ponce Dominguez - german.ponce@outlook.com
#
##############################################################################


from odoo import api, fields, models, _, tools, release
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class AccountMove(models.Model):
    _name = 'account.move'
    _inherit ='account.move'

    purchase_wo_id = fields.Many2one('picking.work.order', 'P. Albaran de Trabajo')
    sale_wo_id = fields.Many2one('picking.work.order', 'V. Albaran de Trabajo')

class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _inherit ='account.move.line'

    purchase_wo_id = fields.Many2one('picking.work.order', 'P. Albaran de Trabajo')
    sale_wo_id = fields.Many2one('picking.work.order', 'V. Albaran de Trabajo')
