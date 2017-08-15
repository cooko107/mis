#-*- coding: utf-8 -*-
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models

class jm_charge_details(models.Model):
    _name = 'jm.student.charge.details'

    project = fields.Selection(selection='get_selection', string=u"收费项目")
    fee = fields.Float(string=u'收费金额',digits=(7, 0))
    way = fields.Selection([[1, '支付宝转账'], [2, '银行卡转账'], [3, '现金收费']], u"收费方式")
    account = fields.Many2one('jm.charge.account', u'收费账户')
    charge_time = fields.Date(u"收费时间")
    confirm_state = fields.Selection([(1,u'待审核'),(2,u'审核通过'),(3,u'审核未通过')], u'审核状态', default=1)
    remarks = fields.Char(u'备注')
    deletable = fields.Boolean(default=True)
    readonly = fields.Boolean(default=False)
    printed = fields.Boolean(u'已打印',default=False)
    single_charge_con = fields.Integer()
    no_up_school_search_con = fields.Integer()
    school_table = fields.Char(u'学校表')
    school_id = fields.Integer()

    @api.model
    def get_selection(self):
        selections = self.env['jm.fee.project'].search([])
        return [(selection.value, selection.name) for selection in selections]

    @api.onchange('confirm_state')
    def set_delete(self):
        if self.confirm_state == 2:
            self.deletable = False


class Jm_up_school_fee_details(models.Model):
    _name = 'jm.up.school.fee.details'

    project = fields.Selection(selection='get_selection', string=u"上缴项目")

    fee = fields.Float(string=u'上缴金额',digits=(7, 0))
    way = fields.Selection([[1, '支付宝转账'], [2, '银行卡转账'], [3, '现金收费']], u"上缴方式")
    account = fields.Many2one('jm.charge.account', u'出款账户')
    charge_time = fields.Date(u"上缴时间")
    remarks = fields.Char(u'备注')
    printing = fields.Boolean(u'打印')
    single_charge_con = fields.Integer()
    multi_charge_con = fields.Integer()
    school_id = fields.Integer()
    school_table = fields.Char(u'学校表')

    @api.model
    def get_selection(self):
        selections = self.env['jm.fee.project'].search([])
        return [(selection.value, selection.name) for selection in selections]


class Jm_tju_student_add_con(models.Model):
    _inherit = 'jm.tju.student'

    WORKFLOW_STATE_SELECTION = [
        ('init', '登记收费'),
        ('confirm', '待审核'),
        ('not_approve', '审核未通过'),
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION, default='init', string="审批状态", readonly=True)

    charge_details = fields.One2many(
        'jm.student.charge.details',
        'school_id',
        string=u'收费明细',
        domain=[('school_table','=','jm.tju.student')]
    )
    up_school_detail = fields.One2many(
        'jm.up.school.fee.details',
        'school_id',
        string=u'上缴',
        domain=[('school_table','=','jm.tju.student')]
    )

    sum_charge = fields.Float(u'收费总额', readonly=1)
    sum_up = fields.Float(u'上缴总额', readonly=1)
    invoice_money = fields.Float(u'发票金额', digits=(7,0))
    invoice = fields.Selection([(1, u'未开票'), (2,u'待开票'), (3,u'已开票')],u'发票状态',default=1)


    @api.constrains('charge_details')
    @api.multi
    def set_school(self):
        school_table = 'jm.tju.student'
        charge_details = self.env['jm.student.charge.details'].search([
            ('school_id', '=', self.id),
            ('school_table', '=', None),
        ])
        for each in charge_details:
            each.update({'school_table':school_table})



    @api.multi
    def to_confirm(self):
        error = 1
        for charge_details in self.charge_details:
            if charge_details.confirm_state != 2:
                error = 0
                break
        if error:
            raise ValidationError(u'尚未登记任何收费')
        self.state = 'confirm'
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'学生登记成功',
                    'message': u'已进入审批流程'
                }
            }
        }

    @api.multi
    def approve(self):
        for charge_details in self.charge_details:
            if charge_details.confirm_state == 1 or charge_details.confirm_state == 3:
                charge_details.confirm_state = 2
                charge_details.deletable = False
        for fee_line in self.fee_line:
            fee_line.fee_charged = 0
            for charge_details in self.charge_details:
                if charge_details.project == fee_line.project:
                    fee_line.fee_charged += charge_details.fee
        self.state = 'init'
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'审核完成',
                    'message': u'学生登记已通过'
                }
            }
        }

    @api.multi
    def not_approve(self):
        for charge_details in self.charge_details:
            if charge_details.confirm_state == 1:
                charge_details.confirm_state = 3
        self.state = 'not_approve'
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'审核完成',
                    'message': u'学生登记未通过'
                }
            }
        }

