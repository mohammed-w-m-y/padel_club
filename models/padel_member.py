from odoo import models, fields

class PadelMember(models.Model):
    _name = 'padel.member'
    _description = 'Padel Member'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True, ondelete='cascade')
    membership_start = fields.Date(string='Membership Start Date', default=fields.Date.context_today)
    level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], string='Skill Level', default='beginner', required=True)