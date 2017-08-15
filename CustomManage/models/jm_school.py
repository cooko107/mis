#-*- coding: utf-8 -*-
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re
class Jm_School(models.Model):
    _name = 'jm.de.school'

    name = fields.Char(u"分校名称")