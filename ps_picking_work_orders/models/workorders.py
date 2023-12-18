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

import logging
import warnings

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessError, ValidationError
from odoo.osv import expression
from odoo.tools import config
from odoo.tools.safe_eval import safe_eval, time

from itertools import zip_longest


class PickingWorkOrder(models.Model):
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _name = 'picking.work.order'
    _description = 'Gestión Albaranes de Trabajo'
    
    def _get_current_user(self):
        return self.env.user.id

    def _get_company(self):
        return self.env.user.company_id.id

    state = fields.Selection([
                            ('Cancelada', 'Cancelada'),
                            ('Borrador', 'Borrador'),
                            ('Proceso', 'En Proceso'),
                            ('Pausa', 'Pausa'),
                            ('Cerrada', 'Cerrada'),
                             ], string="Estado", default="Borrador")

    name = fields.Char('Folio', size=128)

    presupuesto = fields.Char('Presupuesto', size=128)

    expediente = fields.Char('Expediente', size=128)

    workorder_date = fields.Date('Fecha Albaran', default=fields.Date.context_today)
    
    start_time = fields.Float('Hora Comienzo')

    end_time = fields.Float('Hora Final')

    partner_id = fields.Many2one('res.partner', 'Cliente')

    partner_contact_id = fields.Many2one('res.partner', 'Contacto')

    partner_oficial = fields.Char('Oficial', size=128)

    partner_ayudante = fields.Char('Ayudante', size=128)

    address_aditional_info = fields.Char('Datos adicionales dirección', size=128)
    
    customer_order = fields.Char('Pedido cliente', size=128)

    notes = fields.Text('Notas')

    assigned_user_id = fields.Many2one('res.users', 'Asignado al Usuario', default=_get_current_user)

    invoice_line_ids = fields.One2many('picking.work.order.invoice.item', 'wo_id', 'Conceptos de Facturacion')

    technical_line_ids = fields.One2many('picking.work.order.technical.line', 'wo_id', 'Técnicas empleadas')

    qualify_line_ids = fields.One2many('picking.work.order.qualify.work', 'wo_id', 'Calificación del trabajo')

    expenses_officer_line_ids = fields.One2many('picking.work.order.expense.line', 'wo_id', 'Gastos Oficial')

    expenses_auxiliar_line_ids = fields.One2many('picking.work.order.expense.line', 'wo_aux_id', 'Gastos Ayudante')

    officer_signature = fields.Char('Firma Oficial')

    auxiliar_signature = fields.Char('Firma Ayudante')

    customer_signature = fields.Char('Firma Cliente')
    
    supervisor_signature = fields.Char('Firma Supervisor')

    company_id = fields.Many2one('res.company', 'Compañia', default=_get_company)

    def get_technicals_and_qualifications(self):
        all_data_join = []
        technical_line_ids = []
        qualify_line_ids = []
        for techcl in self.technical_line_ids:
            if techcl.name:
                technical_line_ids.append(techcl.name)
        for qlf in self.qualify_line_ids:
            qualify_line_ids.append(qlf.name)
        for x, y in zip_longest(technical_line_ids, qualify_line_ids):
            if x:
                tecnhical = x
            if y:
                qualify = y
            if not x:
                tecnhical = False
            if not y:
                qualify = False
            join_line = [tecnhical, qualify]
            all_data_join.append(join_line)
        return all_data_join

    def get_all_expenses(self):
        all_data_join = []
        expenses_officer_line_ids = []
        expenses_auxiliar_line_ids = []
        for oficial_e in self.expenses_officer_line_ids:
            expenses_officer_line_ids.append(oficial_e)
        for ayudante_e in self.expenses_auxiliar_line_ids:
            expenses_auxiliar_line_ids.append(ayudante_e)
        for x, y in zip_longest(expenses_officer_line_ids, expenses_auxiliar_line_ids):
            if x:
                oficial_line = x
            if y:
                qyudante_line = y
            if not x:
                oficial_line = False
            if not y:
                qyudante_line = False
            join_line = [oficial_line, qyudante_line]
            all_data_join.append(join_line)
        return all_data_join

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.product_image = self.product_id.image_1920
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('picking.work.order') or '/'
        res = super(PickingWorkOrder, self).create(vals)
        return res


    def action_draft(self):
        for record in self:
            record.state = 'Borrador'

    def action_cancel(self):
        for record in self:
            record.state = 'Cancelada'

    def action_done(self):
        for record in self:
            record.state = 'Cerrada'

    def action_start(self):
        for record in self:
            record.state = 'Proceso'

    def action_pause(self):
        for record in self:
            record.state = 'Pausa'


class PickingWorkOrderInvoiceItem(models.Model):
    _name = 'picking.work.order.invoice.item'
    _description = 'Facturacion Albaranes de Trabajo'
    _rec_name = "product_id"

    wo_id = fields.Many2one('picking.work.order', 'WO ID')

    product_id = fields.Many2one('product.product', 'Concepto de trabajo', size=128)
    quantity = fields.Float('Cantidad', digits=(14,2))

class PickingWorkOrderTechnicalLine(models.Model):
    _name = 'picking.work.order.technical.line'
    _description = 'Tecnicas Empleadas'

    wo_id = fields.Many2one('picking.work.order', 'WO ID')

    name = fields.Char('Tecnica', size=128)


class PickingWorkOrderQualifyWork(models.Model):
    _name = 'picking.work.order.qualify.work'
    _description = 'Calificación del Trabajo'

    wo_id = fields.Many2one('picking.work.order', 'WO ID')

    name = fields.Char('Calificación', size=128)

class PickingWorkOrderExpenseLine(models.Model):
    _name = 'picking.work.order.expense.line'
    _description = 'Calificación del Trabajo'

    wo_id = fields.Many2one('picking.work.order', 'WO ID')

    wo_aux_id = fields.Many2one('picking.work.order', 'WO ID')

    quantity = fields.Float('Cantidad', digits=(14,2))

    name = fields.Selection([
                                ('Km.','Km.'),
                                ('Dietas','Dietas'),
                                ('Comidas','Comidas'),
                                ('H. Extras 1','H. Extras 1'),
                                ('H. Extras 2','H. Extras 2'),
                            ],'Concepto', size=128)
    
    total = fields.Float('Total', digits=(14,2))

    parcial_payment = fields.Float('Abonado', digits=(14,2))
    parcial_residual = fields.Float('Pendiente', digits=(14,2))



    @api.onchange('total','parcial_payment')
    def onchange_parcial_payment(self):
        if self.total or self.parcial_payment:
            self.parcial_residual = self.total - self.parcial_payment
    