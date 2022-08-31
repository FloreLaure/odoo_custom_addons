from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError



class appel(models.Model):
    _name = "marche.appel"
    _description = "Enregistrement des appels d'offre"

    name= fields.Text(string="Intitulé du marché", required =True)
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
    dossier = fields.Many2many("marche.dossier", string="dossier à fournir", required =True)
    state = fields.Selection([('soumis', 'Soumis'),('soumetre','Soumetre')],string="Etat")

    def action_soumis(self):
        self.state = 'soumis'

    def action_soumetre(self):
        self.state = 'soumetre'



class dossier(models.Model):
    _name = "marche.dossier"
    _description = "dossier à fournir"

    dossier = fields.Char()



class structure(models.Model):
    _name = "marche.structure"
    _description = "Structure demandeuse"

    name= fields.Char(string="Nom de la structure", required =True)
    phone = fields.Integer(string="Telephone")
    mail = fields.Char(string="E-Mail")



class type_m(models.Model):
    _name = "marche.type_m"
    _description = "Type de marché"

    name = fields.Char(string="Type du marché", required =True)
    descriptions = fields.Text(string="Description du marché")



class ListeMarcheSoumis(models.TransientModel):
    _name = "marche.ListeMarcheSoumis"

    dte_debut = fields.Date(string= "Date de début", required=True)
    dte_fin = fields.Date(string="Date de fin", required=True)
    liste_ids = fields.One2many("marche.ListeMarcheSoumisLine", "liste_id",readonly=True)


    
    def afficherListe(self):

        debut = self.dte_debut
        fin = self.dte_fin

           
            lis.env.cr.execute("""SELECT name, structure, typ, date_depot from marche_appel 
                where state = 'soumis' and date_depot between %s and %s """, (debut, fin)) 
            rows = lis.env.cr.dictfetchall()  
            result =[]

            lis.liste_ids.unlink()
            for line in rows:
                result.append((0,0 {'structure_id' : structure, 'intitule': name, 'type_id': typ, 'dte_depot' : date_depot}))
            self.liste_ids = result




class ListeMarcheSoumisLine(models.TransientModel):
    _name = "marche.ListeMarcheSoumisLine"



    liste_id = fields.Many2one("marche.ListeMarcheSoumis",ondelete='cascade')
    structure_id = fields.Many2one("marche.structure", string="Structure")
    intitule = fields.Char("marche.appel", string="Intitulé")
    type_id = fields.Char(string="Type de marché")
    dte_depot = fields.Date(string="Date de dépôt")





