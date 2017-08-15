# -*- coding: utf-8 -*-
{
    'name': "今明基础数据", # 这里我改成了公司的开发系统全称，中文。

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': "浙江今明教育集团",         # 这里是描述这个模块是干什么用的

    'author': "Songbin",   #这里我改成了自己的名字，汉语拼音

    'sequence':30,

    'website': "http://www.jmedu.com.cn",  #这里是指向公司所在有官方网站

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',   #这里是指模块是属于哪个分类
    'version': '0.1',    # 是指程序的版本

    # any module necessary for this one to work correctly
    'depends': ['base',],  # 依赖的模块，最基本的模块，默认为 'base'

    # always loaded
    'data': [                                      # 这里就是加载的数据文件，放在这里指明。
        # 'security/ir.model.access.csv',
        'views/jmbasedata.xml',  #数字文件，这里放了 动作和菜单 的数据文件。

    ],
    # only loaded in demonstration mode

   'installable': True,    # 是否可以安装
   'application': True,    # 是否指定为应用
   'auto_install': False   # 是否自动安装，默认为否
}