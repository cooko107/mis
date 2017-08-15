#-*- coding: utf-8 -*-
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import re
import jm_custom

class Res_Jmedu(models.Model):
	#表名和描述
	_name = 'jm.contact'
	_description = 'jmedu contact'

	#字段

	name = fields.Char(string = u'姓名', size = 20)
	code = fields.Integer(string = u'编号')

	sex = fields.Selection([(1, u'男'), (2, u'女')], string = u"性别")

	call = fields.Char(u'称谓')

	idcard = fields.Char(u'身份证')
	department = fields.Char(u'部门')
	post = fields.Char(u'职务')
	responsible_business = fields.Char(u'负责业务')

	date = fields.Date(u'出生日期')
	origin = fields.Char(u'籍贯')
	interest = fields.Char(u'兴趣爱好')


	phone = fields.Char(u'手机')
	business_phone = fields.Char(u'办公电话')
	wchat = fields.Char(u'微信')

	qq = fields.Char('QQ')
	email = fields.Char(u'邮箱')
	zipcode = fields.Char(u'邮编')

	province = fields.Many2one('all.province', u'省')
	city = fields.Many2one('all.city', u'市')
	county = fields.Many2one('all.county', u'区/县')

	detail_area = fields.Char(u'详细地址')

	headimgurl = fields.Char(u'头像', )
	headimg = fields.Html(compute='_get_headimg', string=u'头像')
	#test = fields.Many2one('jm.custom',u'tt')
	#img = fields.Binary(attachment=True)

	remarks = fields.Text(u'备注')
	attach = fields.Many2many('ir.attachment','contact_ir_attachment_rel',string=u"附件")
	#_sql_constraints = [('code_check', "UNIQUE(idcard)", u'身份证已存在'),
	#					('code_phone', "UNIQUE(phone)", u'手机号码重复'),]

	@api.one
	def _get_headimg(self):
		self.headimg = '<img src=%s width="100px" height="100px" />' % self.headimgurl

    #函数 view中on_change触发
	def province_change(self,cr,uid,ids,province,context=None):

		province_name = self.pool.get('all.province').browse(cr, uid, [province], context=context)
		return {'domain' : {'city':[('belongs', '=', province_name[0].name)]}, 'value':{'city':'', 'county':''}}

	def city_change(self,cr,uid,ids,city,context=None):

		city_name = self.pool.get('all.city').browse(cr, uid, [city], context=context)
		return {'domain' : {'county':[('belongs', '=', city_name[0].name)]}, 'value':{'county':''}}

	def generate(self, cr, uid, ids, qq, context=None):
		return {
			'type': 'ir.actions.client',
			'tag': 'get_sf_express_list',
			'target': 'new',
		}

	






	'''@api.constrains('idcard')
	def check_id(self):
		idcard_list = list(self.idcard)
		area={"11":"北京","12":"天津","13":"河北","14":"山西","15":"内蒙古",
		      "21":"辽宁","22":"吉林","23":"黑龙江","31":"上海","32":"江苏",
		      "33":"浙江","34":"安徽","35":"福建","36":"江西","37":"山东",
		      "41":"河南","42":"湖北","43":"湖南","44":"广东","45":"广西",
		      "46":"海南","50":"重庆","51":"四川","52":"贵州","53":"云南",
		      "54":"西藏","61":"陕西","62":"甘肃","63":"青海","64":"宁夏",
		      "65":"新疆","71":"台湾","81":"香港","82":"澳门","91":"国外"}
		if (not (self.idcard[0:2] in area)):
			raise ValueError('地区编码不合法')
		if(len(self.idcard)==15):
			if((int(self.idcard[6:8])+1900) % 4 == 0 or
				((int(self.idcard[6:8])+1900) % 100 == 0 and 
					(int(self.idcard[6:8])+1900) % 4 == 0 )):
				ereg=re.compile('[1-9][0-9]{5}[0-9]{2}\
					(((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1]))\
					|(02(0[1-9]|[1-2][0-9]))\
					|((04|06|09|11)(0[1-9]|[1-2][0-9]|30)))[0-9]{3}$')

			else:
				ereg=re.compile('[1-9][0-9]{5}[0-9]{2}(((01|03|05|07|08|10|12)\
					(0[1-9]|[1-2][0-9]|3[0-1]))|(02(0[1-9]|1[0-9]|2[0-8]))\
					|((04|06|09|11)(0[1-9]|[1-2][0-9]|30)))[0-9]{3}$')
			if(re.match(ereg,self.idcard)):
				pass
			else:
				raise ValueError('身份证号码出生日期超出范围或含有非法字符!')
		elif(len(self.idcard)==18):
			if (int(self.idcard[6:10]) % 4 == 0 or 
				(int(self.idcard[6:10]) % 100 == 0 and 
					int(self.idcard[6:10])%4 == 0 )):
				ereg=re.compile('[1-9][0-9]{5}19[0-9]{2}(((01|03|05|07|08|10|12)\
					(0[1-9]|[1-2][0-9]|3[0-1]))|(02(0[1-9]|[1-2][0-9]))\
					|((04|06|09|11)(0[1-9]|[1-2][0-9]|30)))[0-9]{3}[0-9Xx]$')
			else:
				ereg=re.compile('[1-9][0-9]{5}19[0-9]{2}(((01|03|05|07|08|10|12)\
					(0[1-9]|[1-2][0-9]|3[0-1]))|(02(0[1-9]|1[0-9]|2[0-8]))\
					|((04|06|09|11)(0[1-9]|[1-2][0-9]|30)))[0-9]{3}([0-9]|X|x])$')

			if(re.match(ereg,self.idcard)):
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
				if(M == idcard_list[17]):
					pass
				else:
					raise ValueError('身份证号码校验错误!')
			else:
				raise ValueError('身份证号码出生日期超出范围或含有非法字符!')
		else:
			raise ValueError('身份证号码长度不对!')

	@api.constrains('email')
	def check_email(self):
		ereg = re.compile("^[a-zA-Z0-9](([a-zA-Z0-9]*\.[a-zA-Z0-9]*)|[a-zA-Z0-9]*)[a-zA-Z0-9]@([a-z0-9A-Z]+\.)+[a-zA-Z]{2,}$")
		if(re.match(ereg, self.email)):
			pass
		else:
			raise ValueError('邮箱格式不正确')'''