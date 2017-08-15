#-*- coding: utf-8 -*-
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re

class Province(models.Model):
	_name = 'all.province'

	name = fields.Char(u'省')


class City(models.Model):
	_name = 'all.city'

	name = fields.Char(u'市')
	belongs = fields.Char(u'所属省')


class County(models.Model):
	_name = 'all.county'

	name = fields.Char(u'县/区')
	belongs = fields.Char(u'所属市')