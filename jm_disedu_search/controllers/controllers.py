#-*- coding:utf-8 -*-
from openerp import http
import json
import jinja2,sys,os
from openerp.http import request
import base64
import re

class Jm_disedu_search(http.Controller):
    def load_env(self):
        if hasattr(sys, 'frozen'):
            # When running on compiled windows binary, we don't have access to package loader.
            path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
            loader = jinja2.FileSystemLoader(path)
        else:
            loader = jinja2.PackageLoader('openerp.addons.jm_disedu_search', "views/jinjahtml")
        env = jinja2.Environment(loader=loader, autoescape=True)
        return env



    @http.route('/jmdisedu/getschool', type='http', auth='public', csrf=False)
    def render_school(self, **post):
        values = [
            {'value':'jm.tju.plan','name':'天津大学'},
            {'value':'jm.syu.plan','name':'石油大学'},
            {'value':'jm.zzu.plan','name':'郑州大学'},
            {'value':'jm.nku.plan','name':'南开大学'},
        ]
        data = json.dumps(values)
        if post.get('callback'):
            data = post.get('callback') + "(" + data + ")"
            return data
        else:
            return data

    @http.route('/jmdisedu/getsc/<string:school>', type='http', auth='public', csrf=False)
    def render_sc(self,school, **post):
        req_env = request.env[school]
        batch = req_env.search([('batch','=','1')], order='name desc', limit=1).name
        scs = req_env.search([('batch','=',batch),('study_center','=','1')])
        values = [sc.name for sc in scs]
        data = [each for each in set(values)]
        data = json.dumps(data)
        if post.get('callback'):
            data = post.get('callback') + "(" + data + ")"
            return data
        else:
            return data

    @http.route('/jmdisedu/getmajor/', type='http', auth='public', csrf=False)
    def render_major(self, **post):
        values = []
        req_env = request.env[post.get('school')]
        batch = req_env.search([('batch', '=', '1')], order='name desc', limit=1).name
        domains = [
            ('batch', '=', batch),
            ('study_center', '=', post.get('sc')),
        ]

        if post.get('school') == 'jm.tju.plan' or post.get('school') == 'jm.zzu.plan':
            domains.append(('type','=', post.get('level')))
        else:
            domains.append(('level','=', post.get('level')),)

        majors = req_env.search(domains, order='name')
        for major in majors:
            fee = 0
            for item in major.items:
                if item.money > 1500:
                    fee += item.money

            values.append({
                'name': major.name,
                'fee':fee,
            })

        data = json.dumps(values)
        if post.get('callback'):
            data = post.get('callback') + "(" + data + ")"
            return data
        else:
            return data

    @http.route('/jmdisedu/branch/', type='http', auth='public', csrf=False)
    def render_branch(self):
        env = self.load_env()
        return env.get_template('branch.html').render({
        })


    @http.route('/jmdisedu/query1/', type='http', auth='public', csrf=False)
    def render_query1(self):
        env = self.load_env()
        return env.get_template('query1.html').render({
        })

    @http.route('/jmdisedu/query2/', type='http', auth='public', csrf=False)
    def render_query2(self):
        env = self.load_env()
        return env.get_template('query2.html').render({
        })

    @http.route('/jmdisedu/render/major/', type='http', auth='public', csrf=False)
    def render_all_major(self, **post):
        req_env = request.env['jm.major']
        majors = req_env.search([], order='name desc')
        values = [major.name for major in majors]
        data = [each for each in set(values)]
        data = json.dumps(data)
        if post.get('callback'):
            data = post.get('callback') + "(" + data + ")"
            return data
        else:
            return data

    @http.route('/jmdisedu/get/schools/', type='http', auth='public', csrf=False)
    def render_major_school(self, **post):
        batch = request.env['jm.batch'].search([], order='name desc',limit=1)[0].name
        major = post.get('major')
        level = post.get('level')
        tjus = request.env['jm.tju.plan'].search(
            [('batch','=',batch),
             ('type','=',level),
             ('name','=',major),
             ('major','=','1'),]
        )
        nkus = request.env['jm.nku.plan'].search(
            [('batch', '=', batch),
             ('level', '=', level),
             ('name', '=', major),
             ('major', '=', '1'), ]
        )
        syus = request.env['jm.syu.plan'].search(
            [('batch', '=', batch),
             ('level', '=', level),
             ('name', '=', major),
             ('major', '=', '1'), ]
        )
        zzus = request.env['jm.zzu.plan'].search(
            [('batch', '=', batch),
             ('type', '=', level),
             ('name', '=', major),
             ('major', '=', '1'), ]
        )

        values = []
        if tjus:
            sc = [tju.study_center for tju in tjus]
            values.append({
                'school':u'天津大学',
                'sc':sc
            })
        if syus:
            sc = [syu.study_center for syu in syus]
            values.append({
                'school': u'石油大学',
                'sc': sc
            })
        if nkus:
            sc = [nku.study_center for nku in nkus]
            values.append({
                'school': u'南开大学',
                'sc': sc
            })
        if zzus:
            sc = [zzu.study_center for zzu in zzus]
            values.append({
                'school': u'郑州大学',
                'sc': sc
            })

        data = json.dumps(values)
        if post.get('callback'):
            data = post.get('callback') + "(" + data + ")"
            return data
        else:
            return data