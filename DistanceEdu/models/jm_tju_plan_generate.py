#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models

class Tju_Plan_Generate(models.Model):
    _name = 'jm.tju.plan.generate'

    batch = fields.Many2one('jm.batch',string=u'批次')
    level = fields.Many2one('jm.level',string=u'层次')
    sc = fields.Many2many('jm.sc',string=u'学习中心')
    major = fields.Many2many('jm.major',string=u'专业')

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

    items = fields.One2many('jm.tju.plan.generate.items', 'plan_con', u'收费')

    @api.multi
    def generate_plan(self):
        batch = self.batch.name
        level = self.level.name
        if not self.env['jm.tju.plan'].search([('name', '=', batch), ('batch', '=', '1')]):
            self.env['jm.tju.plan'].create({
                'name': batch,
                'batch': '1',
            })
        if not self.env['jm.tju.plan'].search([('name', '=', level), ('batch', '=', batch), ('type', '=', '1')]):
            self.env['jm.tju.plan'].create({
                'name': level,
                'batch': batch,
                'type': '1',
            })
        for sc in self.sc:
            domains = [
                ('name', '=', sc.name),
                ('batch', '=', batch),
                ('type', '=', level),
                ('study_center', '=', '1'),
            ]
            if not self.env['jm.tju.plan'].search(domains):
                self.env['jm.tju.plan'].create({
                    'name': sc.name,
                    'batch': batch,
                    'type': level,
                    'study_center': '1',
                })
            for major in self.major:
                domains = [
                    ('name', '=', major.name),
                    ('batch', '=', batch),
                    ('type', '=', level),
                    ('study_center', '=', sc.name),
                    ('major', '=', '1')

                ]
                if not self.env['jm.tju.plan'].search(domains):
                    new_plan = self.env['jm.tju.plan'].create({
                        'name': major.name,
                        'batch': batch,
                        'type': level,
                        'study_center': sc.name,
                        'major': '1',
                    })
                    for item in self.items:
                        self.env['jm.tju.plan.items'].create({
                            'item': item.item.id,
                            'money': item.money,
                            'plan_con': new_plan.id,
                        })
                else:
                    old_plan = self.env['jm.tju.plan'].search(domains)
                    for item in old_plan.items:
                        item.unlink()
                    for item in self.items:
                        self.env['jm.tju.plan.items'].create({
                            'item': item.item.id,
                            'money': item.money,
                            'plan_con': old_plan.id,
                        })
        self.env.cr.execute("DELETE from jm_tju_plan_generate where 1=1")
        self.env.cr.execute("DELETE from jm_tju_plan_generate_items where 1=1")
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'提示',
                    'message': u'成功生成招生计划表 请到招生计划处查看'
                }
            }
        }


class tju_plan_generate_items(models.Model):
    _name = 'jm.tju.plan.generate.items'

    item = fields.Many2one('jm.fee.project', u'收费项目')
    money = fields.Float(u'收费金额', digits=(7, 0))
    plan_con = fields.Many2one('jm.tju.plan.generate', ondelete='cascade')