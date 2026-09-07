from odoo import api, fields, models


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

    @api.depends('partner_id', 'level')
    def _compute_display_name(self):
        """Custom display name showing member level with partner name for Odoo 19."""
        for record in self:
            if record.partner_id:
                record.display_name = f"{record.partner_id.name} ({record.level.capitalize()})"
            else:
<<<<<<< HEAD
                record.display_name = "New Member"
=======
                record.display_name = "New Member"
>>>>>>> main
