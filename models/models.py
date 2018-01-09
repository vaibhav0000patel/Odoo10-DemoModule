# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.tools import email_split
from odoo.exceptions import UserError,ValidationError

import datetime
import time

class student(models.Model):
    _name = 'student.profile'
    _rec_name = 'name'
    name = fields.Char(string="Name")
    email = fields.Char(string="Email Address")
    dob = fields.Date(string="Birthdate")
    city = fields.Char(string="City")
    data_image = fields.Binary("Profile Picture", attachment=True, help="This field holds the image")
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'), ('female', 'Female')])
    website = fields.Char(string="Website")

    lunch_time = fields.Float(string="Lunch Time")

    country_id = fields.Many2one('student.country', ondelete="cascade", string='Country')
    country_cc = fields.Char(related='country_id.country_code',string="Country Code")

    status_id = fields.Many2one('student.status', ondelete="cascade", string="Status")
    current_status_id = fields.Integer(compute='_current_status_id')

    hobbies_ids = fields.Many2many('student.hobbies', string="Hobbies")

    attendance_ids = fields.One2many('student.attendance',inverse_name='student_id',string='Attendance')

    result_id = fields.One2many('student.result',inverse_name='student_id',string='Result')
    total = fields.Integer(compute="_value_pc", store=True)
    total_subjects = fields.Integer(compute="_value_pc", store=True)
    country_cd = fields.Char(compute="_value_cc", store=True)
    average = fields.Float(compute="_value_avg",store=True)

    kb_color = fields.Integer('Color Index', compute="change_color_on_kanban", store=True)




    @api.one
    def _current_status_id(self):
        self.current_status_id = self.status_id.id

    @api.multi
    @api.depends('status_id')
    def change_color_on_kanban(self):
        '''
            2 = red
            3 = yellow
            5 = green
            7 = orange
        '''
        for record in self:
            color = 1
            if record.current_status_id == 1:
                color = 6
            elif record.current_status_id == 2:
                color = 4
            elif record.current_status_id == 3:
                color = 2
            else:
                color = 5
            record.kb_color = color

    @api.one
    def status_change(self,context=None):
        if(context.get('status_id_ctx',False)):
            self.status_id=context.get('status_id_ctx',False)

    @api.multi
    @api.depends('total')
    def _value_avg(self):
        for record in self:
            if(record.total_subjects!=0):
                record.average = ((record.total)/record.total_subjects)

    @api.multi
    @api.depends('result_id','result_id.subject_score')
    def _value_pc(self):
        for record in self :
            #record.total = sum([x for x.subject_score in record.result_id])
            s = 0
            sc=0
            for x in record.result_id :
                s += x.subject_score
                sc +=1
            record.total = s
            record.total_subjects = sc





    # METHOD OVERRIDING
    @api.model
    def create(self, vals):
        data = super(student, self).create(vals)
        data._value_email_id()
        return data

    @api.multi
    def write(self, vals):
        result_data = super(student, self).write(vals)
        for record in self:
            record._value_email_id()

        return True

    @api.model
    def _value_email_id(self):
        emails = self.env['res.partner'].search([('email', '=', self.email)], limit=1)
        if emails:
            emails.write({
                'name': self.name,
                'email': self.email
            })
        else:
            self.env['res.partner'].create({
                'name': self.name,
                'email': self.email
            })
    # METHOD OVERRIDING







    # PROFILE MAIL
    @api.multi
    def action_quotation_send(self):
        template_id = self.env.ref('student.student_profile_email_template')
        template_id.send_mail(self.id)

    @api.multi
    def action_quotation_send_selected(self,obj):
        template_id = obj.env.ref('student.student_profile_email_template')
        template_id.send_mail(obj.id)

    @api.multi
    def action_quotation_send_all(self):
        sp_object = self.env['student.profile'].search([])
        for obj in sp_object:
            template_id = obj.env.ref('student.student_profile_email_template')
            template_id.send_mail(obj.id)
    # PROFILE MAIL




    # ATTENDANCE MAIL
    @api.multi
    def action_quotation_send_attendance(self):
        template_id = self.env.ref('student.student_attendance_email_template')
        template_id.send_mail(self.id)

    @api.multi
    def action_quotation_send_attendance_selected(self, obj):
        template_id = obj.env.ref('student.student_attendance_email_template')
        template_id.send_mail(obj.id)

    @api.multi
    def action_quotation_send_attendance_all(self):
        sp_object = self.env['student.profile'].search([])
        for obj in sp_object:
            template_id = obj.env.ref('student.student_attendance_email_template')
            template_id.send_mail(obj.id)
    # ATTENDANCE MAIL




    @api.multi
    def duplicate_student_record(self):


        result_ids_list = []
        for result in self.result_id:
            result_ids_list.append((0,0,{'subject_ids': result.subject_ids.id ,'subject_score' : result.subject_score}))

        attendance_ids_list = []
        for result in self.attendance_ids:
            attendance_ids_list.append((0, 0, {'in_time': result.in_time, 'out_time': result.out_time}))

        vals = {}
        vals.update({
            'name': self.name,
            'email': self.email,
            'data_image':self.data_image,
            'dob': self.dob,
            'gender': self.gender,
            'city':self.city,
            'lunch_time':self.lunch_time,
            'website':self.website,
            'country_id': self.country_id.id,
            'country_cd': self.country_cd,
            'status_id': self.status_id.id,
            'attendance_ids': attendance_ids_list,
            'hobbies_ids': [(6, 0, self.hobbies_ids.ids)],
            'result_id': result_ids_list,
            'total': self.total,
            'total_subjects': self.total_subjects,
            'average': self.average,
            'kb_color': self.kb_color
        })
        self.env['student.profile'].create(vals)

    @api.model
    def render_html(self, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        docargs = {
            'doc_ids': self._ids,
            'doc_model': self.model,
            'docs': docs,
            'time': time
        }
        return self.env['report'].render('student.student_profile_report_template', docargs)


class Attendance(models.Model):
    _name = "student.attendance"
    _rec_name='student_id'
    _order='in_time desc'
    student_id = fields.Many2one('student.profile',ondelete="cascade", string='Student')
    in_time = fields.Datetime(string="In Time")
    out_time = fields.Datetime(string="Out Time")



    # CONSTRAINTS
    @api.constrains('in_time','out_time')
    def _validate_check_in_out_time(self):
        for record in self:
            in_time_datetime = datetime.datetime.strptime(record.in_time,'%Y-%m-%d %H:%M:%S')
            in_time_str = in_time_datetime.date()
            out_time_str = datetime.datetime.strptime(record.out_time,'%Y-%m-%d %H:%M:%S').date()

            if(in_time_str!=out_time_str):
                raise ValidationError("Both the dates should be same!")
            else:
                in_time_start = datetime.datetime.strftime(in_time_str, '%Y-%m-%d 00:00:00')
                in_time_end = datetime.datetime.strftime(in_time_str, '%Y-%m-%d 23:59:59')
                results = self.env['student.attendance'].search(
                    ['&', '&', '&',
                     ('student_id', '=', record.student_id.id),
                     ('in_time', '>=', in_time_start),
                     ('in_time', '<=', in_time_end),
                     ('id', '!=', record.id)
                    ])
                if results:
                    raise ValidationError(
                        "Attendance of " +
                        str(record.student_id.name) +
                        " for " +
                        str(in_time_datetime.strftime('%d-%m-%Y')) +
                        " is already done!"
                    )
    # CONSTRAINTS


class result(models.Model):
    _name = 'student.result'
    subject_ids = fields.Many2one('student.subjects',ondelete="cascade", string='Subjects')
    subject_score = fields.Integer(string='Marks')
    student_id = fields.Many2one('student.profile',ondelete="cascade", string='Student')

class country(models.Model):
    _name = 'student.country'
    _rec_name = 'country_name'
    country_name = fields.Char(string="Country Name")
    country_code = fields.Char(string="Country Code")
    active = fields.Boolean(string="Country Active")

    student_ids = fields.One2many('student.profile',inverse_name='country_id',string='Student')
    students_count = fields.Integer(compute="count_countries_students", store=False)

    @api.one
    def count_countries_students(self):
        self.students_count = len(self.student_ids)

class status(models.Model):
    _name = 'student.status'
    _rec_name = 'status_name'
    status_name = fields.Char(string="Status Name")
    student_ids = fields.One2many('student.profile',inverse_name='status_id',string='Student')
    students_count = fields.Integer(compute="count_statuses_students", store=False)

    @api.one
    def count_statuses_students(self):
        self.students_count = len(self.student_ids)

class hobbies(models.Model):
    _name = 'student.hobbies'
    _rec_name = 'hobby_name'
    hobbies_sequence = fields.Integer('sequence', help="Sequence for the handle.", default=10)
    hobby_name = fields.Char(string="Hobby Name")
    student_ids = fields.Many2many('student.profile',inverse_name='hobbies_ids',string='Student')
    students_count = fields.Integer(compute="count_hobbies_students", store=False)

    @api.one
    def count_hobbies_students(self):
        self.students_count = len(self.student_ids)

class subjects(models.Model):
    _name="student.subjects"
    _rec_name = 'subject_name'
    subject_name = fields.Char(string="Subject")

class res_partner(models.Model):
    _inherit="res.partner"
    hobbies_ids = fields.Many2many('student.hobbies', string="Hobbies")

