from odoo import models, fields, api
from datetime import datetime

class CampagnePublicitaire(models.Model):
    _name = 'hamac.campagne'
    _description = 'Campagne Publicitaire'

    name = fields.Char('Nom de la campagne', required=True)
    date_debut = fields.Date('Date de début', required=True)
    date_fin = fields.Date('Date de fin', required=True)
    controle_ids = fields.One2many('hamac.controle', 'campagne_id', string='Contrôles')

    total_controles = fields.Integer("Nombre de contrôles", compute='_compute_total_controles', store=True)

    @api.depends('controle_ids')
    def _compute_total_controles(self):
        for record in self:
            record.total_controles = len(record.controle_ids)

class SupportPublicitaire(models.Model):
    _name = 'hamac.support'
    _description = 'Support Publicitaire'

    name = fields.Char('Identifiant', required=True)

    statut = fields.Selection([
        ('disponible', 'Disponible'),
        ('occupe', 'Occupé'),
        ('maintenance', 'En maintenance')
    ], string='Statut')

    photo = fields.Image("Photo du support")
    controle_ids = fields.One2many('hamac.controle', 'support_id', string='Contrôles')


class Probleme(models.Model):
    _name = 'hamac.probleme'
    _description = 'Problèmes et solutions'

    name = fields.Char('Problème', required=True)
    solution_ids = fields.One2many('hamac.solution', 'probleme_id', string='Solutions')

class Solution(models.Model):
    _name = 'hamac.solution'
    _description = 'Solutions aux problèmes'

    name = fields.Char('Solution', required=True)
    probleme_id = fields.Many2one('hamac.probleme', string='Problème')

# New model for photos
class ControlePhotos(models.Model):
    _name = 'hamac.controle.photo'
    _description = 'Photos du contrôle qualité'

    controle_id = fields.Many2one('hamac.controle', string='Contrôle', ondelete='cascade')
    photo = fields.Binary('Photo', required=True)
    name = fields.Char('Description')

# Modified ControleQualite model
class ControleQualite(models.Model):
    _name = 'hamac.controle'
    _description = 'Contrôle Qualité'

    name = fields.Char('Référence', required=True, copy=False, readonly=True, default='Nouveau')
    campagne_id = fields.Many2one('hamac.campagne', string='Campagne', required=True)
    support_id = fields.Many2one('hamac.support', string='Support', required=True)
    # Replace single photo field with One2many relationship
    photo_ids = fields.One2many('hamac.controle.photo', 'controle_id', string='Photos')
    date_controle = fields.Date('Date du contrôle', required=True)
    etat_support = fields.Selection([
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('mauvais', 'Mauvais')
    ], string='État du support')
    etat_affiches = fields.Selection([
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('mauvais', 'Mauvais')
    ], string='État des affiches')
    probleme_support_id = fields.Many2one('hamac.probleme', string='Problème Support')
    solution_support_id = fields.Many2one('hamac.solution', string='Solution Support',
                                            domain="[('probleme_id', '=', probleme_support_id)]")
    probleme_affiches_id = fields.Many2one('hamac.probleme', string='Problème Affiches')
    solution_affiches_id = fields.Many2one('hamac.solution', string='Solution Affiches',
                                            domain="[('probleme_id', '=', probleme_affiches_id)]")
    notes = fields.Text('Observations')

    # New field for control type
    type_controle = fields.Selection([
        ('pose', 'Contrôle de pose'),
        ('mi_campagne', 'Contrôle mi-campagne'),
        ('fin_campagne', 'Contrôle fin de campagne')
    ], string='Type de contrôle', required=True)

    @api.onchange('etat_support')
    def _onchange_etat_support(self):
        if self.etat_support in ['moyen', 'mauvais']:
            return {'domain': {'probleme_support_id': [('id', '!=', False)]}}
        else:
            self.probleme_support_id = False
            self.solution_support_id = False

    @api.onchange('etat_affiches')
    def _onchange_etat_affiches(self):
        if self.etat_affiches in ['moyen', 'mauvais']:
            return {'domain': {'probleme_affiches_id': [('id', '!=', False)]}}
        else:
            self.probleme_affiches_id = False
            self.solution_affiches_id = False

    @api.model
    def create(self, vals):
        """Crée un contrôle avec une référence continue"""
        vals['name'] = self._generate_reference()
        return super(ControleQualite, self).create(vals)

    def unlink(self):
        """Supprime un contrôle et recalcule les références des contrôles restants"""
        res = super(ControleQualite, self).unlink()
        self._recalculate_references()
        return res

    @api.model
    def _generate_reference(self):
        """Génère une nouvelle référence sous la forme CTRL0001, CTRL0002, ..."""
        total_controles = self.search_count([]) + 1  # Ajoute 1 pour la nouvelle entrée
        return f"CTRL{str(total_controles).zfill(4)}"

    @api.model
    def _recalculate_references(self):
        """Recalcule les références de tous les contrôles après suppression"""
        controles = self.search([], order='id asc')  # Récupère tous les contrôles triés par ID
        for index, record in enumerate(controles, start=1):
            record.name = f"CTRL{str(index).zfill(4)}"

        # Met à jour la séquence pour que la prochaine création continue correctement
        next_number = len(controles) + 1
        sequence = self.env['ir.sequence'].search([('code', '=', 'hamac.controle')], limit=1)
        if sequence:
            sequence.write({'number_next': next_number})




    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('hamac.controle') or 'Nouveau'
        return super(ControleQualite, self).create(vals)
