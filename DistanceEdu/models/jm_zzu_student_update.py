#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models, osv
import re
from passlib.context import CryptContext
import logging
from threading import Thread


class Zzu_Student_update(models.Model):
    #建表
    _name = 'jm.zzu.student.update'
    _description = 'zzu student import'

    name = fields.Char(u'姓名')
    idcard = fields.Char(u'身份证号码')
    sex = fields.Selection([[1,'男'],[2,'女']],string=u'性别',default=1)
    nation = fields.Char(u'民族', default="汉")
    birth = fields.Char(u'出生日期')
    study_level = fields.Char(u'文化程度')
    political = fields.Char(u'政治面貌')
    work_unit = fields.Char(u'工作单位')
    address = fields.Char(u'通讯地址')
    zip = fields.Char(u'邮编')
    phone = fields.Char(u'手机号码')
    tele = fields.Char(u'电话号码')

    # 报名信息
    batch = fields.Char(u'入学考试批次')
    study_center = fields.Char(u'学习中心')
    major = fields.Char(u'报考专业')
    entry_date = fields.Char(u'报名时间')
    test_code = fields.Char(u'准考证号')
    add_score = fields.Char(u'加分项')
    test_pwd = fields.Char(u'考试密码')
    study_code = fields.Char(u'学号')
    state = fields.Char(u'状态')

    bm_fee = fields.Float(u'报名考试费')
    tuition = fields.Float(u'第一年学费')
    z_fee = fields.Float(u'第一年杂费')
    tuition2 = fields.Float(u'第二年学费')
    z_fee2 = fields.Float(u'第二年杂费')
    jc_fee = fields.Float(u'教材费')
    bys_fee = fields.Float(u'毕业生费')
    qcfd_fee = fields.Float(u'全程辅导费（不含论文）')
    qcfd_fee2 = fields.Float(u'全程辅导费（含论文）')
    lwcx_fee = fields.Float(u'论文重修费')
    yh_fee = fields.Float(u'优惠')
    sum_fee = fields.Float(string=u'费用总和', store=True)

    remarks = fields.Text(u'备注')


    def delete(self, cr, uid, context):
        cr.execute("DELETE from jm_zzu_student_update where 1=1")

