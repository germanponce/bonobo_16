# Copyright 2018-2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line", "product.secondary.unit.mixin"]
    _name = "sale.order.line"
    _secondary_unit_fields = {
        "qty_field": "product_uom_qty",
        "uom_field": "product_uom",
    }

    secondary_uom_unit_price = fields.Float(
        string="2nd unit price",
        digits="Product Price",
        compute="_compute_secondary_uom_unit_price",
    )

    product_uom_qty = fields.Float(
        store=True, readonly=False, compute="_compute_product_uom_qty", copy=True
    )

    @api.depends("secondary_uom_qty", "secondary_uom_id", "product_uom_qty")
    def _compute_product_uom_qty(self):
        self._compute_helper_target_field_qty()

    @api.onchange("product_uom")
    def onchange_product_uom_for_secondary(self):
        self._onchange_helper_product_uom_for_secondary()

    @api.onchange("product_id")
    def product_id_change_second_unit(self):
        """
        If default sales secondary unit set on product, put on secondary
        quantity 1 for being the default quantity. We override this method,
        that is the one that sets by default 1 on the other quantity with that
        purpose.
        """
        line_uom_qty = self.product_uom_qty
        self.secondary_uom_id = self.product_id.sale_secondary_uom_id
        if self.product_id.sale_secondary_uom_id:
            if line_uom_qty == 1.0:
                self.secondary_uom_qty = 1.0
                self.onchange_product_uom_for_secondary()
            else:
                self.product_uom_qty = line_uom_qty

    @api.depends("secondary_uom_qty", "product_uom_qty", "price_unit")
    def _compute_secondary_uom_unit_price(self):
        for line in self:
            if line.secondary_uom_id:
                try:
                    line.secondary_uom_unit_price = (
                        line.price_subtotal / line.secondary_uom_qty
                    )
                except ZeroDivisionError:
                    line.secondary_uom_unit_price = 0
            else:
                line.secondary_uom_unit_price = 0


class AccountMoveLine(models.Model):
    # _inherit = ["account.move.line", "product.secondary.unit.mixin"]
    _inherit = "account.move.line"

    # _secondary_unit_fields = {
    #     "qty_field": "quantity",
    #     "uom_field": "product_uom_id",
    # }

    secondary_uom_qty = fields.Float(string="2nd Qty", digits="Product Unit of Measure")
    secondary_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        string="2nd uom",
        ondelete="restrict",
    )

    secondary_uom_unit_price = fields.Float(
        string="2nd unit price",
        digits="Product Unit of Measure",
        store=False,
        readonly=True,
        compute="_compute_secondary_uom_unit_price",
    )

    # quantity = fields.Float(
    #     store=True, readonly=False, compute="_compute_product_uom_qty", copy=True
    # )


    # @api.depends("secondary_uom_qty", "secondary_uom_id", "quantity")
    # def _compute_product_uom_qty(self):
    #     self._compute_helper_target_field_qty()


    @api.onchange('quantity')
    def onchange_2nd_quantity(self):
        no_triggered = self._context.get('no_triggered', False)
        factor = self._get_factor_line()
        if not no_triggered and self.secondary_uom_id:
            if factor < 1:
                secondary_uom_qty = self.quantity / factor
                self.with_context(no_triggered=True).secondary_uom_qty = secondary_uom_qty
            else:
                secondary_uom_qty = self.quantity  *  factor
                self.with_context(no_triggered=True).secondary_uom_qty = secondary_uom_qty

    @api.onchange('secondary_uom_qty')
    def onchange_2nd_secondary_uom_qty(self):
        no_triggered = self._context.get('no_triggered', False)
        factor = self._get_factor_line()
        if not no_triggered and self.secondary_uom_id:
            if factor < 1:
                quantity = self.secondary_uom_qty * factor
                self.with_context(no_triggered=True).quantity = quantity
            else:
                quantity = self.secondary_uom_qty  /  factor
                self.with_context(no_triggered=True).quantity = quantity

    def _get_factor_line(self):
        return self.secondary_uom_id.factor * (
            self.product_uom_id.factor
            if self.product_uom_id != self.secondary_uom_id
            else 1.0
        )

    @api.depends("secondary_uom_qty", "quantity", "price_unit")
    def _compute_secondary_uom_unit_price(self):
        for line in self:
            if line.secondary_uom_id:
                try:
                    line.secondary_uom_unit_price = (
                        line.price_subtotal / line.secondary_uom_qty
                    )
                except ZeroDivisionError:
                    line.secondary_uom_unit_price = 0
            else:
                line.secondary_uom_unit_price = 0

