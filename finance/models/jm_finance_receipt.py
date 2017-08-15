#-*- coding:utf-8 -*-
from openerp import api, fields, models

#票据管理
class Finance_receipt(models.Model):
    _name = 'jm.finance.receipt'
    _rec_name = 'num'

    num = fields.Char(u'票据号')
    name = fields.Char(u'学生姓名')
    project = fields.Char(u'票据项目')
    money = fields.Char(u'金额')
    fake_code = fields.Char(u'防伪码')
    drawer = fields.Char(u'开票人')
    time = fields.Date(u'打印日期')
    finance_order = fields.Many2one('jm.student.charge')
    state = fields.Char(u'状态')


#打印
class Print_detail(models.TransientModel):
    _name = 'jm.student.charge.print.item'
    print_item = fields.Many2many('jm.student.charge.details',string=u'打印项目')
    project = fields.Char(u'打印项目')

    @api.multi
    def print_msg(self):
        return self.env['report'].with_context().get_action(self, 'finance.report_receipt')

    @api.onchange('print_item')
    def set_project(self):
        project = ''
        for item in self.print_item:
            project += self.env['jm.fee.project'].search([('value', '=', item.project)])[0].name + '-'
        self.project = project


class Pre_charge_print_detail(models.Model):
    _name = 'jm.student.pre.charge.print.item'
    print_item = fields.Many2many('jm.multi.charge.fee.add',string=u'打印项目')
    project = fields.Char(u'打印项目')

    @api.multi
    def print_msg(self):
        return self.env['report'].get_action(self, 'finance.pre_charge_report_receipt')

    @api.onchange('print_item')
    def set_project(self):
        project = ''
        for item in self.print_item:
            project += self.env['jm.fee.project'].search([('value', '=', item.project)])[0].name + '-'
        self.project = project



class Finance_receipt_deactivate(models.Model):
    _name = 'jm.finance.receipt.deactivate'
    _rec_name = 'num'

    WORKFLOW_STATE_SELECTION = [
        ('init', '开始'),
        ('confirm', '待审批'),
        ('complete', '完成'),
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION, default='init', string="状态", readonly=True)
    num = fields.Many2one('jm.finance.receipt',u'票据号',ondelete='cascade')
    name = fields.Char(related='num.name',string=u'学生姓名')
    project = fields.Char(related='num.project',string=u'票据项目')
    money = fields.Char(related='num.money',string=u'金额')
    fake_code = fields.Char(related='num.fake_code',string=u'防伪码')
    drawer = fields.Char(related='num.drawer',string=u'开票人')


    @api.multi
    def to_confirm(self):
        self.state = 'confirm'

    @api.multi
    def to_complete(self):
        self.state = 'complete'
        self.env['jm.finance.receipt'].browse(self.num.id)[0].state = u'已作废'

    @api.multi
    def back_init(self):
        self.state = 'init'

    @api.multi
    def deactivate(self):
        self.env['jm.finance.receipt'].browse(self.num.id)[0].state = u'已作废'