class Jm_syu_student_add_con(models.Model):
    _inherit = 'jm.syu.student'

    WORKFLOW_STATE_SELECTION = [
        ('init', '登记收费'),
        ('confirm', '待审核'),
        ('not_approve', '审核未通过'),
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION, default='init', string="审批状态", readonly=True)


    charge_details = fields.One2many(
        'jm.student.charge.details',
        'school_id',
        string=u'收费明细',
        domain=[('school_table','=','jm.syu.student')]
    )
    up_school_detail = fields.One2many(
        'jm.up.school.fee.details',
        'school_id',
        string=u'上缴',
        domain=[('school_table', '=', 'jm.syu.student')]
    )
    invoice_money = fields.Float(u'发票金额', digits=(7, 0))
    invoice = fields.Selection([(1, u'未开票'), (2, u'待开票'), (3, u'已开票')], u'发票状态', default=1)

    @api.constrains('charge_details')
    @api.multi
    def set_school(self):
        school_table = 'jm.syu.student'
        charge_details = self.env['jm.student.charge.details'].search([
            ('school_id', '=', self.id),
            ('school_table', '=', None),
        ])
        for each in charge_details:
            each.update({'school_table': school_table})

    @api.multi
    def to_confirm(self):
        error = 1
        for charge_details in self.charge_details:
            if charge_details.confirm_state != 2:
                error = 0
                break
        if error:
            raise ValidationError(u'尚未登记任何收费')
        self.state = 'confirm'
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'登记完成',
                    'message': u'学生已进入审批流程'
                }
            }
        }

    @api.multi
    def approve(self):
        for charge_details in self.charge_details:
            if charge_details.confirm_state == 1 or charge_details.confirm_state == 3:
                charge_details.confirm_state = 2
                charge_details.deletable = False
        self.state = 'init'
        for fee_line in self.fee_line:
            fee_line.fee_charged = 0
            for charge_details in self.charge_details:
                if charge_details.project == fee_line.project:
                    fee_line.fee_charged += charge_details.fee
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'审核完成',
                    'message': u'学生登记已通过'
                }
            }
        }

    @api.multi
    def not_approve(self):
        for charge_details in self.charge_details:
            if charge_details.confirm_state == 1:
                charge_details.confirm_state = 3
        self.state = 'not_approve'
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'审核完成',
                    'message': u'学生登记未通过'
                }
            }
        }


class Jm_zzu_student_add_con(models.Model):
    _inherit = 'jm.zzu.student'

    WORKFLOW_STATE_SELECTION = [
        ('init', '登记收费'),
        ('confirm', '待审核'),
        ('not_approve', '审核未通过'),
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION, default='init', string="审批状态", readonly=True)

    charge_details = fields.One2many(
        'jm.student.charge.details',
        'school_id',
        string=u'收费明细',
        domain=[('school_table','=','jm.zzu.student')]
    )
    up_school_detail = fields.One2many(
        'jm.up.school.fee.details',
        'school_id',
        string=u'上缴',
        domain=[('school_table', '=', 'jm.zzu.student')]
    )
    invoice_money = fields.Float(u'发票金额', digits=(7, 0))
    invoice = fields.Selection([(1, u'未开票'), (2, u'待开票'), (3, u'已开票')], u'发票状态', default=1)

    @api.constrains('charge_details')
    @api.multi
    def set_school(self):
        school_table = 'jm.zzu.student'
        charge_details = self.env['jm.student.charge.details'].search([
            ('school_id', '=', self.id),
            ('school_table', '=', None),
        ])
        for each in charge_details:
            each.update({'school_table': school_table})

    @api.multi
    def to_confirm(self):
        error = 1
        for charge_details in self.charge_details:
            if charge_details.confirm_state != 2:
                error = 0
                break
        if error:
            raise ValidationError(u'尚未登记任何收费')
        self.state = 'confirm'
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'登记完成',
                    'message': u'学生已进入审批流程'
                }
            }
        }

    @api.multi
    def approve(self):
        for charge_details in self.charge_details:
            if charge_details.confirm_state == 1 or charge_details.confirm_state == 3:
                charge_details.confirm_state = 2
                charge_details.deletable = False
        self.state = 'init'
        for fee_line in self.fee_line:
            fee_line.fee_charged = 0
            for charge_details in self.charge_details:
                if charge_details.project == fee_line.project:
                    fee_line.fee_charged += charge_details.fee
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'审核完成',
                    'message': u'学生登记已通过'
                }
            }
        }

    @api.multi
    def not_approve(self):
        for charge_details in self.charge_details:
            if charge_details.confirm_state == 1:
                charge_details.confirm_state = 3
        self.state = 'not_approve'
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'审核完成',
                    'message': u'学生登记未通过'
                }
            }
        }



