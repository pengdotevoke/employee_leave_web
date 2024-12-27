{
    'name': 'Employee Leave Web Interface',
    'version': '1.0',
    'author': 'James Oginga',
    'category': 'Website',
    'summary': 'Allows employees to apply for leave through the website',
    'depends': ['website', 'hr_holidays'],
    'data': [
        'views/leave_web_templates.xml',
    ],
    'installable': True,
    'application': False,
}
