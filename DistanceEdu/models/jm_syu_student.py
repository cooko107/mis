#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class Syu_Student(models.Model):
    #建表
    _name = 'jm.syu.student'
    _description = 'jm syu student information'
    _rec_name = 'name_show'
    _order = 'batch desc, level, study_center, inputer_dpt, major, student'

    student = fields.Many2one('jm.student', string=u'身份证')
    name_show = fields.Char(string=u'姓名', related='student.sname', readonly='True')
    sex_show = fields.Selection(string=u'性别', related='student.sex', readonly='True')
    nation_show = fields.Char(related='student.nation', string=u'民族', readonly='True')
    native_place_show = fields.Char(related='student.native_place', string=u'籍贯', readonly='True')
    birth_show = fields.Date(related='student.birth', string=u'出生日期', readonly='True')
    phone_show = fields.Char(related='student.phone', string=u'手机', readonly='True')
    wchat_show = fields.Char(related='student.wchat', string=u'微信', readonly='True')
    address_show = fields.Char(related='student.address', string=u'住址', readonly='True')

    batch = fields.Many2one('jm.syu.plan',u'批次',domain=[('batch','=','1')])
    level = fields.Many2one('jm.syu.plan',u'层次',domain=[('level','=','1')])
    major = fields.Many2one('jm.syu.plan',u'专业',domain=[('major','=','1')])
    study_center = fields.Many2one('jm.syu.plan',u'学习中心',domain=[('study_center','=','1')])
    study_no = fields.Char(u'学号')
    student_source = fields.Char(u'信息来源')
    is_test = fields.Char(u'是否申请考试')
    test_num = fields.Char(u'准考证号')
    before_school = fields.Char(u'入学前学校名称')
    bs_code = fields.Char(u'入学前学校代码')
    bgy = fields.Char(u'入学前毕业年份')
    bg_code = fields.Char(u'入学前毕业证书编号')
    subject1 = fields.Integer(u'科目一')
    subject2 = fields.Integer(u'科目二')
    subject3 = fields.Integer(u'科目三')
    add_points = fields.Integer(u'附加分')
    sum_points = fields.Integer(u'总分')
    com_points = fields.Integer(u'综合分')
    study_state = fields.Char(u'学籍状态')
    sign_date = fields.Date(u'注册时间')
    recruit_date = fields.Date(u'录取时间')
    firstcon = fields.Char(u'第一联系方式')
    inputer = fields.Char(u'所属教师')
    inputer_dpt = fields.Many2one('jm.custom',u'所属渠道')
    beschool = fields.Many2one(related='inputer_dpt.school', string=u'所属分校', store=True,readonly='True')
    up_per = fields.Integer(u'渠道上缴比例(%)',)

    fee_line = fields.One2many(
        'jm.charge',
        'school_id',
        string=u'收费情况',
        domain=[('school_table', '=', 'jm.syu.student')]
    )

    # 收费信息
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
    sum_fee = fields.Float(compute='_compute_sum', string=u'费用总和', store=True)
    remarks = fields.Text(u'备注')
    #state = fields.Char(u'收费是否确认', default="未确认")

    @api.onchange('inputer_dpt', 'batch', 'level')
    def set_fee_charge(self):
        if self.inputer_dpt and self.batch and self.level:
            protocol = self.env['jm.custom.protocol'].search(
                [('custom.id', '=', self.inputer_dpt.id),
                 ('batch.name', '=', self.batch.name),
                 ('level.name', '=', self.level.name),
                 ('school.value', '=', 'jm.syu.student')],
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


    # 批次改变时 给层次加domain
    def batch_c(self, cr, uid, ids, batch, context=None):
        batch_name = self.pool.get('jm.syu.plan').browse(cr, uid, [batch], context=context)
        return {'domain': {'level': [('batch', '=', batch_name[0].name), ('level', '=', '1')]},
                'value': {'level': '', 'major': '', 'study_center': ''}}

    # 层次改变时 给学习中心加domain
    def level_c(self, cr, uid, ids, level, context=None):
        # level_name = self.pool.get('jm.syu.plan').browse(cr, uid, [level], context=context)
        level_name = self.pool.get('jm.syu.plan').browse(cr, uid, [level], context=context)
        return {'domain': {'study_center': [('batch', '=', level_name[0].batch), ('level', '=', level_name[0].name),
                                            ('study_center', '=', '1')]},
                'value': {'major': '', 'study_center': ''}}

    # 学习中心改变时 给专业加domain
    def study_center_c(self, cr, uid, ids, study_center, context=None):
        # level_name = self.pool.get('jm.syu.plan').browse(cr, uid, [level], context=context)
        study_center_name = self.pool.get('jm.syu.plan').browse(cr, uid, [study_center], context=context)
        return {'domain': {
            'major': [('batch', '=', study_center_name[0].batch), ('study_center', '=', study_center_name[0].name),
                      ('major', '=', '1'), ('level', '=', study_center_name[0].level)]},
                'value': {'major': ''}}

    '''@api.constrains('level','student')
    def create_order(self):
        self.env.cr.execute("SELECT id from jm_syu_student where student=%s and level=%s" %(self.student.id, self.level.id))
        exist = self.env.cr.fetchall()
        if(exist):
            raise ValueError("该学生在该学年已报过")
        else:
            self.env.cr.execute("INSERT into jm_student_order (student_id,student_table,school_id,school_table) "
                                "values(%s,'jm_student',%s,'jm_syu_student')" % (self.student.id, self.id))'''
    
class New_inf(models.TransientModel):
    _name = 'jm.syu.student.change'

    inputer = fields.Char(u'所属教师')
    inputer_dpt = fields.Many2one('jm.custom',u'所属部门')

    @api.multi
    def change_inputer(self):
        for id in self.env.context.get('active_ids'):
            stu_info = self.env['jm.syu.student'].browse(id)
            new_info = self.env['jm.syu.student.change'].browse(self.id)
            inputer_dpt = new_info.inputer_dpt
            inputer = new_info.inputer
            stu_info.inputer = inputer
            stu_info.inputer_dpt = inputer_dpt
            stu_info.set_fee_charge()
            # stu_info.state = 'init'
            # wkf_ins = self.env['workflow.instance'].create({
            #     'res_type':'jm.syu.student',
            #     'uid':1,
            #     'wfk_id':6,
            #     'state':'active',
            #     'res_id':id,
            # })
            # self.env['workflow.workitem'].create({
            #     'act_id':23,
            #     'inst_id':wkf_ins.id,
            #     'state':'complete',
            # })

