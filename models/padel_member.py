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
    booking_ids = fields.One2many(
        comodel_name='padel.booking',
        inverse_name='member_id',
        string='Bookings',
    )
    booking_count = fields.Integer(
        string='Booking Count',
        compute='_compute_booking_count',
    )

    @api.depends('partner_id', 'level')
    def _compute_display_name(self):
        for record in self:
            if record.partner_id:
                record.display_name = f"{record.partner_id.name} ({record.level.capitalize()})"
            else:
                record.display_name = "New Member"

    @api.depends('booking_ids')
    def _compute_booking_count(self):
        for member in self:
            member.booking_count = len(member.booking_ids)

    def action_view_bookings(self):
        self.ensure_one()
        return {
            'name': f'Bookings for {self.partner_id.name if self.partner_id else "Member"}',
            'type': 'ir.actions.act_window',
            'res_model': 'padel.booking',
            'view_mode': 'list,form,calendar,kanban',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }