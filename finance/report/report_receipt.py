# _*_ coding: utf-8 _*_
from openerp import models, fields, api
import base64
import os
import re
import datetime

count_map = {1:1, 2:10, 3:100, 4:1000, 5:10000}

def set_to_chinese(money, s):
    end_map = {10:u'拾',100:u'佰',1000:u'仟',10000:u'万'}
    trans_map = {0:u'零',1:u'壹',2:u'贰',3:u'叁',4:u'肆',
                 5:u'伍',6:u'陆',7:u'柒',8:u'捌',9:u'玖'}
    if s == 1:
        return trans_map[money]
    if money%s == 0:
        return trans_map[money/s]+end_map[s]
    else:
        mid = trans_map[0] if len(str(money))-len(str(money%s))>1 else u''
        return trans_map[money/s]+end_map[s]+ mid + set_to_chinese(money%s, count_map[len(str(money%s))])

class Report_receipt(models.AbstractModel):
    _name = "report.finance.report_receipt"

    @api.multi
    def render_html(self,data):
        report = self.env['report']
        report_obj = self.env['jm.student.charge.print.item'].browse(self.id)[0]
        school = report_obj.print_item[0].school_table
        stu = report_obj.print_item[0].school_id
        stu_info = self.env[school].browse(stu)

        user = self.env['res.users'].browse(self.env.uid)[0]
        name = stu_info.student.sname
        money = 0
        code = base64.b64encode(os.urandom(20))
        for item in report_obj.print_item:
            money += item.fee
            item.printed = True
        chinese_money = set_to_chinese(int(money), count_map[len(str(int(money)))])+u'元整'

        pattern = re.compile(r'20(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+).(\d+)000$')
        num = pattern.sub(r'\1\2\3\4\5\6\7', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        num = user.areacode + num + str(self.env.uid).zfill(5)
        drawer = user.name
        values = {'name':name,
                  'project':report_obj.project,
                  'num':num,
                  'money':money,
                  'drawer':drawer,
                  'fake_code':code,
                  'time':fields.Date.today(),
                  'state':u'正常'}
        self.env['jm.finance.receipt'].create(values)
        docargs = {
            "project":report_obj.project,
            "num":num,
            "name": name,
            "money": money,
            "code": code,
            'chinese_money':chinese_money,
        }

        return report.render('finance.report_receipt_template', docargs)

class Pre_charge_report_receipt(models.AbstractModel):
    _name = "report.finance.pre_charge_report_receipt"

    @api.multi
    def render_html(self, data=None):
        report = self.env['report']
        docs = self.env['jm.pre.charge.student'].browse(self._ids)
        docargs = {
            'docs': docs,
        }
        return report.render('finance.pre_charge_report_receipt_template', docargs)