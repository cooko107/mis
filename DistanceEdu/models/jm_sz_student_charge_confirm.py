#-*- coding: utf-8 -*-
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re
#
# class SZ_student_charge_confirm(models.Model):
#     _name = 'sz.student.charge.confirm'
#
#     WORKFLOW_STATE_SELECTION = [
#         ('init', '收费登记'),
#         ('confirm', '待审批'),
#         ('complete', '完成'),
#     ]
#     state = fields.Selection(WORKFLOW_STATE_SELECTION, default='init', string="状态", readonly=True)
#
#     student_idcard = fields.Many2one('jm.student.order', u'身份证')
#     name = fields.Char(string=u'姓名', compute='_get_info',store='True')
#
#     study_center = fields.Char(string=u'报考中心', compute='_get_info',store='True')
#     batch = fields.Char(string=u'报考批次', compute='_get_info',store='True')
#     level = fields.Char(string=u'报考层次', compute='_get_info',store='True')
#     major = fields.Char(string=u'报考专业', compute='_get_info',store='True')
#
#     bm_fee = fields.Float(u'报名考试费', digits=(7, 0))
#     tuition = fields.Float(u'第一年学费', digits=(7, 0))
#     jc_fee = fields.Float(u'第一年教材费', digits=(7, 0))
#     ptfw_fee = fields.Float(u'第一年平台服务费', digits=(7, 0))
#     tuition2 = fields.Float(u'第二年学费', digits=(7, 0))
#     jc_fee2 = fields.Float(u'第二年教材费', digits=(7, 0))
#     ptfw_fee2 = fields.Float(u'第二年平台服务费', digits=(7, 0))
#     lwzd_fee = fields.Float(u'毕业论文指导费', digits=(7, 0))
#     dzsx_fee = fields.Float(u'电子摄像费', digits=(7, 0))
#     qcfd_fee = fields.Float(u'全程辅导费（课程）', digits=(7, 0))
#     qcfd_fee2 = fields.Float(u'全程辅导费（论文）', digits=(7, 0))
#     lwcx_fee = fields.Float(u'论文重修费', digits=(7, 0))
#
#     remarks = fields.Text(u'备注')
#
#     _sql_constraints = [('code_check', "UNIQUE(student_idcard)", u'该学生已登记')]
#
#     @api.depends('student_idcard')
#     @api.multi
#     def _get_info(self):
#         # print self.student_idcard
#         if (self.student_idcard):
#             env = self.student_idcard.school_table
#             env = env.replace('_', '.')
#             self.name = self.env[env].browse(self.student_idcard.school_id)[0].name_show
#             self.batch = self.env[env].browse(self.student_idcard.school_id)[0].batch.name
#             self.level = self.env[env].browse(self.student_idcard.school_id)[0].level.name
#             self.study_center = self.env[env].browse(self.student_idcard.school_id)[0].study_center.name
#             self.major = self.env[env].browse(self.student_idcard.school_id)[0].major.name
#
#     #workflow
#     @api.one
#     def to_confirm(self):
#         self.state = 'confirm'
#
#     @api.one
#     def to_complete(self):
#         self.state = 'complete'
#         env = self.student_idcard.school_table
#         env = env.replace('_', '.')
#         stu = self.env[env].browse(self.student_idcard.school_id)[0]
#         remarks_fun = lambda s1,s2:s1+s2 if s1 and s2 else s1 if not s2 else s2 if not s1 else False
#         values = {'bm_fee':self.bm_fee,
#                   'tuition':self.tuition,
#                   'jc_fee':self.jc_fee,
#                   'ptfw_fee':self.ptfw_fee,
#                   'tuition2':self.tuition2,
#                   'jc_fee2':self.jc_fee2,
#                   'ptfw_fee2':self.ptfw_fee2,
#                   'lwzd_fee':self.lwzd_fee,
#                   'dzsx_fee':self.dzsx_fee,
#                   'qcfd_fee':self.qcfd_fee,
#                   'qcfd_fee2':self.qcfd_fee2,
#                   'lwcx_fee':0,
#                   'state':u'已确认',
#                   'remarks':remarks_fun(stu.remarks, self.remarks)}
#         stu.write(values)
#         values.pop('state')
#         values.pop('remarks')
#         charge_details = self.env['jm.charge'].search([('order_con', '=', self.student_idcard.id)])
#         for charge_detail in charge_details:
#             charge_detail.fee = values[charge_detail.project]
#
#     @api.one
#     def back_init(self):
#         self.state = 'init'










