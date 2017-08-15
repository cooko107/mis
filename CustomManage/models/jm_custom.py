#-*- coding: utf-8 -*-
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re
from openerp.http import request

class Res_Jmedu(models.Model):
	_name = 'jm.custom'
	_description = 'jmedu customt'
	_order = 'call'
	_rec_name = 'call'

	image = fields.Binary(u'头像')
	name = fields.Char(string = u'全称', size = 20)
	call = fields.Char(string = u'简称', size = 20)
	code = fields.One2many('jm.custom.code','cus_con',string=u'编码',ondelete='cascade')
	categories = fields.Selection([(1, '渠道'),(2,'分校')], string=u'类别')
	area = fields.Char(string=u'地区' )
	custom_rank = fields.Selection([(1, u'普通客户')], string=u'客户级别')
	school = fields.Many2one('jm.de.school',string=u'所属分校')

	#公司信息

	legal_rep = fields.Char(u'法人代表')
	bus_reg = fields.Char(u'统一社会信用代码')
	reg_address = fields.Char(u'注册地址')
	duty_paragraph =  fields.Char(u'税号')
	open_bank =  fields.Char(u'开户银行')
	bank_account = fields.Char(u'银行账号')

	#联系信息
	phone = fields.Char(u'联系方式')
	email = fields.Char(u'Email', default='')
	qq = fields.Char(u'QQ')
	wchat = fields.Char(u'微信')
	province = fields.Many2one('all.province', u'省')
	city = fields.Many2one('all.city', u'市')
	county = fields.Many2one('all.county', u'区/县')
	zipcode = fields.Char(u'邮编')
	detail_address = fields.Char(u'详细地址')
	remarks = fields.Char(u'备注')

	contact = fields.Many2many('jm.contact','name', string=u'联系人')


	count = fields.Float(string=u'天大学生数量', compute='student_count')
	zzu_count = fields.Float(string=u'郑大学生数量', compute='zzu_student_count')
	syu_count = fields.Float(string=u'石大学生数量', compute='syu_student_count')

	def student_count(self):
		self.env.cr.execute("SELECT count(id) from jm_tju_student where inputer_dpt=%s" %(self.id))
		count = self.env.cr.fetchall()
		self.count = count[0][0]

	def zzu_student_count(self):
		self.env.cr.execute("SELECT count(id) from jm_zzu_student where inputer_dpt=%s" % (self.id))
		count = self.env.cr.fetchall()
		self.zzu_count = count[0][0]

	def syu_student_count(self):
		self.env.cr.execute("SELECT count(id) from jm_syu_student where inputer_dpt=%s" % (self.id))
		count = self.env.cr.fetchall()
		self.syu_count = count[0][0]


	#_sql_constraints = [('code_check', "UNIQUE(name)", u'名称已存在')]
	#_sql_constraints = [('code_check', "CHECK(id != phone)", u'error')]

	def province_change(self,cr,uid,ids,province,context=None):

		province_name = self.pool.get('all.province').browse(cr, uid, [province], context=context)
		return {'domain' : {'city':[('belongs', '=', province_name[0].name)]}, 'value':{'city':'', 'county':''}}

	def city_change(self,cr,uid,ids,city,context=None):

		city_name = self.pool.get('all.city').browse(cr, uid, [city], context=context)
		return {'domain' : {'county':[('belongs', '=', city_name[0].name)]}, 'value':{'county':''}}

	def delete_custom(self, cr, uid, allid, context):
		for each_id in allid:
			cr.execute("delete from jm_custom where id=%s" %(each_id))
			cr.execute("delete from jm_custom_code where cus_con='%s'" %(str(each_id)))


	'''def cancel(self, cr, uid, allid, context):
		for id in allid:
			cr.execute("UPDATE jm_custom set name=%s where id=%s" %(id, id))'''
	'''@api.constrains('email')
	def check_email(self):
		ereg = re.compile("^[a-zA-Z0-9](([a-zA-Z0-9]*\.[a-zA-Z0-9]*)|[a-zA-Z0-9]*)[a-zA-Z0-9]@([a-z0-9A-Z]+\.)+[a-zA-Z]{2,}$")
		if(re.match(ereg, self.email)):
			pass
		else:
			raise ValueError('邮箱格式不正确')'''

class Custom_code(models.Model):
	_name = 'jm.custom.code'

	cus_con = fields.Char(u'客户编码')
	code = fields.Char(u'客户代码')