{
    'name': 'Padel Club Management',
    'version': '17.0.1.0.0',
    'category': 'Services/Padel',
    'summary': 'Manage padel courts, members, bookings, and invoicing.',
    'description': """
        Padel Club Management System
        ============================
        - Court Management (Indoor/Outdoor, Hourly Rates)
        - Member Profiles & Levels
        - Booking Management & Overlap Prevention
        - Invoicing & Reporting Integration
    """,
    'author': 'Shafeek',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/padel_court_views.xml',
        'views/padel_member_views.xml',
        'views/padel_booking_views.xml',
        'views/menus.xml',
    ],
    'demo': [
        'data/padel_demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}