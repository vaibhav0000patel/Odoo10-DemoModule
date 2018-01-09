# -*- coding: utf-8 -*-
from odoo import http

# class Student(http.Controller):
#     @http.route('/student/student/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/student/student/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('student.listing', {
#             'root': '/student/student',
#             'objects': http.request.env['student.student'].search([]),
#         })

#     @http.route('/student/student/objects/<model("student.student"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('student.object', {
#             'object': obj
#         })

class Student(http.Controller):
    @http.route('/student/example', auth="public", website="true")
    def index(self):
        students = http.request.env['student.profile'].sudo().search([])
        return http.request.render('student.example_page', {'students':students})
