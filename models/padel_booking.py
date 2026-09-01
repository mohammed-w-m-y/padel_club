from odoo import api, fields, models


class PadelBooking(models.Model):
    _name = 'padel.booking'
    _description = 'Padel Court Booking'

    court_id = fields.Many2one(
        comodel_name='padel.court',
        string='Court',
        required=True,
    )
    member_id = fields.Many2one(
        comodel_name='padel.member',
        string='Member',
        required=True,
    )
    start_datetime = fields.Datetime(
        string='Start Datetime',
        required=True,
    )
    end_datetime = fields.Datetime(
        string='End Datetime',
        required=True,
    )
    duration_hours = fields.Float(
        string='Duration (Hours)',
        compute='_compute_duration_hours',
        store=True,
    )
    currency_id = fields.Many2one(
        related='court_id.currency_id',
        string='Currency',
        store=True,
        readonly=True,
    )
    price = fields.Monetary(
        string='Total Price',
        compute='_compute_price',
        currency_field='currency_id',
        store=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
    )

    @api.depends('start_datetime', 'end_datetime')
    def _compute_duration_hours(self):
        for booking in self:
            if booking.start_datetime and booking.end_datetime:
                delta = booking.end_datetime - booking.start_datetime
                booking.duration_hours = delta.total_seconds() / 3600.0
            else:
                booking.duration_hours = 0.0

    @api.depends('duration_hours', 'court_id.hourly_rate')
    def _compute_price(self):
        for booking in self:
            if booking.court_id and booking.duration_hours:
                booking.price = booking.duration_hours * booking.court_id.hourly_rate
            else:
                booking.price = 0.0