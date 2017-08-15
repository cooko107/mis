#-*- coding:utf-8 -*-
from openerp import api, fields, models


item_dic = {
    u'第一年学费':'tuition',
    u'第二年学费':'tuition2',
    u'报名费':'bm_fee',
}

class zzu_charge_import(models.Model):
    _name = 'jm.zzu.up.school.fee.import'

    batch = fields.Char(u'年级')
    school_code = fields.Char(u'学号')
    name = fields.Char(u'姓名')
    major = fields.Char(u'专业')
    project = fields.Char(u'项目')
    money = fields.Float(u'金额')
    time = fields.Char(u'录入时间')
    state = fields.Char(u'状态')


class Zzu_up_fee_confirm(models.TransientModel):
    _name = 'jm.zzu.up.school.fee.confirm'

    @api.multi
    def confirm_import_up(self):
        success = 0
        fail = 0
        act_ids = self.env.context.get('active_ids')
        for record in self.env['jm.zzu.up.school.fee.import'].browse(act_ids):
            stu = self.env['jm.zzu.student'].search([('study_code', '=', record.school_code)], limit=1)
            if not stu:
                record.state = u'未找到该学生'
                fail += 1
                continue
            vals = {
                'project':item_dic[record.project],
                'fee':record.money,
                'charge_time':record.time,
                'school_id':stu.id,
                'school_table':'jm.zzu.student',
            }
            self.env['jm.up.school.fee.details'].create(vals)
            self.env['jm.charge'].search(
                [('school_id', '=', stu.id),
                 ('school_table', '=', 'jm.zzu.student'),
                 ('project', '=', item_dic[record.project])],
                limit=1
            ).up_school_fee += record.money
            record.state = u'导入成功'
            success += 1
        return {
            "type": "ir.actions.client",
            "tag": "action_notify",
            "params": {
                "title": u'上缴导入成功',
                "text": u'%s成功, %s失败' %(success, fail),
            }
        }



class Syu_charge_import(models.Model):
    _name = 'jm.syu.up.school.fee.import'

    batch = fields.Char(u'年级')
    school_code = fields.Char(u'学号')
    name = fields.Char(u'姓名')
    major = fields.Char(u'专业')
    project = fields.Char(u'项目')
    money = fields.Float(u'金额')
    time = fields.Char(u'缴费时间')
    fee_type = fields.Char(u'费用类型')
    remarks = fields.Char(u'备注')
    state = fields.Char(u'状态')


class Syu_up_fee_confirm(models.TransientModel):
    _name = 'jm.syu.up.school.fee.confirm'

    @api.multi
    def confirm_import_up(self):
        success = 0
        fail = 0
        act_ids = self.env.context.get('active_ids')
        for record in self.env['jm.syu.up.school.fee.import'].browse(act_ids):
            stu = self.env['jm.syu.student'].search([('study_no', '=', record.school_code)], limit=1)
            if not stu:
                record.state = u'未找到该学生'
                fail += 1
                continue
            vals = {
                'project': item_dic[record.project],
                'fee': record.money,
                'charge_time': record.time,
                'school_id': stu.id,
                'school_table': 'jm.zzu.student',
            }
            self.env['jm.up.school.fee.details'].create(vals)
            self.env['jm.charge'].search(
                [('school_id', '=', stu.id),
                 ('school_table', '=', 'jm.syu.student'),
                 ('project', '=', item_dic[record.project])],
                limit=1
            ).up_school_fee += record.money
            record.state = u'导入成功'
            success += 1
        return {
            "type": "ir.actions.client",
            "tag": "action_notify",
            "params": {
                "title": u'上缴导入成功',
                "text": u'%s成功, %s失败' % (success, fail),
            }
        }


class Tju_charge_import(models.Model):
    _name = 'jm.tju.up.school.fee.import'

    batch = fields.Char(u'年级')
    school_code = fields.Char(u'学号')
    name = fields.Char(u'姓名')
    project = fields.Char(u'项目')
    money = fields.Float(u'金额')
    time = fields.Char(u'缴费时间')
    account = fields.Many2one('jm.charge.account', u'出款账户')
    remarks = fields.Char(u'备注')
    state = fields.Char(u'状态')


class Tju_up_fee_confirm(models.TransientModel):
    _name = 'jm.tju.up.school.fee.confirm'

    @api.multi
    def confirm_import_up(self):
        success = 0
        fail = 0
        act_ids = self.env.context.get('active_ids')
        for record in self.env['jm.tju.up.school.fee.import'].browse(act_ids):
            stu = self.env['jm.tju.student'].search([('study_code', '=', record.school_code)], limit=1)
            if not stu:
                record.state = u'未找到该学生'
                fail += 1
                continue
            vals = {
                'project': item_dic[record.project],
                'fee': record.money,
                'charge_time': record.time,
                'school_id': stu.id,
                'school_table': 'jm.tju.student',
            }
            self.env['jm.up.school.fee.details'].create(vals)
            self.env['jm.charge'].search(
                [('school_id', '=', stu.id),
                 ('school_table', '=', 'jm.tju.student'),
                 ('project', '=', item_dic[record.project])],
                limit=1
            ).up_school_fee += record.money
            record.state = u'导入成功'
            success += 1
        return {
            "type": "ir.actions.client",
            "tag": "action_notify",
            "params": {
                "title": u'上缴导入成功',
                "text": u'%s成功, %s失败' % (success, fail),
            }
        }

class Nku_charge_import(models.Model):
    _name = 'jm.nku.up.school.fee.import'

    batch = fields.Char(u'年级')
    school_code = fields.Char(u'学号')
    name = fields.Char(u'姓名')
    project = fields.Char(u'项目')
    money = fields.Float(u'金额')
    time = fields.Char(u'缴费时间')
    account = fields.Many2one('jm.charge.account', u'出款账户')
    remarks = fields.Char(u'备注')
    state = fields.Char(u'状态')


class Nku_up_fee_confirm(models.TransientModel):
    _name = 'jm.nku.up.school.fee.confirm'

    @api.multi
    def confirm_import_up(self):
        success = 0
        fail = 0
        act_ids = self.env.context.get('active_ids')
        for record in self.env['jm.nku.up.school.fee.import'].browse(act_ids):
            stu = self.env['jm.nku.student'].search([('study_num', '=', record.school_code)], limit=1)
            if not stu:
                record.state = u'未找到该学生'
                fail += 1
                continue
            vals = {
                'project': item_dic[record.project],
                'fee': record.money,
                'charge_time': record.time,
                'school_id': stu.id,
                'school_table': 'jm.nku.student',
            }
            self.env['jm.up.school.fee.details'].create(vals)
            self.env['jm.charge'].search(
                [('school_id', '=', stu.id),
                 ('school_table', '=', 'jm.nku.student'),
                 ('project', '=', item_dic[record.project])],
                limit=1
            ).up_school_fee += record.money
            record.state = u'导入成功'
            success += 1
        return {
            "type": "ir.actions.client",
            "tag": "action_notify",
            "params": {
                "title": u'上缴导入成功',
                "text": u'%s成功, %s失败' % (success, fail),
            }
        }