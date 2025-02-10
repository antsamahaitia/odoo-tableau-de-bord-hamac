# -*- coding: utf-8 -*-

{
    "name": 'Tableau de Bord',
    "version": "15.0.1.0.0",
    "category": "Dashboard",
    "depends": ['web','website'],
    "data": [
        'security/ir.model.access.csv',
        'views/dashboard_views.xml',
        'views/Bus_views.xml',
        'views/tableau_de_bord.xml',
          ],
    "assets": {
        "web.assets_backend": [
            "/tableau_de_bord/static/src/css/custom_dashboard.css",
            "/tableau_de_bord/static/src/js/custom_dashboard.js",

        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
    "description": """
        Module Tableau de Bord pour Odoo 15.5
        ======================================
        - Suivi des placements publicitaires
        - Gestion des abribus et affiches sur bus
        - Objectifs mensuels et reporting
    """
}