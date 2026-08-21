from odoo import models, fields, api
from datetime import timedelta


class PadelRecurringBookingWizard(models.TransientModel):
    _name = 'padel.recurring.booking.wizard'
    _description = 'Create Recurring Bookings'

    member_id = fields.Many2one('padel.member', string='Member', required=True)
    court_id = fields.Many2one('padel.court', string='Court', required=True)
    start_datetime = fields.Datetime(string='First Start Time', required=True)
    duration_hours = fields.Float(string='Duration (Hours)', default=1.0, required=True)
    number_of_weeks = fields.Integer(string='Number of Weeks', default=4, required=True)

    def action_generate_bookings(self):
        booking_ids = []
        for i in range(self.number_of_weeks):
            start = self.start_datetime + timedelta(weeks=i)
            end = start + timedelta(hours=self.duration_hours)

            # Check overlap before creating
            overlap = self.env['padel.booking'].search([
                ('court_id', '=', self.court_id.id),
                ('state', '!=', 'cancelled'),
                ('start_datetime', '<', end),
                ('end_datetime', '>', start),
            ])
            if not overlap:
                booking = self.env['padel.booking'].create({
                    'member_id': self.member_id.id,
                    'court_id': self.court_id.id,
                    'start_datetime': start,
                    'end_datetime': end,
                    'state': 'draft',
                })
                booking_ids.append(booking.id)

        return {
            'name': 'Created Bookings',
            'type': 'ir.actions.act_window',
            'res_model': 'padel.booking',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', booking_ids)],
        }