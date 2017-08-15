# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : '客户管理',
    'version' : '1.0',
    'summary': 'hello',
    'category': 'jmedu',
    'sequence': 30,
    'description': "",
    'author': 'CooKo',
    'depends':['base'],
    'data':[
            #'static/src/xml/test.xml',
            #'static/src/js/test.js',
            'views/jm_contact_view.xml',
            'views/jm_personal_view.xml',
            'views/jm_school_view.xml',
            'views/jm_custom_view.xml',
            'views/test.xml',
            'security/ir.model.access.csv',
            'security/custommanage_security.xml',
            'all.city.csv',
            'all.county.csv',
            'all.province.csv',

            ],
    'qweb': [
        'static/src/xml/test.xml',
        'views/delete.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
