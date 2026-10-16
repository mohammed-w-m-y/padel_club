
from odoo import fields, models


class IrRule(models.Model):
    _inherit = "ir.rule"

    def _eval_context(self):
        eval_context = super()._eval_context()
        eval_context["today"] = fields.Date.context_today(self)
        return eval_context
