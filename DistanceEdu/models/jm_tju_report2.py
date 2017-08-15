#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re
class Tju_Report(models.Model):
    _name = 'jm.tju.report2'

    _rec_name = 'start_time'

    batch = fields.Many2one('jm.batch', u'批次')
    start_time = fields.Date(u'起始日期')
    end_time = fields.Date(u'结束日期')

    qd = fields.Char(u'渠道')
    ben_count = fields.Float(u'本科', digits=(12,0))
    zhuan_count = fields.Float(u'专科', digits=(12,0))
    sum_count = fields.Float(u'总计', digits=(12,0))
    wbl = fields.Float(u'未补录', digits=(12,0))
    ylq = fields.Float(u'已录取', digits=(12,0))

    @api.constrains('start_time','start_time')
    def check(self):
        if(self.start_time > self.end_time or not self.start_time or not self.end_time):
            raise ValueError("输入的时间无效")


    def generate_report2(self,cr,uid,ids,context=None):
        #取得输入的起止时间
        starttime = self.browse(cr, uid, ids, context=context)[0].start_time
        endtime = self.browse(cr, uid, ids, context=context)[0].end_time
        batch = self.browse(cr, uid, ids, context=context)[0].batch
        #因为在上面已做验证  所以直接pass
        if(starttime > endtime or not starttime or not endtime):
            pass
        else:
            cr.execute("delete from jm_tju_report2 WHERE 1=1")
            #选择高起专各个渠道的id
            cr.execute("SELECT id,call from jm_custom")
            all_qd = cr.fetchall()

            cr.execute("select id from jm_tju_plan where batch='%s' and name='高起专' and type='1'" %(batch.name))
            gqz = cr.fetchall()

            cr.execute("select id from jm_tju_plan where batch='%s' and name='专升本' and type='1'" %(batch.name))
            zsb = cr.fetchall()

            #遍历各个高起专的学习中心
            for each_gqz in gqz:
                for each_qd in all_qd:
                    each_sum = 0
                # 统计改高起专的学习中心报名人数
                    cr.execute("SELECT COUNT(id) from jm_tju_student where  level=%s and inputer_dpt=%s and entry_date between "
                                "'%s' and '%s'" %(each_gqz[0],each_qd[0],starttime, endtime))
                    eachgqz_count = cr.fetchall()
                #写入报表数据库

                    cr.execute("INSERT into jm_tju_report2(batch,start_time,end_time,qd, zhuan_count) values(%s,'%s','%s','%s', %s)"
                                %(batch.id,starttime,endtime,each_qd[1], eachgqz_count[0][0]))
            #遍历各个专升本的学习中心
            for each_zsb in zsb:
                for each_qd in all_qd:
                #统计改专升本的学习中心报名人数
                    cr.execute("SELECT COUNT(id) from jm_tju_student where level=%s and inputer_dpt=%s and entry_date between "
                                "'%s' and '%s'" % (each_zsb[0], each_qd[0], starttime, endtime))
                    eachzsb_count = cr.fetchall()
                #查看改学习中心是否存在
                    cr.execute("SELECT zhuan_count from jm_tju_report2 where qd='%s' and start_time='%s' and end_time='%s'"
                                "" % (each_qd[1],starttime, endtime))
                    zhuan_count = cr.fetchall()
                #存在 则更新
                    if (zhuan_count):
                        cr.execute("UPDATE jm_tju_report2 set (ben_count,sum_count)=(%s,%s) where qd='%s' and start_time='%s' and end_time='%s'"
                                     %(eachzsb_count[0][0],eachzsb_count[0][0]+zhuan_count[0][0],each_qd[1], starttime, endtime))
                #否则 插入
                    else:
                        cr.execute("INSERT into jm_tju_report2(batch,start_time,end_time,qd, zhuan_count,ben_count,sum_count) values(%s,'%s','%s','%s',0, %s,%s)"
                                %(batch.id,starttime,endtime,each_qd[1], eachzsb_count[0][0],eachzsb_count[0][0]))
            #将无效数据删除
            cr.execute("DELETE from jm_tju_report2 where qd is NULL")
            return {
                'type': 'ir.actions.client',
                'tag': 'operation_success',
                'target':'self',
                'action':{
                    'action': 'doNotify',
                    'message':{
                        'title':u'提示',
                        'message':u'数据统计成功'
                    }
                }
            }










