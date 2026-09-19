from odoo import fields, models


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