class zzu_confirm_import(models.Model):
    _name = 'jm.zzu.confirm.import'
    _description = "confirm import zzu student"

    @api.multi
    def check_id(self, stu_idcard):
        idcard_list = list(stu_idcard)
        area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古",
                "21": "辽宁", "22": "吉林", "23": "黑龙江", "31": "上海", "32": "江苏",
                "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东",
                "41": "河南", "42": "湖北", "43": "湖南", "44": "广东", "45": "广西",
                "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南",
                "54": "西藏", "61": "陕西", "62": "甘肃", "63": "青海", "64": "宁夏",
                "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
        if (not (stu_idcard[0:2] in area)):
            return 1
        if (len(stu_idcard) == 15):
            if ((int(stu_idcard[6:8]) + 1900) % 4 == 0 or
                    ((int(stu_idcard[6:8]) + 1900) % 100 == 0 and
                                 (int(stu_idcard[6:8]) + 1900) % 4 == 0)):
                ereg = re.compile('[1-9][0-9]{5}[0-9]{2}[0-9]{4}[0-9]{3}$')

            else:
                ereg = re.compile('[1-9][0-9]{5}[0-9]{2}[0-9]{4}[0-9]{3}$')
            if (re.match(ereg, stu_idcard)):
                pass
            else:
                return 1
        elif (len(stu_idcard) == 18):
            if (int(stu_idcard[6:10]) % 4 == 0 or
                    (int(stu_idcard[6:10]) % 100 == 0 and
                                 int(stu_idcard[6:10]) % 4 == 0)):
                ereg = re.compile('[1-9][0-9]{5}[0-9]{8}[0-9]{3}[0-9Xx]$')
            else:
                ereg = re.compile('[1-9][0-9]{5}[0-9]{8}[0-9]{3}([0-9]|X|x])$')

            if (re.match(ereg, stu_idcard)):
                S = ((int(idcard_list[0]) + int(idcard_list[10])) * 7 +
                     (int(idcard_list[1]) + int(idcard_list[11])) * 9 +
                     (int(idcard_list[2]) + int(idcard_list[12])) * 10 +
                     (int(idcard_list[3]) + int(idcard_list[13])) * 5 +
                     (int(idcard_list[4]) + int(idcard_list[14])) * 8 +
                     (int(idcard_list[5]) + int(idcard_list[15])) * 4 +
                     (int(idcard_list[6]) + int(idcard_list[16])) * 2 +
                     int(idcard_list[7]) * 1 + int(idcard_list[8]) * 6 +
                     int(idcard_list[9]) * 3)
                Y = S % 11
                M = "F"
                JYM = "10X98765432"
                M = JYM[Y]
                if (M == idcard_list[17]):
                    pass
                else:
                    return 1
            else:
                return 1
        else:
            return 1

    @api.multi
    def confirm_import(self):
        create = 0
        update = 0
        error = 0
        for id in self.env.context.get('active_ids'):
            import_info = self.env['jm.zzu.student.update'].browse(id)
            stu_base_info = self.env['jm.student'].search([('idcard', '=', import_info.idcard)])
            if stu_base_info:
                pass
            else:
                base_info = {
                    'sname': import_info.name,
                    'idcard': import_info.idcard,
                    'sex': import_info.sex,
                    'nation': import_info.nation,
                    'birth': import_info.birth,
                    'phone': import_info.phone,
                    'study_level':import_info.study_level,
                    'work_unit': import_info.work_unit,
                    'address': import_info.address,
                    'zip': import_info.zip,

                }
                stu_base_info = self.env['jm.student'].create(base_info)

            batch_name = import_info.batch.replace(u'年度','').replace(u'季','')

            level_name = u'高起专' if import_info.major[-3:] == u'(专)' else u'专升本'
            study_center_name = u'郑大' + import_info.study_center
            major_name = import_info.major.replace(u'(专)', '')
            inputer_dpt_code = import_info.tele.replace('-','')

            batch = self.env['jm.zzu.plan'].search(
                [('name', '=', batch_name),
                 ('batch', '=', '1')],
                limit=1
            )
            if not batch:
                import_info.state = u'批次错误'
                error += 1
                continue
            level = self.env['jm.zzu.plan'].search(
                [('name', '=', level_name),
                 ('batch', '=', batch_name),
                 ('type', '=', '1'), ],
                limit=1
            )
            if not level:
                import_info.state = u'层次错误'
                error += 1
                continue
            study_center = self.env['jm.zzu.plan'].search(
                [('name', '=', study_center_name),
                 ('batch', '=', batch_name),
                 ('type', '=', level_name),
                 ('study_center', '=', '1')],
                limit=1
            )
            if not study_center:
                import_info.state = u'学习中心错误'
                error += 1
                continue
            major = self.env['jm.zzu.plan'].search(
                [('name', '=', major_name),
                 ('batch', '=', batch_name),
                 ('type', '=', level_name),
                 ('study_center', '=', study_center_name),
                 ('major', '=', '1')],
                limit=1
            )
            if not major:
                import_info.state = u'专业错误'
                error += 1
                continue
            inputer_dpt = self.env['jm.custom'].search(
                [('phone', '=', inputer_dpt_code)],
                limit=1
            )
            info = {
                'student': stu_base_info.id,
                'add_score': import_info.add_score,
                'test_code': import_info.test_code,
                'test_pwd': import_info.test_pwd,
                'study_code': import_info.study_code,
                'entry_date': import_info.entry_date.split(' ')[0],
                'batch': batch.id,
                'level': level.id,
                'study_center': study_center.id,
                'major': major.id,
            }
            stu_info = self.env['jm.zzu.student'].search(
                [('student', '=', stu_base_info.id),
                 ('batch', '=', batch.id)]
            )

            if not stu_info:
                if not inputer_dpt:
                    import_info.state = u'电话号码错误'
                    error += 1
                    continue
                if inputer_dpt.categories == 2:
                    import_info.state = u'号码需精确到渠道'
                    error += 1
                    continue
                info['inputer_dpt'] = inputer_dpt.id
                stu_info = self.env['jm.zzu.student'].create(info)
                for item in major.items:
                    self.env['jm.charge'].create({
                        'project': item.item.value,
                        'fee': item.money,
                        'school_table': 'jm.zzu.student',
                        'school_id': stu_info.id
                    })
                create += 1

            else:
                if inputer_dpt and inputer_dpt.categories != 2:
                    info['inputer_dpt'] = inputer_dpt.id
                stu_info.update(info)
                for item in stu_info.fee_line:
                    for major_item in major.items:
                        if item.project == major_item.item.value:
                            item.fee = major_item.money
                update += 1

            if not self.env['res.users'].search([('login', '=', import_info.idcard)]):
                self.env['res.users'].create({
                    'login': import_info.idcard,
                    'password': '123456',
                    'name': import_info.name,
                    'department': u'无',
                })
            import_info.unlink()

        return {
            "type": "ir.actions.client",
            "tag": "action_notify",
            "params": {
                "title": u'学生导入成功',
                "text": u'新增%s条数据,更新%s条数据，%s条数据有误' % (create, update, error),
            }
        }



