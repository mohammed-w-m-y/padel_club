from odoo import api, fields, models


class PadelCourt(models.Model):
    _name = 'padel.court'
    _description = 'Padel Court'

    name = fields.Char(string='Court Name', required=True)
    court_type = fields.Selection(
        selection=[
            ('indoor', 'Indoor'),
            ('outdoor', 'Outdoor'),
        ],
        string='Court Type',
        default='indoor',
        required=True,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    hourly_rate = fields.Monetary(
        string='Hourly Rate',
        currency_field='currency_id',
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Uncheck to archive the court without deleting it.',
    )
    booking_ids = fields.One2many(
        comodel_name='padel.booking',
        inverse_name='court_id',
        string='Bookings',
    )
    booking_count = fields.Integer(
        string='Booking Count',
        compute='_compute_booking_count',
    )

    @api.depends('booking_ids')
    def _compute_booking_count(self):
        for court in self:
            court.booking_count = len(court.booking_ids)

    def action_view_bookings(self):
        self.ensure_one()
        return {
            'name': f'Bookings for {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'padel.booking',
            'view_mode': 'list,form,calendar,kanban',
            'domain': [('court_id', '=', self.id)],
            'context': {'default_court_id': self.id},
        }