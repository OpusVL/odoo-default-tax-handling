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

from openerp import models, fields, api

class ProductTemplateTax(models.Model):
    _name = "product.template.tax"

    name = fields.Char()
    active_on_product = fields.Boolean(help='Set the default taxes on product creation. Only one active default can be applied at one time')
    active_on_order_line = fields.Boolean(help='Set the default taxes on new sale order line creation. Only one active default can be applied at one time')
    default_product_taxes = fields.Many2many(comodel_name='account.tax', help='Select the taxes to be applied to products - both sale and purchase taxes can be put here')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
