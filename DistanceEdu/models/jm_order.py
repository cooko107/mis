#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re

class Fee(models.Model):
    _name = 'jm.charge'
    student_con = fields.Integer('connect_student')
    order_con = fields.Integer('connect_order')
    add_con = fields.Char('connect_fee')
    project = fields.Selection(selection='get_selection', string = u"收费项目")
    fee_charged = fields.Float(u'实收金额', digits=(7, 0))
    fee = fields.Float(string=u'高校标准',default=0.0,digits=(7, 0))
    fee_charge = fields.Float(string=u'应收金额',digits=(7, 0))
    up_school_fee = fields.Float(string=u'上交高校金额',default=0.0,digits=(7, 0))
    deletable = fields.Boolean(default=False)
    school_id = fields.Integer()
    school_table = fields.Char(u'学校表')

    @api.model
    def get_selection(self):
        selections = self.env['jm.fee.project'].search([])
        return [(selection.value, selection.name) for selection in selections]

    '''@api.constrains(fee,fee_charged)
    def _set_readonly(self):
        if(self.fee_charged >= self.fee):
            self.readonly = True'''

    '''@api.onchange('fee_charged')
    def _set_deletable(self):
        for each in self:
            if (each.fee_charged >= each.fee):
                each.deletable = False
            else:
                each.deletable = True'''

class Student_Order(models.Model):
    _name = 'jm.student.order'
    _rec_name = 'student_id'

    batch = fields.Char(u'批次')
    student_id = fields.Char(u'身份证')
    student_table = fields.Char(u'学生表')
    student_name = fields.Char(u'学生姓名')
    school_id = fields.Integer(u'学校id')
    school_table = fields.Char(u'学校表')

    fee_line = fields.One2many('jm.charge','order_con')

    @api.multi
    def name_get(self):
        result = []
        for r in self:
            #name = self.env['jm.student'].search([('idcard','=',r.student_id)])[0].sname
            #print st_id
            #name = self.env['jm.student'].browse(st_id[0])[0].sname
            result.append((r.id, '%s(%s)' %(r.student_id, r.student_name)))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=80):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('student_id', operator, name), ('student_name', operator, name)]
        pos = self.search(domain + args, limit=limit)
        return pos.name_get()