#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re
from passlib.context import CryptContext
class Jm_Student(models.Model):
    _name = 'jm.student'
    _rec_name = 'idcard'
    _order = 'idcard'

    name = fields.Char()
    sname = fields.Char(u'姓名')
    card_type = fields.Char(u'证件类型', default='身份证')
    idcard = fields.Char(u'证件号码')
    sex = fields.Selection([[1,'男'],[2,'女']],string=u'性别',default=1)
    nation = fields.Char(u'民族', default="汉")
    native_place = fields.Char(u'籍贯', default='浙江省')
    birth = fields.Date(u'出生日期')
    phone = fields.Char(u'手机')
    tele = fields.Char(u'固定电话')
    qq = fields.Char(u'QQ')
    wchat = fields.Char(u'微信')
    political = fields.Char(u'政治面貌')
    work_time = fields.Date(u'参加工作时间')
    job_type = fields.Char(u'职业类别')
    job = fields.Char(u'职务或工种')
    work_unit = fields.Char(u'工作单位')
    address = fields.Char(u'住址')
    email = fields.Char(u'邮箱')
    letter_add = fields.Char(u'通知书邮寄地址')
    zip = fields.Char(u'邮编')
    study_level = fields.Char(u'文化程度')

# class multi_school(models.Model):
#     _name = 'jm.multi.school.student'
#
#     name = fields.Char(u'姓名',readonly=True)
#     idcard = fields.Char(u'身份证',readonly=True)
#     batch = fields.Char(u'批次',readonly=True)
#     the_one = fields.Selection([[1,u'天大'],[2,u'郑大'],[3,u'石大'],[4,u'南开']],u'确认高校')
#     tju = fields.Boolean(u'天大',readonly=True)
#     syu = fields.Boolean(u'石大',readonly=True)
#     nku = fields.Boolean(u'南开',readonly=True)
#     zzu = fields.Boolean(u'郑大',readonly=True)
#
#     @api.multi
#     def set_one(self):
#         if(self.the_one == 1):
#             if(self.syu == True):
#                 self.env.cr.execute("select id from jm_syu_plan where name='%s'" %(self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" %(self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_syu_student where batch=%s and student=%s" %(batch_id,stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_syu_student')"%(
#                        self.batch,self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_syu_student'"%(
#                                      self.batch,self.idcard))
#             if (self.zzu == True):
#                 self.env.cr.execute("select id from jm_zzu_plan where name='%s'" % (self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" % (self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_zzu_student where batch=%s and student=%s" % (batch_id, stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_zzu_student')" % (
#                        self.batch, self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_zzu_student'" % (
#                                      self.batch, self.idcard))
#             if (self.nku == True):
#                 self.env.cr.execute("select id from jm_nku_plan where name='%s'" % (self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" % (self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_nku_student where batch=%s and student=%s" % (batch_id, stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_nku_student')" % (
#                        self.batch, self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_nku_student'" % (
#                                      self.batch, self.idcard))
#         if (self.the_one == 2):
#             if (self.tju == True):
#                 self.env.cr.execute("select id from jm_tju_plan where name='%s'" % (self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" % (self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_tju_student where batch=%s and student=%s" % (batch_id, stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_tju_student')" % (
#                        self.batch, self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_tju_student'" % (
#                                      self.batch, self.idcard))
#             if (self.zzu == True):
#                 self.env.cr.execute("select id from jm_zzu_plan where name='%s'" % (self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" % (self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_zzu_student where batch=%s and student=%s" % (batch_id, stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_zzu_student')" % (
#                     self.batch, self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_zzu_student'" % (
#                     self.batch, self.idcard))
#             if (self.nku == True):
#                 self.env.cr.execute("select id from jm_nku_plan where name='%s'" % (self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" % (self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_nku_student where batch=%s and student=%s" % (batch_id, stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_nku_student')" % (
#                     self.batch, self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_nku_student'" % (
#                     self.batch, self.idcard))
#         if (self.the_one == 3):
#             if (self.syu == True):
#                 self.env.cr.execute("select id from jm_syu_plan where name='%s'" % (self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" % (self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_syu_student where batch=%s and student=%s" % (batch_id, stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_syu_student')" % (
#                     self.batch, self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_syu_student'" % (
#                     self.batch, self.idcard))
#             if (self.tju == True):
#                 self.env.cr.execute("select id from jm_tju_plan where name='%s'" % (self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" % (self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_tju_student where batch=%s and student=%s" % (batch_id, stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_tju_student')" % (
#                     self.batch, self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_tju_student'" % (
#                     self.batch, self.idcard))
#             if (self.nku == True):
#                 self.env.cr.execute("select id from jm_nku_plan where name='%s'" % (self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" % (self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_nku_student where batch=%s and student=%s" % (batch_id, stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_nku_student')" % (
#                     self.batch, self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_nku_student'" % (
#                     self.batch, self.idcard))
#         if (self.the_one == 4):
#             if (self.syu == True):
#                 self.env.cr.execute("select id from jm_syu_plan where name='%s'" % (self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" % (self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_syu_student where batch=%s and student=%s" % (batch_id, stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_syu_student')" % (
#                     self.batch, self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_syu_student'" % (
#                     self.batch, self.idcard))
#             if (self.zzu == True):
#                 self.env.cr.execute("select id from jm_zzu_plan where name='%s'" % (self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" % (self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_zzu_student where batch=%s and student=%s" % (batch_id, stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_zzu_student')" % (
#                     self.batch, self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_zzu_student'" % (
#                     self.batch, self.idcard))
#             if (self.tju == True):
#                 self.env.cr.execute("select id from jm_tju_plan where name='%s'" % (self.batch))
#                 batch_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("select id from jm_student where idcard='%s'" % (self.idcard))
#                 stu_id = self.env.cr.fetchall()[0][0]
#                 self.env.cr.execute("delete from jm_tju_student where batch=%s and student=%s" % (batch_id, stu_id))
#                 sql = "delete from jm_charge where order_con in (select id from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_tju_student')" % (
#                     self.batch, self.idcard)
#                 self.env.cr.execute(sql)
#                 self.env.cr.execute("delete from jm_student_order where batch='%s' and student_id='%s' and school_table='jm_tju_student'" % (
#                     self.batch, self.idcard))
#
#         self.env.cr.execute("delete from jm_multi_school_student where id=%s" %(self.id))
#         return {
#             'type': 'ir.actions.client',
#             'tag': 'operation_success',
#             'target': 'self',
#             'action': {
#                 'action': 'doNotify',
#                 'message': {
#                     'title': u'提示',
#                     'message': u'成功'
#                 }
#             }
#         }




