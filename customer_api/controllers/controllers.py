from odoo import http, exceptions
from odoo.http import request
from odoo.exceptions import UserError, MissingError, AccessError, ValidationError

from odoo import http
from odoo.http import request
import logging
import json

_logger = logging.getLogger(__name__)


class OdooRestful(http.Controller):

    # Customer API......................................

    @http.route(route='/read/customer', type='json', auth='user')
    def read_partners(self, **kwargs):
        user = request.env.user
        partners_sheet = request.env['res.partner'].sudo().search([])
        partners_data = []
        for partners in partners_sheet:
            data = {
                'name': partners.name,
                'last_name': partners.last_name,
                'student_id': partners.student_id,
                'student_department_id': partners.student_department_id,
                'email': partners.email,
            }
            partners_data.append(data)
        response = {'status': 200, 'response': partners_data, 'message': 'Success'}
        return response

    @http.route(route='/student/balance', type='json', auth='user')
    def read_student(self, **kwargs):
        # Extracting query parameters
        # domain = []
        # data = json.loads(request.httprequest.data.decode('utf-8'))
        # params = data.get('params', {})


        part = kwargs.get('student_id')

        # Search for records based on the domain
        partner = request.env['res.partner'].sudo().search([('student_id', '=', part)], limit=1)

        records = request.env['account.move.line'].sudo().search([('partner_id', '=',partner.id)])

        # Preparing response data
        products_data = []
        for record in records:
            data = {
                'student_name': record.partner_id.name,
                'name': record.name,
                'debit': record.debit,
                'credit': record.credit,
                'date': record.date.strftime('%Y-%m-%d'),
                'balance': record.balance,  # assuming balance calculation
            }
            products_data.append(data)

        response = {'status': 200, 'response': products_data, 'message': 'Success'}
        return response

    # create customer Api

    @http.route('/create/customer', type='json', methods=['POST'], auth='user')
    def create_customer(self, **kwargs):
        try:
            # Attempt to load JSON data directly from the request body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            params = data.get('params', {})

            _logger.info("Received data: %s", data)
            name = params.get('name')
            email = params.get('email')
            student_id = params.get('student_id')
            # company_type = params.get('company_type', "company")
            student = request.env['res.partner'].sudo().search([('student_id', '=',student_id)], limit=1)
            if not student:


                new_customer = request.env['res.partner'].sudo().create({
                    'name': name,  # Combining name and last name for the full name
                    # 'last_name': last_name,
                    'student_id': student_id,
                    # 'student_department_id': student_department_id,
                    # 'company_type': company_type,
                    'email': email,
                })

            # Successful creation response
                return {'success': True, 'message': 'Customer created successfully', 'id': new_customer.id}
            else:
                return {'success': True, 'message': 'Already Exist',}


        except Exception as e:
            _logger.error("Failed to create customer: %s", str(e))
            return {'success': False, 'message': 'Failed to create customer: {}'.format(str(e))}

    # update customer api
    @http.route('/update/customer', type='json', auth='user')
    def update_customer(self):
        try:
            # Parse JSON data directly from request body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            params = data.get('params', {})
            partner_id = params.get('student_id')
            partner = request.env['res.partner'].sudo().search([('student_id', '=', partner_id)], limit=1)
            if partner:
                partner.write({
                    'name': params.get('name'),
                    'last_name': params.get('last_name'),  # Make sure this field exists in your model
                    'student_id': params.get('student_id'),  # Make sure this field exists in your model
                    'student_department_id': params.get('student_department_id'),
                    'email': params.get('email'),
                })
                return {'success': True, 'message': 'Customer updated successfully', 'id': partner.id}
            else:
                return {'success': False, 'message': 'Customer not found'}
        except UserError as e:
            _logger.error(f"Failed to update customer: {e}")
            return {'success': False, 'message': f"Failed to update customer: {e}"}
        except Exception as e:
            _logger.error(f"Unexpected error: {e}")
            return {'success': False, 'message': f"An unexpected error occurred: {e}"}

    # Product APIs.................................................................
    @http.route('/create/product', type='json', auth='user')
    def create_products(self, **kwargs):
        try:
            # Directly parsing JSON data from the request body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            params = data.get('params', {})

            new_product = request.env['product.template'].sudo().create({
                'name': params.get('name'),
                'type': params.get('detailed_type', 'product'),  # Assuming 'type' is the correct field
                'list_price': params.get('list_price'),
                'standard_price': params.get('standard_price'),
            })
            return {'success': True, 'message': 'Product created successfully', 'product_id': new_product.id}
        except exceptions.ValidationError as e:
            _logger.error("Validation error: %s", str(e))
            return {'success': False, 'message': 'Failed to create product due to a validation error.'}
        except Exception as e:
            _logger.error("Unexpected error: %s", str(e))
            return {'success': False, 'message': 'An unexpected error occurred.'}

    @http.route(route='/read/products', type='json', auth='user')
    def read_products(self, **kwargs):
        products = request.env['product.template'].sudo().search([])
        products_data = []
        for product in products:
            data = {
                'name': product.name,
                'detailed_type': product.detailed_type,
                'list_price': product.list_price,
                'standard_price': product.standard_price,
            }
            products_data.append(data)
        response = {'status': 200, 'response': products_data, 'message': 'Success'}
        return response

    # update api product

    @http.route('/update/product', type='json', auth='user')
    def update_product(self):
        try:
            # Parse the JSON data directly from the request body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            params = data.get('params', {})

            product_id = int(params.get('id'))
            if not product_id:
                return {'success': False, 'message': 'Missing product ID.'}
            product = request.env['product.template'].sudo().search([('id', '=', product_id)], limit=1)

            if not product.exists():
                return {'success': False, 'message': 'Product not found.'}

            update_vals = {
                'name': params.get('name', product.name),
                # Ensure 'detailed_type' matches your model's field if it's custom.
                'list_price': params.get('list_price', product.list_price),
                'standard_price': params.get('standard_price', product.standard_price),
            }
            product.write(update_vals)

            return {'success': True, 'message': 'Product updated successfully.', 'id': product.id}

        except ValueError as e:
            _logger.error(f"JSON parsing error: {e}")
            return {'success': False, 'message': 'Invalid JSON data.'}

        except Exception as e:
            _logger.error(f"Unexpected error: {type(e).__name__} - {e}")
            return {'success': False, 'message': f"An unexpected error occurred: {type(e).__name__} - {e}"}

    @http.route(route='/delete/product', type='json', auth='user')
    def delete_attendance(self, **kwargs):
        product_id = kwargs.get('id')
        response = {'success': False, 'message': 'Record not found'}
        if product_id:
            products = request.env['product.template'].sudo().search([('id', '=', product_id)])
            if products:
                products.sudo().unlink()
                response = {'success': True, 'message': 'Record has been delete successfully'}
        return response

    # Invoice API............................................................................................

    @http.route('/read/invoices', type='json', auth='user')
    def read_invoices(self, **kwargs):
        invoices = request.env['account.move'].sudo().search([])
        invoices_data = []
        for invoice in invoices:
            invoice_lines_data = []
            for line in invoice.invoice_line_ids:
                line_data = {
                    'product': line.product_id.name,
                    'name': line.name,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                    'subtotal': line.quantity * line.price_unit,
                }
                invoice_lines_data.append(line_data)
            invoice_data = {
                'name': invoice.name,
                'partner': invoice.partner_id.name,
                'invoice_date': invoice.invoice_date,
                'lines': invoice_lines_data,
            }
            invoices_data.append(invoice_data)
        response = {'status': 200, 'response': invoices_data, 'message': 'Success'}
        return response

    @http.route('/create/invoice', type='json', auth='user')
    def create_invoice(self):
        try:
            # Directly parsing JSON data from the request body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            params = data.get('params', {})
            invoice = params.get('invoice_line_ids', [])
            # Your logic here...
            part = params.get('student_id')

            # Search for records based on the domain
            partner = request.env['res.partner'].sudo().search([('student_id', '=', part)], limit=1)
            invoice_data = {
                'partner_id': partner.id,
                'invoice_date': params.get('invoice_date'),
                'move_type': 'out_invoice',
            }
            invoice_lines = [
                (0, 0, {
                    'product_id': int(line['product_id']),
                    'quantity': (line['quantity']),
                    'price_unit': float(line['price_unit']),
                }) for line in invoice  # Assuming invoice_lines_data is your list of dictionaries
            ]

            invoice_data['invoice_line_ids'] = invoice_lines

            new_invoice = request.env['account.move'].sudo().create(invoice_data)
            # new_invoice.action_post()
            return {
                'status': 200,
                'message': 'Invoice created successfully',
                'invoice_id': new_invoice.id
            }
        except Exception as e:
            _logger.error(f"Failed to create invoice: {e}")
            raise UserError(f"Failed to create invoice: {e}")

    @http.route('/update/invoice', type='json', auth='user')
    def update_invoice(self):
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            params = data.get('params', {})
            invoice_id = params.get('id')
            invoice_lines_data = params.get('invoice_line_ids', [])  # Renamed for clarity

            if not invoice_id:
                return {'status': 400, 'message': 'No invoice ID provided', 'invoice_id': False}

            # Fetch the invoice using the provided ID
            invoice_obj = request.env['account.move'].sudo().search([('id', '=', int(invoice_id))], limit=1)

            if not invoice_obj.exists():
                return {'status': 404, 'message': 'Invoice not found', 'invoice_id': False}

            # Prepare invoice data and lines from the parsed JSON
            invoice_data = {
                'partner_id': int(params.get('partner_id')),
                'invoice_date': params.get('invoice_date'),
                'payment_reference': params.get('payment_reference')
            }
            invoice_lines = [(0, 0, {
                'product_id': int(line['product_id']),
                'quantity': float(line['quantity']),  # Ensure this is float if decimal quantities are allowed
                'price_unit': float(line['price_unit']),
            }) for line in invoice_lines_data]  # Correctly processing lines data

            invoice_data['invoice_line_ids'] = [(5, 0, 0)] + invoice_lines  # Clear existing lines and add new ones

            invoice_obj.write(invoice_data)
            return {
                'status': 200,
                'message': 'Invoice updated successfully',
                'id': invoice_obj.id  # Correctly referring to the invoice object
            }
        except ValueError as e:
            _logger.error(f"JSON parsing error: {e}")
            return {'status': 500, 'message': 'Invalid JSON data.', 'invoice_id': False}
        except Exception as e:
            _logger.error(f"Unexpected error: {type(e).__name__} - {e}")
            return {'status': 500, 'message': f"An unexpected error occurred: {type(e).__name__} - {e}",
                    'invoice_id': False}

    @http.route('/delete/invoice', type='json', auth='user')
    def delete_invoice(self, **kwargs):
        invoice_id = kwargs.get('invoice_id')
        invoice = request.env['account.move'].sudo().browse(invoice_id)

        try:
            invoice.unlink()
            return {'status': 200, 'message': 'Invoice deleted successfully'}
        except Exception as e:
            raise UserError(f"Failed to delete invoice: {e}")

    #     read payments api

    @http.route('/read/payments', type='json', auth='user')
    def read_payments(self, limit=10, offset=0, **kwargs):
        try:
            payment_fields = ['date', 'name', 'journal_id', 'payment_method_line_id', 'partner_id', 'amount', 'state']
            payments_data = request.env['account.payment'].sudo().search_read([],
                                                                              fields=payment_fields,
                                                                              limit=limit,
                                                                              offset=offset,
                                                                              order='date desc')
            refined_payments = []
            for payment in payments_data:
                # Extracting the name from the tuple (e.g., (id, name))
                journal_name = payment['journal_id'][1] if payment['journal_id'] else ''
                payment_method_name = payment['payment_method_line_id'][1] if payment['payment_method_line_id'] else ''
                customer_name = payment['partner_id'][1] if payment['partner_id'] else ''

                refined_payments.append({
                    'date': payment['date'],
                    'number': payment['name'],
                    'journal': journal_name,
                    'payment_method': payment_method_name,
                    'customer': customer_name,
                    'amount': payment['amount'],
                    'status': payment['state'],
                })
            if not refined_payments:
                return {'status': 204, 'response': [], 'message': 'No data found'}
            return {'status': 200, 'response': refined_payments, 'message': 'Success'}
        except Exception as e:
            return {'status': 500, 'message': 'Error retrieving payments: {}'.format(str(e))}

    # updated api payment
    @http.route('/update/payment', type='json', auth='user')
    def update_payment_record(self, **kwargs):
        record_id = kwargs.get('id')
        if record_id:
            payment_record = request.env['account.payment'].sudo().search(
                [('id', '=', int(record_id))])

            if payment_record:
                update_data = {key: value for key, value in kwargs.items() if key != 'id'}
                payment_record.sudo().write(update_data)

            return {'status': 200, 'response': "Record Updated", 'message': 'Success'}
        return {'status': 400, 'response': "Invalid ID",
                'message': 'Failed to update record due to missing or invalid ID'}

    # delete api payment

    @http.route('/delete/payment', type='json', auth='user')
    def delete_payment_record(self, **kwargs):
        record_id = kwargs.get('id')
        if record_id:
            # Search for the payment record by ID
            payment_record = request.env['account.payment'].sudo().search([('id', '=', int(record_id))])

            # Check if any record was found
            if payment_record.exists():
                # Delete the found record(s)
                payment_record.sudo().unlink()
                return {'status': 200, 'response': "Record deleted", 'message': 'Success'}
            else:
                return {'status': 404, 'response': "Record not found",
                        'message': 'No record found with the provided ID'}

        # If ID is not provided or invalid
        return {'status': 400, 'response': "Invalid ID",
                'message': 'Failed to delete record due to missing or invalid ID'}

    # create payment
    @http.route('/create/payment', type='json', auth='user')
    def create_payment(self, **kwargs):
        date = kwargs.get('date')
        name = kwargs.get('name')
        company_id = kwargs.get('company_id')
        partner_id = kwargs.get('partner_id')
        amount_signed = kwargs.get('amount_signed')
        currency_id = kwargs.get('currency_id')
        activity_ids = kwargs.get('activity_ids',[])
        state = kwargs.get('state', 'pending')  # Default state as 'pending' if not specified


        try:
            # Create a new payment record
            new_payment = http.request.env['account.payment'].sudo().create({
                'date': date,
                'name': name,
                'company_id': company_id,
                'partner_id': partner_id,
                'amount_signed': amount_signed,
                'currency_id': currency_id,
                'state' : state,
            })

            # Return a JSON response with success status and the ID of the newly created payment record
            return {'success': True, 'message': 'Record created successfully', 'payment_id': new_payment.id}
        except exceptions.UserError as e:
            # Catching and returning user errors such as validation failures
            return {'success': False, 'message': str(e)}
        except Exception as e:
            # General exception catch if something unexpected occurs
            return {'success': False, 'message': 'An unexpected error occurred: {}'.format(str(e))}







