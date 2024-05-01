# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class customer_api(models.Model):
    _inherit = 'res.partner'

    last_name = fields.Char('Last Name')
    student_id = fields.Char('Student Unique ID')
    student_department_id = fields.Char(string='Campus')
    name = fields.Char(index=True, default_export_compatible=True)

    # @api.constrains('student_id')
    # def _check_fine_val(self):
    #     for record in self:
    #         student = self.env['res.partner'].sudo().search([('student_id', '=', record.student_id)], limit=1)
    #         if student:
    #             raise ValidationError("Student Already Exist")



