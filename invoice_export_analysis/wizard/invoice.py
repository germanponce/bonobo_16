#-*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

#PARA FECHAS
from datetime import datetime, timedelta

####### TRABAJAR CON LOS EXCEL
import base64
import xlsxwriter
import tempfile
from xlsxwriter.utility import xl_rowcol_to_cell

#OTROS
import re
from collections import defaultdict
from odoo.tools import float_compare, float_round, float_is_zero, pycompat

import logging
_logger = logging.getLogger(__name__)


class InvoiceExportAnalysis(models.TransientModel):
    _name = 'invoice.export.analysis'

    #CAMPOS PARA GENERAR EL ARCHIVO
    datas_fname = fields.Char('Nombre del Archivo',size=256)
    file = fields.Binary('Layout')
    download_file = fields.Boolean('Archivo Listo')
    cadena_decoding = fields.Text('Archivo')

    company_id = fields.Many2one('res.company', 'Compañia', default=lambda self: self.env.user.company_id, required=True)

    output_type = fields.Selection([
                                     ('view','Análisis Odoo'),
                                     ('xlsx','Excel')
                                    ], 'Tipo Informe', default="xlsx")

    def calculate(self):
        """METODO PRINCIPAL DEL MODULO KARDEX"""
        cr = self.env.cr
        context = self._context
        active_ids = context.get('active_ids', [])
        return self.export_xlsx_file()
    
    def get_lines(self,):
        xlines = []
        context = self._context
        active_ids = context.get('active_ids', [])
        #SE BUSCAN LOS IDS DE LOS REGISTROS DENTRO DEL RANGO DE FECHAS SELECCIONADO
        move_obj = self.env['account.move']
        
        taxes_name_list = []
        for rec in move_obj.browse(active_ids):
            print ("### o.tax_totals: ", rec.tax_totals)
            tax_totals = rec.tax_totals

            tax_subtotals = tax_totals['subtotals']
            for subtotal in tax_subtotals:
                subtotal_to_show = subtotal['name']
                tax_details = tax_totals['groups_by_subtotal'][subtotal_to_show]
                print ("### tax_details: ", tax_details)
                for tax_d in tax_details:
                    tax_group_name = tax_d.get('tax_group_name','')
                    tax_group_amount = tax_d.get('tax_group_amount', 0.0)
                    if tax_group_name.upper() not in taxes_name_list:
                        taxes_name_list.append(tax_group_name.upper())
        for rec in move_obj.browse(active_ids):
            invoice_taxes_dict = {}

            tax_totals = rec.tax_totals
            tax_subtotals = tax_totals['subtotals']
            for subtotal in tax_subtotals:
                subtotal_to_show = subtotal['name']
                tax_details = tax_totals['groups_by_subtotal'][subtotal_to_show]
                print ("### tax_details: ", tax_details)
                for tax_d in tax_details:
                    tax_group_name = tax_d.get('tax_group_name','')
                    tax_group_amount = tax_d.get('tax_group_amount', 0.0)
                    if tax_group_name.upper() not in invoice_taxes_dict:
                        invoice_taxes_dict[tax_group_name.upper()] = tax_group_amount
            line_data = {
                            'FECHA': rec.invoice_date,
                            'NUMERO': rec.name,
                            'EMPRESA': rec.partner_id.name,
                            'NIF': rec.partner_id.vat,
                            'BASE IMPONIBLE': rec.amount_untaxed,
                            'TOTAL': rec.amount_total,
                        }
            for tax_name in taxes_name_list:
                tax_name_amount = invoice_taxes_dict.get('tax_name',0.0)
                line_data[tax_name] = tax_name_amount
            xlines.append(line_data)


        columns = [
                ['FECHA', 'DATE'],
                ['NUMERO', 'CHAR'],
                ['EMPRESA', 'CHAR'],
                ['NIF', 'CHAR'],
                ['BASE IMPONIBLE', 'FLOAT'],
                ]
        for tax_name in taxes_name_list:
            columns.append([tax_name, 'FLOAT'])
        columns.append(['TOTAL', 'FLOAT'])
        return xlines,columns
   
    def prepare_worksheet(self, workbook, data_exists, row=3):
        """
        crea una pestaña de excel
        regresa el workbook 
        y el row final
        """
        #print('prepare_worksheet')
        if workbook:
            cell_formats = self.get_cell_formats(workbook)
        worksheet = False

        xlines,columns = self.sudo().get_lines()

        if len(xlines) > 0 and not workbook:
            data_exists = True

        if len(xlines) > 0 and workbook:
            data_exists = True

            #se crea pestaña si no se ha creado aun
            if not worksheet:
                worksheet = workbook.add_worksheet('Facturas')
                # Widen the first column to make the text clearer.
                worksheet.set_column('A:K', 20)

                #SE ESTABLECE ENCABEZADO
                worksheet = self.set_worksheet_header(worksheet, cell_formats)

            #SE CREA LA TABLA DEL REPORTE
            #SE CREAN LOS NOMBRES DE COLUMNAS
            #row = start_row # la primera sera en 7
            worksheet.write(row ,0, "NIF: "+str(self.company_id.vat or ""), cell_formats['BOLD'])
            row += 1
            column = 0
            column_titles = [x[0] for x in columns]
            for title in column_titles:
                worksheet.write(row ,column, title, cell_formats['BLUE_BG'])
                column += 1
            row += 1
            ########################################

            for line in xlines:
                column = 0
                for cell in column_titles:
                    format = [x[1] for x in columns if x[0]==cell][0]
                    x_format = cell_formats[format]

                    worksheet.write(row ,column, line[cell],x_format)

                    column += 1
                row += 1
            row += 1

        return workbook, data_exists


    def get_cell_formats(self, workbook):
        """
        crea los formatos de celda del archivo
        devuelve diccionario con formatos de celda
        """
        #print('get_cell_formats')
        #FORMATOS DE CELDA ###########
        bold = workbook.add_format({'bold': True})
        blue_bg =  workbook.add_format()
        blue_bg.set_font_color('white')
        blue_bg.set_bold()
        blue_bg.set_bg_color('blue')


        totals_blue_bg =  workbook.add_format({'num_format': '#,##0.00'})
        totals_blue_bg.set_font_color('white')
        totals_blue_bg.set_bold()
        totals_blue_bg.set_bg_color('blue')

        border = workbook.add_format()
        border.set_border(1)
        #border.set_bold()

        report_title_style = workbook.add_format({'bold': True})
        report_title_style.set_font_size(12)

        border_number = workbook.add_format({'num_format': '#,##0.00'})
        border_number.set_border(1)

        borderless_num_format = workbook.add_format({'num_format': '#,##0.00'})
        borderless_num_format.set_bold()

        border_date = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        border_date.set_border(1)

        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})

        cell_formats = {
            'CHAR': border,
            'TEXT': border,
            'BOOLEAN': border,
            'INTEGER':border_number,
            'FLOAT':border_number,
            'DATE':border_date,
            'DATETIME':border_date,

            'TITLE': report_title_style,
            'TITLE_DATE': date_format,
            'BOLD': bold,
            'BLUE_BG': blue_bg,
        }
        return cell_formats
        ##############################3


    def set_worksheet_header(self, worksheet, cell_formats):
        """
        establece el encabezado de la pestaña
        """
        #print('set_worksheet_header')
        report_title = 'Reporte Facturas Exportadas'

        date = datetime.now().strftime('%d-%m-%Y')

        #ENCABEZADO####################################################
        worksheet.write('A1', self.company_id.name.upper(), cell_formats['TITLE'])
        worksheet.write('A2', report_title, cell_formats['TITLE'])
        worksheet.write('B2', date, cell_formats['BOLD'])
        return worksheet

    
    def export_xlsx_file(self):
        #print('export_xlsx_file')

        company_name = self.company_id.name
        fname=tempfile.NamedTemporaryFile(suffix='.xlsx',delete=False)
        workbook = xlsxwriter.Workbook(fname)
        date = datetime.now().strftime('%d-%m-%Y')
        datas_fname = 'FACTURAS_'+str(date)+".xlsx" # Nombre del Archivo

        #se añade pestaña(s)
        row = 7
        data_exists = False
        workbook, data_exists = self.prepare_worksheet(workbook, data_exists)

        if not data_exists:
            raise ValidationError(_('Los parametros seleccionados actualmente no generan informacion para el reporte, intente modificándolos.'))
            return {}

        ### Finalizando con la Generación del Reporte en Excel ###
        workbook.close()
        f = open(fname.name, "rb")
        data = f.read()
        f.close()

        self.write({'cadena_decoding':"",
            'datas_fname':datas_fname,
            'file': base64.b64encode(data),
            'download_file': True})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.export.analysis',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
            }


