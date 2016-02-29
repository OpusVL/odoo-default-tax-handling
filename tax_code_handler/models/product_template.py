# -*- coding: utf-8 -*-

##############################################################################
#
# tax_code_handler
# Copyright (C) 2016 OpusVL (<http://opusvl.com/>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, SUPERUSER_ID
from openerp import exceptions


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Have to override method instead of appending vals to super
    def create(self, cr, uid, vals, context=None):
        # Start Extension
        stax = []
        ptax = []
        pt_tax_obj = self.pool.get('product.template.tax')
        dpt = pt_tax_obj.search(cr, SUPERUSER_ID, [('active_on_product', '=', True)], context=context)
        dpt_rec = pt_tax_obj.browse(cr, SUPERUSER_ID, dpt, context=context)
        if len(dpt) > 1:
            raise exceptions.Warning('More than one default product tax set up to be active on product creation')
        elif len(dpt) < 1:
            pass
        elif len(dpt) == 1:
            for i in dpt_rec.default_product_taxes:
                if i.type_tax_use == 'sale':
                    stax.append(i.id)
                if i.type_tax_use == 'purchase':
                    ptax.append(i.id)
        if ptax:
            vals['supplier_taxes_id'] = [(6, False, ptax)]
        if stax:
            vals['taxes_id'] = [(6, False, stax)]
        # End Extension

        product_template_id = super(ProductTemplate, self).create(cr, uid, vals, context=context)
        if not context or "create_product_product" not in context:
            self.create_variant_ids(cr, uid, [product_template_id], context=context)
        self._set_standard_price(cr, uid, product_template_id, vals.get('standard_price', 0.0), context=context)
        related_vals = {}
        if vals.get('ean13'):
            related_vals['ean13'] = vals['ean13']
        if vals.get('default_code'):
            related_vals['default_code'] = vals['default_code']
        if related_vals:
            self.write(cr, uid, product_template_id, related_vals, context=context)
        return product_template_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
