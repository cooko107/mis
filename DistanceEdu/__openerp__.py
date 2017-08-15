#-*- coding: utf-8 -*-
{
    'name' : '远程招生',
    'version' : '1.0',
    'summary': '远程教育管理',
    'category': 'jmedu',
    'sequence': 30,
    'description': "",
    'author': 'CooKo',
    'depends':['base','usersplus','CustomManage'],
    'data':[
            'views/nku_student_view.xml',
            'views/jm_student_view.xml',
            'views/zzu_plan_view.xml',
            'views/zzu_plan_generate_view.xml',
            'views/zzu_student_update_view.xml',
            'views/zzu_student_view.xml',
            'views/nku_plan_view.xml',
            'views/nku_plan_generate_view.xml',
            'views/nku_student_view.xml',
            'views/nku_student_update_view.xml',
            'views/tju_student_view.xml',
            'views/tju_student_update_view.xml',
            'views/tju_student_update2_view.xml',
            'views/tju_plan_generate_view.xml',
            'views/syu_plan_view.xml',
            'views/syu_plan_generate_view.xml',
            'views/syu_student_view.xml',
            'views/syu_student_update_view.xml',
            # 'views/jm_sz_student_charge_workflow.xml',
            # 'views/jm_sz_student_charge_confirm.xml',
            'views/tju_plan_view.xml',
            'views/load_message.xml',
            'security/DistanceEdu_security.xml',
            'security/ir.model.access.csv'

            ],
    #'js':[
     #   'static/src/js/x.js'
    #],

    'installable': True,
    'application': True,
    'auto_install': False
}