from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class PadelBooking(models.Model):
    _name = 'padel.booking'
    _description = 'Padel Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    court_id = fields.Many2one('padel.court', string='Court', required=True, tracking=True)
    member_id = fields.Many2one('padel.member', string='Member', required=True, tracking=True)
    start_datetime = fields.Datetime(string='Start Datetime', required=True, tracking=True)
    end_datetime = fields.Datetime(string='End Datetime', required=True, tracking=True)

    duration_hours = fields.Float(string='Duration (Hours)', compute='_compute_duration', store=True)

    currency_id = fields.Many2one('res.currency', related='court_id.currency_id', store=True)
    price = fields.Monetary(string='Total Price', compute='_compute_price', store=True, currency_field='currency_id')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft', required=True, tracking=True)

    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)

    @api.depends('start_datetime', 'end_datetime')
    def _compute_duration(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                diff = record.end_datetime - record.start_datetime
                record.duration_hours = diff.total_seconds() / 3600.0
            else:
                record.duration_hours = 0.0

    @api.depends('duration_hours', 'court_id.hourly_rate')
    def _compute_price(self):
        for record in self:
            if record.court_id and record.duration_hours:
                record.price = record.duration_hours * record.court_id.hourly_rate
            else:
                record.price = 0.0

    # SQL Constraint
    _sql_constraints = [
        ('check_dates', 'CHECK(end_datetime > start_datetime)', 'The end time must be after the start time!')
    ]

    # Python Overlap Constraint
    @api.constrains('court_id', 'start_datetime', 'end_datetime', 'state')
    def _check_booking_overlap(self):
        for record in self:
            if record.state == 'cancelled':
                continue

            overlapping = self.search([
                ('id', '!=', record.id),
                ('court_id', '=', record.court_id.id),
                ('state', '!=', 'cancelled'),
                ('start_datetime', '<', record.end_datetime),
                ('end_datetime', '>', record.start_datetime),
            ])
            if overlapping:
                raise ValidationError("There is already a booking for this court in the selected time frame!")

    # Onchange Warning for Archived Court
    @api.onchange('court_id')
    def _onchange_court_id(self):
        if self.court_id and not self.court_id.active:
            return {
                'warning': {
                    'title': "Archived Court Selected",
                    'message': "Warning: The selected court is archived and not active!",
                }
            }

    # State Machine Methods
    def action_confirm(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError("Only draft bookings can be confirmed.")
            rec.state = 'confirmed'

    def action_done(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise ValidationError("Only confirmed bookings can be marked as done.")
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError("Completed bookings cannot be cancelled.")
            rec.state = 'cancelled'

    def action_reset_draft(self):
        for rec in self:
            if rec.state != 'cancelled':
                raise ValidationError("Only cancelled bookings can be reset to draft.")
            rec.state = 'draft'