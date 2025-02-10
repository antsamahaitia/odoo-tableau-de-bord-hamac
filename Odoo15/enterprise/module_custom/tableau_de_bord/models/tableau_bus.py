from odoo import models, fields, api



class ControleBus(models.Model):
    _name = 'hamac.bus'
    _description = 'Contrôle Qualité des Bus'

    bus_numero = fields.Char('Numéro du bus', required=True)
    date_pose = fields.Date('Date de pose', required=True)
    date_fin = fields.Date('Date de fin de campagne', required=True)
    nom_campagne = fields.Char('Campagne')
    photo_pose = fields.Binary('Photos après pose')
    etat_affiche = fields.Selection([
        ('conforme', 'Conforme'),
        ('a_remplacer', 'À remplacer')
    ], string='État de l\'affiche', required=True)
    type_bus = fields.Selection([
        ('bus', 'Bus'),
        ('cotisse', 'Cotisse')
    ], string='Type', required=True)

# Champ Many2many pour lier plusieurs photos avec description
    photos_ids = fields.Many2many('ir.attachment', 'hamac_bus_attachment_rel', 'bus_id', 'attachment_id',
                                  string="Photos", domain=[('mimetype', '=', 'image/jpeg')])

    description = fields.Char('Description des photos')