{
    'name': 'Mikrotik API Integration',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Integrasi dengan Mikrotik API',
    'description': 'Modul untuk integrasi dengan Mikrotik API.',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/mikrotik_config_views.xml',
        'static/src/js/mikrotik_monitor.js',
    ],
    'installable': True,
    'application': True,
}
