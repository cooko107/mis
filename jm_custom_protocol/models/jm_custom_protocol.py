#-*- coding: utf-8 -*-
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models

class Jm_custom_protocol(models.Model):
    _name = 'jm.custom.protocol'
    _rec_name = 'custom'

    custom = fields.Many2one('jm.custom', u'渠道', ondelete='cascade')
    batch = fields.Many2one('jm.batch', u'批次')
    level = fields.Many2one('jm.level', u'层次')
    school = fields.Many2one('jm.school', u'学校')
    up_per = fields.Integer(u'上缴比例(%)')
    items = fields.One2many('jm.custom.protocol.items', 'protocol_con', u'收费项目', copy=True)
    attachment = fields.Many2many('ir.attachment', string=u"附件", ondelete='cascade', copy=False)


    @api.onchange('custom')
    def set_default_custom(self):
        custom_act_id = self.env.context.get('active_id')
        print self.env.context
        if custom_act_id:
            self.custom = custom_act_id

    @api.constrains('up_per')
    def check_up_per(self):
        if self.up_per > 100 or self.up_per < 0:
            raise ValidationError(u'上缴比例不符合比例规则')




class Jm_custom_protocol_items(models.Model):
    _name = 'jm.custom.protocol.items'

    item = fields.Many2one('jm.fee.project', u'收费项目')
    money = fields.Float(u'收费金额', digits=(7,0))
    way = fields.Selection([(1, u'比例(%)'), (2, u'金额')], u'方式', default=1)
    protocol_con = fields.Many2one('jm.custom.protocol', u'渠道链接', ondelete='cascade')

    @api.constrains('money')
    def check_money(self):
        if self.way == 1:
            if self.money < 0 or self.money > 100:
                raise ValidationError(u'收费中有比例不符合规则')

class Jm_custom_add_protocol_count(models.Model):
    _inherit = 'jm.custom'

    protocol_count = fields.Integer(u'协议数量', compute='protocol_counts')

    @api.multi
    def protocol_counts(self):
        pro_num = self.env['jm.custom.protocol'].search_count([('custom.id', '=', self.id)])
        self.protocol_count = pro_num