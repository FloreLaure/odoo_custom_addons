# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'GESTION MARCHE',
    'version' : '1.1',
    'summary': 'GESTION MARCHE',
    'sequence': 10,
    'description': "Gestion des marches",
    
    'depends' : ['base_setup', ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'view/appel.xml',
        'view/structure.xml',
        'view/dossier.xml',
        'view/type_m.xml',
        'view/listeSoumisLine.xml',
        'view/ListeMarcheSoumis.xml',
        'view/concurence.xml',

    ],
    
    'installable': True,
    'application': True,
    
}


