# -*- coding: utf-8 -*-
{
    'name': "Student Management",
    'sequence':1,
    'summary': """Student and Result Management""",

    'description': """
        Student and Result Management
    """,

    'author': "Biznovare",
    'website': "http://www.biznovare.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/res_partner_view_override.xml',
        'views/manage_attendance.xml',
        'views/manage_countries.xml',
        'views/manage_hobbies.xml',
        'views/manage_status.xml',
        'views/manage_subjects.xml',
        'views/manage_results.xml',
        'views/alumni_students.xml',
        'report/student_profile_report_template.xml',
        'report/profile_report.xml',
        'report/student_attendance_report_template.xml',
        'report/attendance_report.xml',
        'data/mail_template_data.xml',
        'wizard/country_wizard_views.xml',
        'views/menuitems.xml',
        'actions/action_server.xml',
        'actions/scheduled_action_server.xml',
        'security/student_security.xml',
        'security/ir.model.access.csv',
        'webpages/example_page.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True
}