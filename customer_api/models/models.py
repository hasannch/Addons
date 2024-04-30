# -*- coding: utf-8 -*-

from odoo import models, fields, api


class customer_api(models.Model):
    _inherit = 'res.partner'

    last_name = fields.Char('Last Name')
    student_id = fields.Char('Student Unique ID')
    student_department_id = fields.Char(string='Campus')
    name = fields.Char(index=True, default_export_compatible=True)
