# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo.tools.translate import _
from odoo.tools import email_split
from odoo.exceptions import UserError

from odoo import api, fields, models


_logger = logging.getLogger(__name__)


class CountryWizard(models.TransientModel):

    _name = 'country.wizard'
    _description = 'Choose Country'

    country_portal_id = fields.Many2one('student.country', string='Country')
    student_ids = fields.Many2many('student.profile', string='students')

    @api.model
    def default_get(self, fields):
        res = super(CountryWizard, self).default_get(fields)
        res['student_ids'] = self.env.context.get('active_ids', [])
        return res

    @api.multi
    def action_apply(self):
        cid = self.country_portal_id.id
        obj = self.env['student.profile'].browse(self.student_ids.ids)
        obj.write({'country_id': cid})
        return {'type': 'ir.actions.act_window_close'}
