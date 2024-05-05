
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_repr, float_round, float_compare
from odoo.exceptions import ValidationError
from collections import defaultdict

class ProductProduct(models.Model):
    _inherit = 'product.product'

    packaging_qty = fields.Float(string="Packaging Qty",
        compute='_compute_packaging_qty')

    @api.depends('qty_available')
    def _compute_packaging_qty(self):
        for product in self:
            product.packaging_qty = product.qty_available
            product_packages = self.env['product.packaging'].search([('product_id', '=', product.id)], limit=1)
            if product_packages:
                first_product_package = product_packages[0]
                product.packaging_qty = product.qty_available / first_product_package.qty
            else:
                product.packaging_qty = 0.0  # Set a default value if no product packages found


