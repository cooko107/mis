#-*- coding: utf-8 -*-
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re
class Users_Plus(models.Model):
    _inherit = 'res.users'

    department = fields.Char(u'部门')

    platform = fields.Many2many('jm.sc',string=u'学习中心')

    custom = fields.Many2many('jm.custom', string=u'渠道')

    areacode = fields.Char(u'打印区号')
