# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import models, api
_logger = logging.getLogger(__name__)


class PostObjectData(models.TransientModel):
    _name = 'post.object.data'
    _description = 'Post Object'

    @api.model
    def generate_account_taxes(self):
        """
        Generate eco participation account taxes
        """
        _logger.info(
            '======START GENERATE ACCOUNT TAXES========')
        chart_template = self.env.ref('l10n_fr.l10n_fr_pcg_chart_template')
        companies = self.env['res.company'].search([])
        for company in companies:
            chart_template.tax_template_ids._generate_tax(company)

        self.env['ir.config_parameter'].sudo().set_param(
            'generated_eco_participation_taxes', True)
        _logger.info(
            '======END GENERATE ACCOUNT TAXES========')
        return True

    @api.model
    def start(self):
        """
        Place all the functions need to run here
        """
        _logger.info('=====START post object=======')
        generated_eco_participation_taxes = self.env[
            'ir.config_parameter'].sudo().get_param(
            'generated_eco_participation_taxes'
        )
        if not generated_eco_participation_taxes:
            self.generate_account_taxes()
        _logger.info('======END post object========')
        return True


