from odoo import api, fields, models


class SaleOrderLineSequence(models.Model):
    _inherit = "sale.order.line"

    order_line_number = fields.Integer(
        string="Sequence", compute="_compute_line_number", store=True
    )

    @api.depends("order_id.order_line", "sequence")
    def _compute_line_number(self):
        orders = self.mapped("order_id")
        for order in orders:
            number = 1
            for rec in order.order_line.sorted(key=lambda r: r.sequence):
                rec.order_line_number = number
                number += 1
