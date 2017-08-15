#-*- coding:utf-8 -*-
from openerp import api, fields, models
#未缴费查询
class no_charge_search(models.Model):
    _name = 'jm.finance.no.charge.search'

    batch = fields.Many2one('jm.batch')
    school = fields.Many2one('jm.school')
    custom = fields.Many2one('jm.custom')
    batch_name = fields.Char(u'批次')
    school_name = fields.Char(u'学校')
    inputer_dpt = fields.Char(string=u'渠道')
    level = fields.Char(u'层次')
    study_center = fields.Char(u'学习中心')
    major = fields.Char(u'专业')
    name = fields.Char(u'姓名')
    idcard = fields.Char(u'身份证')
    no_charge_details = fields.One2many('jm.finance.no.charge.details', 'no_charge_con', u'未缴明细')
    readable = fields.Boolean(default=False)

    @api.model
    def get_school(self):
        selections = self.env['jm.school'].search([])
        return [(selection.value, selection.name) for selection in selections]

    @api.multi
    def generate_table(self):
        self.env.cr.execute("delete from jm_finance_no_charge_search where readable='True'")
        students = self.env['jm.student.order'].search([('batch', '=', self.batch.name),
                                                        ('school_table', '=', self.school.value)])
        for student in students:
            values = {}
            unlink = True
            school_table = self.school.value.replace("_", ".")
            stu_info = self.env[school_table].search([('id', '=', student.school_id)])[0]
            if self.custom:
                if stu_info.inputer_dpt.id != self.custom.id:
                    continue
            values['batch_name'] = self.batch.name
            values['level'] = stu_info.level.name
            values['study_center'] = stu_info.study_center.name
            values['major'] = stu_info.major.name
            values['inputer_dpt'] = stu_info.inputer_dpt.call
            values['readable'] = True
            values['name'] = stu_info.student.sname
            values['idcard'] = stu_info.student.idcard
            #print values
            no_charge_student = self.create(values)

            details = self.env['jm.charge'].search([('order_con', '=', student.id)])
            for detail in details:
                if detail.fee > max(detail.fee_charged, detail.up_school_fee):
                    self.env['jm.finance.no.charge.details'].create({'project':detail.project,
                                                                     'fee':detail.fee - max(detail.fee_charged, detail.up_school_fee),
                                                                     'fee_charged':max(detail.fee_charged, detail.up_school_fee),
                                                                     'no_charge_con':no_charge_student.id})
                    unlink = False
            if unlink:
                no_charge_student.unlink()
        self.env.cr.commit()
        self.env.cr.execute("delete from jm_finance_no_charge_search where readable='False'")

class No_charge_detail(models.Model):
    _name = 'jm.finance.no.charge.details'

    project = fields.Selection(selection='get_selection', string=u"收费项目")
    fee = fields.Float(string=u'收费金额', digits=(7, 0))
    fee_charged = fields.Float(string=u'已收金额', digits=(7, 0))
    no_charge_con = fields.Integer()

    @api.model
    def get_selection(self):
        selections = self.env['jm.fee.project'].search([])
        return [(selection.value, selection.name) for selection in selections]



