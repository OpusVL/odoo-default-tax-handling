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

from openerp.osv import osv
from openerp import exceptions


class SaleOrderLine(osv.osv):
    _inherit = "sale.order.line"

    def default_get(self, cr, uid, fields, context=None):
        res = super(SaleOrderLine, self).default_get(cr, uid, fields, context=None)
        pt_tax_obj = self.pool.get('product.template.tax')
        res_user_obj = self.pool.get('res.users')
        users_company_id = res_user_obj.browse(cr, uid, uid, context=context).company_id
        dot = pt_tax_obj.search(cr, uid, [('active_on_order_line', '=', True)], context=context)
        dot_rec = pt_tax_obj.browse(cr, uid, dot, context=context)
        if len(dot) > 1:
            raise exceptions.Warning('More than one default tax set up to be active on order line creation')
        elif len(dot) < 1:
            pass
        elif len(dot) == 1:
            for i in dot_rec.default_product_taxes:
                if (i.type_tax_use == 'sale') and (users_company_id == i.company_id):
                    res['tax_id'] = [(6, False, [i.id])]
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
