# -*- coding: utf-8 -*-
from openerp import models, fields, api



class Batch(models.Model):
    _name = 'jm.batch'
    _order = 'name desc'
    name = fields.Char(u'批次')

class Level(models.Model):
    _name = 'jm.level'
    name = fields.Char(string=u"所选层次", required=True)



class Sc(models.Model):
    _name = 'jm.sc'
    _order = 'name'
    name = fields.Char(string=u"学习中心", required=True)

class School(models.Model):
    _name = "jm.school"
    _order = 'name'
    name = fields.Char(string=u"学校名称", required=True)
    value = fields.Char(string=u'值', required=True)

class Major(models.Model):
    _name = 'jm.major'
    _order = 'name'
    name = fields.Char(string=u"学习专业", required=True)

class Fee_project(models.Model):
    _name = 'jm.fee.project'
    _order = 'name'
    name = fields.Char(string=u"收费项目", required=True)
    value = fields.Char(string=u"Value", required=True)
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100