class Jm_nku_student_add_con(models.Model):
    _inherit = 'jm.nku.student'

    WORKFLOW_STATE_SELECTION = [
        ('init', '登记收费'),
        ('confirm', '待审核'),
        ('not_approve', '审核未通过'),
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION, default='init', string="审批状态", readonly=True)

    charge_details = fields.One2many(
        'jm.student.charge.details',
        'school_id',
        string=u'收费明细',
        domain=[('school_table','=','jm.nku.student')]
    )
    up_school_detail = fields.One2many(
        'jm.up.school.fee.details',
        'school_id',
        string=u'上缴',
        domain=[('school_table', '=', 'jm.nku.student')]
    )
    invoice_money = fields.Float(u'发票金额', digits=(7, 0))
    invoice = fields.Selection([(1, u'未开票'), (2, u'待开票'), (3, u'已开票')], u'发票状态', default=1)

    @api.constrains('charge_details')
    @api.multi
    def set_school(self):
        school_table = 'jm.nku.student'
        charge_details = self.env['jm.student.charge.details'].search([
            ('school_id', '=', self.id),
            ('school_table', '=', None),
        ])
        for each in charge_details:
            each.update({'school_table': school_table})

    @api.multi
    def to_confirm(self):
        error = 1
        for charge_details in self.charge_details:
            if charge_details.confirm_state != 2:
                error = 0
                break
        if error:
            raise ValidationError(u'尚未登记任何收费')
        self.state = 'confirm'
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'登记完成',
                    'message': u'学生已进入审批流程'
                }
            }
        }

    @api.multi
    def approve(self):
        for charge_details in self.charge_details:
            if charge_details.confirm_state == 1 or charge_details.confirm_state == 3:
                charge_details.confirm_state = 2
                charge_details.deletable = False
        self.state = 'init'
        for fee_line in self.fee_line:
            fee_line.fee_charged = 0
            for charge_details in self.charge_details:
                if charge_details.project == fee_line.project:
                    fee_line.fee_charged += charge_details.fee
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'审核完成',
                    'message': u'学生登记已通过'
                }
            }
        }

    @api.multi
    def not_approve(self):
        for charge_details in self.charge_details:
            if charge_details.confirm_state == 1:
                charge_details.confirm_state = 3
        self.state = 'not_approve'
        return {
            'type': 'ir.actions.client',
            'tag': 'operation_success',
            'target': 'self',
            'action': {
                'action': 'doNotify',
                'message': {
                    'title': u'审核完成',
                    'message': u'学生登记未通过'
                }
            }
        }


class Jm_finance_charge_import(models.Model):
    _name = 'jm.finance.charge.import'

    name = fields.Char(u'姓名')
    batch = fields.Many2one('jm.batch', u'批次')
    school = fields.Many2one('jm.school', u'学校')
    idcard = fields.Char(u'身份证')
    study_code = fields.Char(u'学号')
    project = fields.Many2one('jm.fee.project', u'收费项目')
    way = fields.Selection([[1, '支付宝转账'], [2, '银行卡转账'], [3, '现金收费']], u"收费方式",default=2)
    money = fields.Float(u'收费金额')
    time = fields.Date(u'收费时间')
    account = fields.Many2one('jm.charge.account', u'收费账户')
    remarks = fields.Char(u'备注')

