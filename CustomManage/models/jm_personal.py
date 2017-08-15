#-*- coding: utf-8 -*-
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re

class Jm_personal(models.Model):
	#表名和描述
    _name = 'jm.personal'

    name = fields.Char(u'名称')
    code = fields.Char(u'编码')
    besq = fields.Many2one('jm.custom',u'所属客户')
    remarks = fields.Text(u'备注')