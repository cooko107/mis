#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re

class Syu_Plan(models.Model):
    _name = 'jm.syu.plan'
    _order = 'batch desc, level desc, study_center, major'

    name = fields.Char(u'名称')
    batch = fields.Char(u'批次')
    level = fields.Char(u'层次')
    school = fields.Char(u'学校')
    major = fields.Char(u'专业')
    study_center = fields.Char(u'学习中心')
    items = fields.One2many('jm.syu.plan.items', 'plan_con', u'收费列表')


    #费用
    bm_fee = fields.Float(u'报名考试费')
    tuition = fields.Float(u'第一年学费')
    jc_fee = fields.Float(u'第一年教材费')
    ptfw_fee = fields.Float(u'第一年平台服务费')
    tuition2 = fields.Float(u'第二年学费')
    jc_fee2 = fields.Float(u'第二年教材费')
    ptfw_fee2 = fields.Float(u'第二年平台服务费')
    lwzd_fee = fields.Float(u'毕业论文指导费')
    dzsx_fee = fields.Float(u'电子摄像费')
    qcfd_fee = fields.Float(u'全程辅导费（课程）')
    qcfd_fee2 = fields.Float(u'全程辅导费（论文）')
    lwcx_fee = fields.Float(u'论文重修费')
    show_name = fields.Char(u'专业')

    remarks = fields.Text(u'备注')

    #设置专业的显示名称
    @api.constrains('major')
    def get_name(self):
        if(self.major == '1'):
            self.env.cr.execute("UPDATE jm_syu_plan set show_name='%s' where name='%s' and batch='%s' and level='%s' and study_center='%s'"
                               %(self.name, self.name, self.batch, self.level, self.study_center))

    def delete(self, cr, uid, context):
        it = ['bm_fee', 'tuition', 'jc_fee', 'ptfw_fee', 'tuition2', 'jc_fee2', 'ptfw_fee2', 'lwzd_fee', 'dzsx_fee',
              'qcfd_fee', 'qcfd_fee2', 'lwcx_fee']

        for id in context.get('active_ids'):
            cr.execute("select bm_fee,tuition,jc_fee,ptfw_fee,tuition2,jc_fee2,ptfw_fee2,lwzd_fee,dzsx_fee"
                       ",qcfd_fee,qcfd_fee2,lwcx_fee from jm_syu_plan where id=%s" % id)
            items = cr.fetchall()

            i = 0
            for item in items[0]:
                cr.execute("select id from jm_fee_project where value='%s'" % it[i])
                pro = cr.fetchall()[0][0]
                cr.execute("insert into jm_syu_plan_items (item,money,plan_con) values(%s, %s, %s)" % (pro, item, id))
                i += 1

class Syu_Plan_items(models.Model):
    _name = 'jm.syu.plan.items'

    item = fields.Many2one('jm.fee.project', u'收费项目')
    money = fields.Float(u'收费金额', digits=(7, 0))
    plan_con = fields.Integer()