class Jm_finance_charge_import_confirm(models.TransientModel):
    _name = 'jm.finance.charge.import.confirm'

    @api.multi
    def real_import(self):
        success = 0
        fail = 0
        for id in self.env.context.get('active_ids'):
            import_info = self.env['jm.finance.charge.import'].browse(id)
            stu = self.env[import_info.school.value].search(
                [('student.idcard', '=', import_info.idcard),
                 ('batch.name', '=', import_info.batch.name)],
                limit = 1,
            )
            if not stu:
                fail += 1
                continue
            self.env['jm.student.charge.details'].create({
                'project':import_info.project.value,
                'account':import_info.account.id,
                'charge_time':import_info.time,
                'fee':import_info.money,
                'school_id':stu.id,
                'school_table':import_info.school.value,
                'deletable':False,
                'confirm_state':2,
                'way':import_info.way,
                'remarks':import_info.remarks,
            })
            charge_line = self.env['jm.charge'].search(
                [('project','=',import_info.project.value),
                 ('school_id', '=', stu.id),
                 ('school_table', '=', import_info.school.value)],
                limit = 1,
            )
            charge_line.fee_charged += import_info.money
            success += 1
        return {
            "type": "ir.actions.client",
            "tag": "action_notify",
            "params": {
                "title": u'收费导入成功',
                "text": u'%s成功, %s失败' % (success, fail),
            }
        }




#收款账户
class Charge_account(models.Model):
    _name = 'jm.charge.account'

    _rec_name = 'account'
    account = fields.Char(u'收款账户')



class Pre_charge(models.Model):
    _name = 'jm.pre.charge.student'

    idcard = fields.Char(u'身份证')
    name = fields.Char(u'姓名')
    sex = fields.Selection([(1, '男'), (2, '女')], string=u'性别')
    phone = fields.Char(u'手机')
    inputer = fields.Char(u'介绍人')

    batch = fields.Selection(selection='set_batch', string=u'批次')
    level = fields.Selection(selection='set_level', string=u'层次')
    school = fields.Selection(selection='set_school', string=u'学校')
    study_center = fields.Many2one('jm.sc', string=u'学习中心')
    major = fields.Char(u'专业')

    fee_line = fields.One2many('jm.pre.charge.student.items', 'pre_con', string='收费')


    @api.model
    def set_batch(self):
        selections = self.env['jm.batch'].search([])
        return [(selection.id, selection.name) for selection in selections]

    @api.model
    def set_level(self):
        selections = self.env['jm.level'].search([])
        return [(selection.id, selection.name) for selection in selections]

    @api.model
    def set_school(self):
        selections = self.env['jm.school'].search([])
        return [(selection.id, selection.name) for selection in selections]

    @api.onchange('school')
    @api.model
    def set_sc(self):
        domain = {}
        if not self.school:
            domain['study_center'] = [('name', '=', 0)]
            return {'domain': domain}
        else:
            school_name = self.env['jm.school'].browse(self.school)[0].name
            print school_name
            domain['study_center'] = [('name', 'like', school_name)]
            return {'domain': domain}






class Pre_charge_items(models.Model):
    _name = 'jm.pre.charge.student.items'

    project = fields.Selection(selection='get_selection', string=u"收费项目")
    fee = fields.Float(string=u'收费金额',digits=(7, 0))
    way = fields.Selection([[1, '支付宝转账'], [2, '银行卡转账'], [3, '现金收费']], u"收费方式")
    account = fields.Many2one('jm.charge.account', u'收费账户')
    charge_time = fields.Date(u"收费时间")
    remarks = fields.Char(u'备注')
    pre_con = fields.Many2one('jm.pre.charge.student', ondelete='cascade')


    @api.model
    def get_selection(self):
        selections = self.env['jm.fee.project'].search([])
        return [(selection.value, selection.name) for selection in selections]
