from odoo import http
from odoo.http import request
import base64


class EmployeeLeaveWeb(http.Controller):
    @http.route('/leave/apply', type='http', auth='public', website=True)
    def leave_form(self, **kwargs):
        return request.render('employee_leave_web.leave_form')

    @http.route('/leave/submit', type='http', auth='public', methods=['POST'], website=True)
    def submit_leave(self, **kwargs):
        employee_id = kwargs.get('employee_id')
        leave_type_id = kwargs.get('leave_type_id')
        date_from = kwargs.get('date_from')
        date_to = kwargs.get('date_to')
        reason = kwargs.get('reason')
        attachment_file = request.httprequest.files.get('attachment')

        
        employee = request.env['hr.employee'].sudo().search([('identification_id', '=', employee_id)], limit=1)
        if not employee:
            return request.render('employee_leave_web.leave_form', {
                'error': 'Invalid Employee ID',
            })

        
        leave_vals = {
            'name': reason or 'Leave Request',
            'employee_id': employee.id,
            'holiday_status_id': int(leave_type_id),
            'request_date_from': date_from,
            'request_date_to': date_to,
        }
        leave = request.env['hr.leave'].sudo().create(leave_vals)

        # Handle the file attachment
        if attachment_file:
            file_content = attachment_file.read()  # Read the binary content of the file
            filename = attachment_file.filename
            attachment_vals = {
                'name': filename,
                'type': 'binary',
                'datas': base64.b64encode(file_content),  # Convert binary data to Base64
                'res_model': 'hr.leave',
                'res_id': leave.id,  # Link attachment to the leave request
            }
            attachment = request.env['ir.attachment'].sudo().create(attachment_vals)

            # Link the attachment to the leave request
            leave.sudo().write({
                'supported_attachment_ids': [(4, attachment.id)]
            })


        return request.render('employee_leave_web.leave_success')
