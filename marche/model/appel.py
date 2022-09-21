from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError



class appel(models.Model):
    _name = "marche.appel"
    _description = "Enregistrement des appels d'offre"

    name= fields.Text(string="Intitulé du marché", required ="True")
    structure = fields.Many2one("marche.structure", string="Structure demandeuse", required =True)
    lieu = fields.Char(string="Lieu de dépot")
    date_parution = fields.Date(string="Date de parution")
    date_depot = fields.Date(string="Date de dépot")
    date_limite = fields.Datetime(string="Date limite de dépot")
    budget = fields.Integer(string="Budget")
    num_quotidient = fields.Integer(string="Numero du quotidient")
    page = fields.Integer(string="Page")
    dure = fields.Char(string="Durée de la mission")
    typ = fields.Many2one("marche.type_m", string="Type du marché")
    num_appel = fields.Integer(string="Numéro d'appel d'offre")
    fiche = fields.Binary(string="Quotidient", )
    dossier = fields.Many2many("marche.dossier", string="Dossier à fournir", required =True)
    concuren=fields.One2many("marche.concurence", "resultats", string="Résultat")
    state = fields.Selection([('N','Nouveau'),('S', 'Soumis'),('O','Obtenu'),('P', 'Perdu')], default="N", string="Etat")


    def action_soumis(self):
        self.state = 'S'


    def action_nouveau(self):
        self.state = 'N'

    def action_obtenu(self):
        self.state = 'O'

    def action_perdu(self):
        self.state = 'P'

## classe pour l'enregistrement des dossiers à fournir ##

class dossier(models.Model):
    _name = "marche.dossier"
    _description = "dossier à fournir"

    dossier = fields.Char(string="Pièces à fournir")


## classe pour l'enregistrement des structure demandeuses ##

class structure(models.Model):
    _name = "marche.structure"
    _description = "Structure demandeuse"

    name= fields.Char(string="Nom de la structure", required =True)
    phone = fields.Integer(string="Telephone")
    mail = fields.Char(string="E-Mail")


## classe pour l'enregistrement des informations sur les concurents ##

class concurence(models.Model):
    _name="marche.concurence"
    _description="Concurrents"

    resultats = fields.Many2one("marche.appel")
    name=fields.Char(string="Nom du concurent")
    dossier_concurent=fields.Text(string="Dossiers fournis par le concurent")
    budget_concurent=fields.Integer(string="Budget proposé")
    rang=fields.Integer(string="Rang")

 
## classe pour l'enregistrement des types de marché ##

class type_m(models.Model):
    _name = "marche.type_m"
    _description = "Type de marché"

    name = fields.Char(string="Type du marché", required =True)
    descriptions = fields.Text(string="Description du marché")


## classes pour le resumé des marchés soumis pendant une periode donnée:dte_debut dte_fin ##


class ListeMarcheSoumis(models.TransientModel):
    _name = "liste.marche.soumis"
    _description = "Soumis marche"

    dte_debut = fields.Date(string="Date de début", required=True)
    dte_fin = fields.Date(string="Date de fin", required=True)
    liste_ids = fields.One2many("liste.marche.soumis.line", "liste_id",readonly=True)

    def afficherListe(self):

        debut = self.dte_debut
        fin = self.dte_fin

        for lis in self:
            lis.env.cr.execute("""SELECT name, structure, typ, date_depot from marche_appel 
                where state = 'S' and date_depot between %s and %s """,(debut,fin)) 
            rows = lis.env.cr.dictfetchall()  
            result =[]

            lis.liste_ids.unlink()
            for line in rows:
                result.append((0,0, {'structure_id' : line['structure'], 'intitule': line['name'], 'type_id': line['typ'], 'dte_depot' : line['date_depot']}))
            self.liste_ids = result


class ListeMarcheSoumisLine(models.TransientModel):
    _name = "liste.marche.soumis.line"
    _description = "Soumis line"

    liste_id = fields.Many2one("liste.marche.soumis", ondelete="cascade")
    structure_id = fields.Many2one("marche.structure", string="Structure")
    intitule = fields.Text(string="Intitulé")
    type_id = fields.Many2one("marche.type_m",string="Type de marché")
    dte_depot = fields.Date(string="Date de dépôt")


## classes pour le resumé des marchés obtenue pendant une periode donnée:dte_debut dte_fin ##

class ListeMarcheObtenue(models.TransientModel):
    _name = "liste.marche.obtenue"
    _description = " marche obtenue"

    dte_debut = fields.Date(string="Date de début", required=True)
    dte_fin = fields.Date(string="Date de fin", required=True)
    obtenue_ids = fields.One2many("liste.marche.obtenue.line", "obtenue_id",readonly=True)

    def ObtenueListe(self):

        debut = self.dte_debut
        fin = self.dte_fin

        for lis in self:
            lis.env.cr.execute("""SELECT name, structure, typ, budget ,dure from marche_appel  
                where state = 'O' """) 
            rows = lis.env.cr.dictfetchall()  
            result =[]

            lis.obtenue_ids.unlink()
            for line in rows:
                result.append((0,0, {'structure_id' : line['structure'], 'intitule': line['name'], 'type_id': line['typ'], 'dure' : line['dure'], 'budget' : line['budget']}))
            self.obtenue_ids = result


class ListeMarcheObtenueLine(models.TransientModel):
    _name = "liste.marche.obtenue.line"
    

    obtenue_id = fields.Many2one("liste.marche.obtenue", ondelete="cascade")
    structure_id = fields.Many2one("marche.structure", string="Structure")
    intitule = fields.Text(string="Intitulé")
    budget = fields.Integer(string="Budget")
    dure = fields.Char(string="Durée")
    type_id = fields.Many2one("marche.type_m",string="Type de marché")




