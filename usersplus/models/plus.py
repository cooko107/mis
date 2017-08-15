#-*- coding: utf-8 -*-
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re
class Student_Plus(models.Model):
    _inherit = 'jm.student'

    qq = fields.Char(u'QQ')
