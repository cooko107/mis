#-*- coding: utf-8 -*-
{
    'name' : '财务',
    'version' : '1.0',
    'summary': '财务',
    'category': 'jmedu',
    'sequence': 30,
    'description': "",
    'author': 'CooKo',
    'depends':['base','DistanceEdu','mail'],
    'data':[
            'views/form_hide_edit.xml',
            'views/jm_finance_workflow.xml',
            'views/jm_finance_receipt.xml',
            'templates/report_template.xml',
            'report/report_receipt.xml',
            'views/jm_finance_up_school.xml',
            'views/jm_finance_search.xml',
            'views/jm_finance_student_charge.xml',
            'views/jm_finance_menu.xml',
            'security/finance_security.xml',
            'security/ir.model.access.csv',
            ],
    'installable': True,
    'application': True,
    'auto_install': False
}