#未上缴高校
class No_up_school_search(models.Model):
    _name = 'jm.finance.no.up.school.search'

    batch = fields.Many2one('jm.batch')
    school = fields.Many2one('jm.school')
    custom = fields.Many2one('jm.custom')
    type = fields.Selection([(1,'全额未缴费'),(2,'部分缴费')],default=1)
    project = fields.Selection(selection='get_selection', string=u"查询项目")

    batch_name = fields.Char(u'批次')
    school_name = fields.Char(u'学校')
    inputer_dpt = fields.Char(string=u'渠道')
    level = fields.Char(u'层次')
    study_center = fields.Char(u'学习中心')
    major = fields.Char(u'专业')
    name = fields.Char(u'姓名')
    idcard = fields.Char(u'身份证')
    last_time = fields.Date(u'最后缴费日期')
    readable = fields.Boolean(default=False)

    @api.model
    def get_selection(self):
        selections = self.env['jm.fee.project'].search([('value', 'like', 'tuition')])
        return [(selection.value, selection.name) for selection in selections]

    @api.multi
    def generate_table(self):
        self.env.cr.execute("delete from jm_finance_no_up_school_search where readable='True'")
        search_domain = [('batch','=',self.batch.name),
                         ('study_center','like',self.school.name),
                         ]
        if self.custom:
            search_domain.append(('inputer_dpt', '=', self.custom.call))
        students = self.env['jm.student.charge'].search(search_domain)
        for student in students:
            for fee_line in student.fee_line:
                if fee_line.project == self.project and \
                                fee_line.up_school_fee == 0 if self.type == 1 else fee_line.up_school_fee < fee_line.fee:
                    values = {'batch_name': self.batch.name,
                              'school_name': self.school.name,
                              'inputer_dpt': student.inputer_dpt,
                              'level': student.level,
                              'study_center': student.study_center,
                              'name': student.name_show,
                              'idcard': student.student_idcard.student_id,
                              'readable': True,
                              }
                    self.create(values)

        self.env.cr.execute("delete from jm_finance_no_up_school_search where readable='False'")
        self.env.cr.commit()


class No_up_school_detail(models.Model):
    _name = 'jm.finance.no.up.school.details'

    project = fields.Selection(selection='get_selection', string=u"收费项目")
    fee = fields.Float(string=u'剩余上缴金额', digits=(7, 0))
    fee_charged = fields.Float(string=u'已上缴金额', digits=(7, 0))
    no_charge_con = fields.Integer()

    @api.model
    def get_selection(self):
        selections = self.env['jm.fee.project'].search([])
        return [(selection.value, selection.name) for selection in selections]


class charged_search(models.Model):
    _name = 'jm.finance.charged.search'

    batch = fields.Many2one('jm.batch')
    school = fields.Many2one('jm.school')
    custom = fields.Many2one('jm.custom')
    linedate1 = fields.Datetime(u'划线日期1')
    linedate2 = fields.Datetime(u'划线日期2')
    project = fields.Selection(selection='get_selection', string=u"查询项目")
    readable = fields.Boolean(default=False)

    batch_name = fields.Char(u'批次')
    school_name = fields.Char(u'学校')
    inputer_dpt = fields.Char(string=u'渠道')
    level = fields.Char(u'层次')
    study_center = fields.Char(u'学习中心')
    name = fields.Char(u'姓名')
    idcard = fields.Char(u'身份证')

    @api.model
    def get_selection(self):
        selections = self.env['jm.fee.project'].search([('value', 'like', 'tuition')])
        return [(selection.value, selection.name) for selection in selections]

    @api.multi
    def generate_table(self):
        self.env.cr.execute("delete from jm_finance_charged_search where readable='True'")
        search_domain = [('batch', '=', self.batch.name),
                         ('study_center', 'like', self.school.name),
                         ]
        if self.custom:
            search_domain.append(('inputer_dpt', '=', self.custom.call))

        students = self.env['jm.student.charge'].search(search_domain)
        #print students
        for student in students:
            for fee_line in student.fee_detail:
                if fee_line.project == self.project:
                    if fee_line.charge_time > self.linedate1 and fee_line.charge_time < self.linedate2:
                        values = {'batch_name': self.batch.name,
                                  'school_name': self.school.name,
                                  'inputer_dpt': student.inputer_dpt,
                                  'level': student.level,
                                  'study_center': student.study_center,
                                  'name': student.name_show,
                                  'idcard':student.student_idcard.student_id,
                                  'readable': True,
                                  }
                        self.create(values)
        self.env.cr.execute("delete from jm_finance_charged_search where readable='False'")
        self.env.cr.commit()





