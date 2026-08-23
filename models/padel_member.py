from odoo import fields, models


class PadelMember(models.Model):
    _name = 'padel.member'
    _description = 'Padel Club Member'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner / Contact',
        required=True,
        ondelete='cascade',
    )
    membership_start = fields.Date(
        string='Membership Start Date',
        default=fields.Date.context_today,
        required=True,
    )
    level = fields.Selection(
        selection=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        string='Skill Level',
        default='beginner',
        required=True,
    )

    def name_get(self):
        """Custom display name showing member level with partner name."""
        result = []
        for record in self:
            name = f"{record.partner_id.name} ({record.level.capitalize()})" if record.partner_id else "New Member"
            result.append((record.id, name))
        return result
