#-*- coding: utf-8 -*-
from passlib.context import CryptContext
from openerp import api, fields, models
import re

class Syu_Student_Updata(models.Model):
    #建表
    _name = 'jm.nku.student.update'
    #_description = 'jm student information'

    name = fields.Char(u'姓名')
    idcard = fields.Char(u'证件号码')
    sex = fields.Selection([[1, '男'], [2, '女']], string=u'性别', default=1)
    nation = fields.Char(u'民族', default="汉族")
    birth = fields.Char(u'出生日期')
    political = fields.Char(u'政治面貌')
    job_type = fields.Char(u'职业类别')
    study_level = fields.Char(u'文化程度')
    zip = fields.Char(u'邮政编码')
    address = fields.Char(u'通信地址')
    work_unit = fields.Char(u'工作单位')
    phone = fields.Char(u'手机')

    batch = fields.Char(u'入学批次')
    level = fields.Char(u'培养层次')
    study_center = fields.Char(u'学习中心')
    major = fields.Char(u'就读专业名称')


    bm_time = fields.Char(u'报名时间')
    bm_code = fields.Char(u'报名编号')
    nk_username = fields.Char(u'用户名')
    enrol_time = fields.Char(u'录取时间')
    ap_num = fields.Char(u'奥鹏学号')
    study_num = fields.Char(u'学号')
    ap_email = fields.Char(u'电子邮件')
    inputer_dpt = fields.Char(u'录入人')
    # 收费信息
    remarks = fields.Text(u'录取备注')
    state = fields.Char(u'状态')

class nku_confirm_import(models.Model):
    _name = 'jm.nku.confirm.import'
    _description = "confirm import nku student"

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
            import_info = self.env['jm.nku.student.update'].browse(id)
            #print import_info.idcard
            stu_base_info = self.env['jm.student'].search([('idcard', '=', import_info.idcard)])
            if not stu_base_info:
                if self.check_id(import_info.idcard):
                    import_info.state = u'身份证号码错误'
                    continue
                stu_base_info = self.env['jm.student'].create({
                    'name':import_info.name,
                    'sname':import_info.name,
                    'idcard':import_info.idcard,
                    'sex':import_info.sex,
                    'nation':import_info.nation,
                    'birth':import_info.birth,
                    'political':import_info.political,
                    'job_type':import_info.job_type,
                    'study_level':import_info.study_level,
                    'zip':import_info.zip,
                    'address':import_info.address,
                    'work_unit':import_info.work_unit,
                    'phone':import_info.phone,

                })

            batch_name = '20' + import_info.batch.replace('03', u'春').replace('09','秋')
            level_name = u'高起专' if import_info.level == u'专科' else import_info.level
            study_center_name = u'南开' + import_info.study_center

            batch = self.env['jm.nku.plan'].search([
                ('name', '=', batch_name),
                ('batch', '=', '1')
            ])
            level = self.env['jm.nku.plan'].search([
                ('name', '=', level_name),
                ('batch', '=', batch_name)
            ])
            study_center = self.env['jm.nku.plan'].search([
                ('name', '=', study_center_name),
                ('batch', '=', batch_name),
                ('level', '=', level_name)
            ])
            major = self.env['jm.nku.plan'].search([
                ('name', '=', import_info.major),
                ('batch', '=', batch_name),
                ('level', '=', level_name),
                ('study_center', '=', study_center_name)
            ])
            inputer_code = self.env['jm.custom.code'].search([
                ('code', '=', import_info.inputer_dpt.lower() if  import_info.inputer_dpt else import_info.inputer_dpt)
            ], limit=1)
            inputer_dpt = 0
            inputer = ''
            if not inputer_code:
                inputer_code = self.env['jm.personal'].search([
                    ('code', '=', import_info.inputer_dpt)
                ], limit=1)
                if not inputer_code:
                    import_info.state = u'录入人找不到'
                    error += 1
                    continue
                else:
                    inputer_dpt = inputer_code.besq.id
                    inputer = inputer_code.code
            else:
                inputer_dpt = inputer_code.cus_con

            if not batch:
                import_info.state = u'找不到批次'
                error += 1
                continue
            if not level:
                import_info.state = u'找不到层次'
                error += 1
                continue
            if not study_center:
                import_info.state = u'找不到学习中心'
                error += 1
                continue
            if not major:
                import_info.state = u'找不到专业'
                error += 1
                continue

            stu_info = self.env['jm.nku.student'].search([
                ('student.idcard','=', import_info.idcard),
                ('batch.name', '=', batch_name)
            ])
            values = {
                'student': stu_base_info.id,
                'bm_time': import_info.bm_time,
                'bm_code': import_info.bm_code,
                'nk_username': import_info.nk_username,
                'enrol_time': import_info.enrol_time,
                'ap_num': import_info.ap_num,
                'study_num': import_info.study_num,
                'ap_email': import_info.ap_email,
                'batch': batch.id,
                'level': level.id,
                'study_center': study_center.id,
                'major': major.id,
                'inputer_dpt': inputer_dpt,
                'inputer': inputer,
            }

            if not stu_info:
                stu_info = self.env['jm.nku.student'].create(values)
                for item in major.items:
                    self.env['jm.charge'].create({
                        'project': item.item.value,
                        'fee': item.money,
                        'school_table': 'jm.nku.student',
                        'school_id': stu_info.id
                    })
                create += 1
            else:
                stu_info.update(values)
                for item in stu_info.fee_line:
                    for major_item in major.items:
                        if item.project == major_item.item.value:
                            item.fee = major_item.money
                update += 1
            user_info = self.env['res.users'].search([
                ('login', '=', import_info.idcard)
            ])
            if not user_info:
                self.env['res.users'].create({
                    'login':import_info.idcard,
                    'department':u'无',
                    'name':import_info.name,
                    'password':'123456',
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


