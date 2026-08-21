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