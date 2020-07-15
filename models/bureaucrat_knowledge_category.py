from odoo import models


class BureaucratKnowledgeCategory(models.Model):
    _name = 'bureaucrat.knowledge.category'
    _inherit = [
        'bureaucrat.knowledge.category',
        'website.published.mixin',
        'website.seo.metadata',
    ]

    def _compute_website_url(self):
        res = super(BureaucratKnowledgeCategory, self)._compute_website_url()
        for category in self:
            category.website_url = '/knowledge/%s' % category.id
        return res

    def action_show_on_website(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.website_url,
            'target': 'self',
        }
