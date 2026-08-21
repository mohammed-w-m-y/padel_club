from odoo import models, fields


class PadelCourt(models.Model):
    _name = 'padel.court'
    _description = 'Padel Court'

    name = fields.Char(string='Court Name', required=True)
    court_type = fields.Selection([
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor')
    ], string='Court Type', required=True, default='indoor')

    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    hourly_rate = fields.Monetary(string='Hourly Rate', currency_field='currency_id', required=True)
    active = fields.Boolean(string='Active', default=True)