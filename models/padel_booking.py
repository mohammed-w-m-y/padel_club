<<<<<<< HEAD
from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError
=======
from odoo import api, fields, models
>>>>>>> main


class PadelBooking(models.Model):
    _name = 'padel.booking'
    _description = 'Padel Court Booking'
<<<<<<< HEAD
    _order = 'start_datetime desc'

    def _default_start_datetime(self):
        """Compute default start datetime as the next full hour."""
        now = fields.Datetime.now()
        return now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
=======
>>>>>>> main

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
<<<<<<< HEAD
        default=_default_start_datetime,
=======
>>>>>>> main
    )
    end_datetime = fields.Datetime(
        string='End Datetime',
        required=True,
<<<<<<< HEAD
        default=lambda self: self._default_start_datetime() + timedelta(hours=1),
    )
    duration_hours = fields.Float(
        string='Duration (Hours)',
        compute='_compute_booking_details',
=======
    )
    duration_hours = fields.Float(
        string='Duration (Hours)',
        compute='_compute_duration_hours',
>>>>>>> main
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
<<<<<<< HEAD
        compute='_compute_booking_details',
=======
        compute='_compute_price',
>>>>>>> main
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

<<<<<<< HEAD
    # ---------------------------------------------------------
    # SQL Constraints
    # ---------------------------------------------------------
    _sql_constraints = [
        (
            'check_dates',
            'CHECK(end_datetime > start_datetime)',
            'End datetime must be strictly after start datetime!'
        )
    ]

    # ---------------------------------------------------------
    # Computed Fields
    # ---------------------------------------------------------
    @api.depends('start_datetime', 'end_datetime', 'court_id.hourly_rate')
    def _compute_booking_details(self):
        """Compute duration in hours and total price based on court hourly rate."""
        for booking in self:
            if booking.start_datetime and booking.end_datetime and booking.end_datetime > booking.start_datetime:
                delta = booking.end_datetime - booking.start_datetime
                booking.duration_hours = delta.total_seconds() / 3600.0
                booking.price = booking.duration_hours * (booking.court_id.hourly_rate or 0.0)
            else:
                booking.duration_hours = 0.0
                booking.price = 0.0

    # ---------------------------------------------------------
    # Python Constraints (Overlap & Date Validation)
    # ---------------------------------------------------------
    @api.constrains('start_datetime', 'end_datetime')
    def _check_valid_dates(self):
        """Validate that end_datetime is strictly after start_datetime."""
        for booking in self:
            if booking.start_datetime and booking.end_datetime and booking.end_datetime <= booking.start_datetime:
                raise ValidationError("End Datetime must be strictly after Start Datetime!")

    @api.constrains('court_id', 'start_datetime', 'end_datetime', 'state')
    def _check_booking_overlap(self):
        """Prevent double-booking for the same court during overlapping time slots."""
        for booking in self:
            if booking.state == 'cancelled':
                continue

            domain = [
                ('id', '!=', booking.id),
                ('court_id', '=', booking.court_id.id),
                ('state', '!=', 'cancelled'),
                ('start_datetime', '<', booking.end_datetime),
                ('end_datetime', '>', booking.start_datetime),
            ]
            overlapping_booking = self.search(domain, limit=1)
            if overlapping_booking:
                raise ValidationError(
                    f"The court '{booking.court_id.name}' is already booked during this time slot!"
                )

    # ---------------------------------------------------------
    # Onchange Handlers
    # ---------------------------------------------------------
    @api.onchange('court_id')
    def _onchange_court_id(self):
        """Show warning if an archived court is selected."""
        if self.court_id and not self.court_id.active:
            return {
                'warning': {
                    'title': "Archived Court Selected",
                    'message': f"Warning: The court '{self.court_id.name}' is archived!",
                }
            }

    # ---------------------------------------------------------
    # Action Methods
    # ---------------------------------------------------------
    def action_confirm(self):
        """Confirm the booking."""
        for booking in self:
            if booking.state == 'cancelled':
                raise ValidationError("You cannot confirm a cancelled booking. Reset it to draft first.")
            booking.state = 'confirmed'

    def action_done(self):
        """Mark booking as completed."""
        for booking in self:
            if booking.state != 'confirmed':
                raise ValidationError("Only confirmed bookings can be marked as Done.")
            booking.state = 'done'

    def action_cancel(self):
        """Cancel the booking."""
        for booking in self:
            if booking.state == 'done':
                raise ValidationError("You cannot cancel a completed (Done) booking.")
            booking.state = 'cancelled'

    def action_reset_to_draft(self):
        """Reset cancelled booking back to draft."""
        for booking in self:
            booking.state = 'draft'
=======
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
>>>>>>> main
