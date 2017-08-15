#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import logging
_logger = logging.getLogger(__name__)
from openerp.exceptions import except_orm

#天津大学学生报名表
class Tju_Student(models.Model):
    #建表
    _name = 'jm.tju.student'
    _description = 'jm tju student information'
    _rec_name = 'student'
    _order = 'batch desc, level, study_center, inputer_dpt desc, major, student'

    #state = fields.Float()
    student = fields.Many2one('jm.student', string=u'身份证')
    name_show = fields.Char(string=u'姓  名', related='student.sname', readonly='True')
    sex_show = fields.Selection(string=u'性别', related='student.sex', readonly='True')
    nation_show = fields.Char(related='student.nation', string=u'民族', readonly='True')
    native_place_show = fields.Char(related='student.native_place', string=u'籍贯', readonly='True')
    birth_show = fields.Date(related='student.birth', string=u'出生日期', readonly='True')
    phone_show = fields.Char(related='student.phone', string=u'手机', readonly='True')
    wchat_show = fields.Char(related='student.wchat', string=u'微信', readonly='True')
    address_show = fields.Char(related='student.address', string=u'住址', readonly='True')

    #其他信息
    graduate_time = fields.Date(u'毕业时间')
    graduate_major = fields.Char(u'专业')
    graduate_school = fields.Char(u'毕业院校名称')
    graduate_code = fields.Char(u'毕业院校代码')
    graduate_cer_code = fields.Char(u'毕业证书代码')

    #报名信息
    study_center = fields.Many2one('jm.tju.plan',string=u'报考中心',domain=[('study_center', '=','1')])
    batch = fields.Many2one('jm.tju.plan',string=u'招生批次号',domain=[('batch','=','1')])
    level = fields.Many2one('jm.tju.plan', string=u'报考层次',domain=[('type','=','1')])
    major = fields.Many2one('jm.tju.plan', string=u'报考专业')
    entry_date = fields.Date(u'报名日期')
    school_date = fields.Char(u'入学日期')
    student_state = fields.Char(u'学生状态')
    tuition_fees = fields.Char(u'学费标准')
    zkzh = fields.Char(u'准考证号')
    study_code = fields.Char(u'学号')
    is_test = fields.Char(string=u'是否免试', default='参加考试')
    inputer = fields.Char(string=u'所属教师')
    inputer_dpt = fields.Many2one('jm.custom',string=u'所属渠道')
    beschool = fields.Many2one(related='inputer_dpt.school', string=u'所属分校', store=True,readonly='True')
    firstcon = fields.Char(u'第一联系方式')
    up_per = fields.Integer(u'渠道上缴比例(%)')

    #表2
    reg_time = fields.Date(u'注册时间')
    reg_code = fields.Char(u'注册号')
    school_state = fields.Char(u'学籍状态')
    highest_degree = fields.Char(u'最高学历')
    is_change = fields.Char(u'是否异动')
    warning = fields.Char(u'警告', default='正常')
    college_remark = fields.Char(u'学院备注')
    syn = fields.Char(u'同步')

    #收费信息
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
    yh_fee = fields.Float(u'优惠')
    ykj = fields.Float(u'一口价')
    sum_fee = fields.Float(compute='_compute_sum',string=u'费用总和',store=True)
    remarks = fields.Text(u'备注')

    fee_line = fields.One2many(
        'jm.charge',
        'school_id',
        string=u'收费情况',
        domain=[('school_table', '=', 'jm.tju.student')],
    )



    @api.onchange('inputer_dpt', 'batch', 'level')
    def set_fee_charge(self):
        if self.inputer_dpt and self.batch and self.level:
            protocol = self.env['jm.custom.protocol'].search(
                [('custom.id', '=', self.inputer_dpt.id),
                 ('batch.name', '=', self.batch.name),
                 ('level.name', '=', self.level.name),
                 ('school.value', '=', 'jm.tju.student')],
                limit=1,
            )
            self.up_per = protocol.up_per
            for fee_line in self.fee_line:
                fee_line.fee_charge = 0
                for item in protocol.items:
                    if fee_line.project == item.item.value:
                        if item.way == 1:
                            fee_line.fee_charge = item.money * fee_line.fee / 100
                        if item.way == 2:
                            fee_line.fee_charge = item.money


    #批次改变时 给层次加domain
    def batch_c(self, cr, uid, ids, batch, context=None):
        batch_name = self.pool.get('jm.tju.plan').browse(cr, uid, [batch], context=context)
        return {'domain': {'level': [('batch','=',batch_name[0].name),('type', '=', '1')]},
                'value': {'level': '', 'major':'','study_center':''}}

    # 层次改变时 给学习中心加domain
    def level_c(self, cr, uid, ids,level,context=None):
        #level_name = self.pool.get('jm.tju.plan').browse(cr, uid, [level], context=context)
        level_name = self.pool.get('jm.tju.plan').browse(cr, uid, [level], context=context)
        return {'domain': {'study_center': [('batch','=',level_name[0].batch),('type', '=', level_name[0].name),
                                     ('study_center', '=', '1')]},
                'value':{'major' : '','study_center':''}}

    # 学习中心改变时 给专业加domain
    def study_center_c(self, cr, uid, ids, study_center, context=None):
        # level_name = self.pool.get('jm.tju.plan').browse(cr, uid, [level], context=context)
        study_center_name = self.pool.get('jm.tju.plan').browse(cr, uid, [study_center], context=context)
        return {'domain': {'major': [('batch','=',study_center_name[0].batch),('study_center', '=', study_center_name[0].name),
                                            ('major', '=', '1'),('type','=',study_center_name[0].type)]},
                'value': {'major': ''}}


#天津大学 学生信息更改中间表
class New_inf(models.TransientModel):
    _name = 'jm.tju.student.change'

    inputer = fields.Char(u'所属教师')
    inputer_dpt = fields.Many2one('jm.custom',u'所属部门')


    @api.multi
    def change_inputer(self):
        for id in self.env.context.get('active_ids'):
            stu_info = self.env['jm.tju.student'].browse(id)
            new_info = self.env['jm.tju.student.change'].browse(self.id)
            inputer_dpt = new_info.inputer_dpt
            inputer = new_info.inputer
            stu_info.inputer = inputer
            stu_info.inputer_dpt = inputer_dpt
            stu_info.set_fee_charge()
            # stu_info.state = 'init'
            # wkf_ins = self.env['workflow.instance'].create({
            #     'res_type':'jm.tju.student',
            #     'uid':1,
            #     'wfk_id':4,
            #     'state':'active',
            #     'res_id':id,
            # })
            # self.env['workflow.workitem'].create({
            #     'act_id':15,
            #     'inst_id':wkf_ins.id,
            #     'state':'complete',
            # })
