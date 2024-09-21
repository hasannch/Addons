# -*- coding: utf-8 -*-
# from odoo import http


# class BillFromOldSystemReport(http.Controller):
#     @http.route('/bill_from_old_system_report/bill_from_old_system_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bill_from_old_system_report/bill_from_old_system_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bill_from_old_system_report.listing', {
#             'root': '/bill_from_old_system_report/bill_from_old_system_report',
#             'objects': http.request.env['bill_from_old_system_report.bill_from_old_system_report'].search([]),
#         })

#     @http.route('/bill_from_old_system_report/bill_from_old_system_report/objects/<model("bill_from_old_system_report.bill_from_old_system_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bill_from_old_system_report.object', {
#             'object': obj
#         })

