# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


#PLAYER STUFF
class player(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    _description = 'los jugadores'

    nickname = fields.Char(String = "nickname", required = True)
    name = fields.Char(String = "name", required = True)
    lastname = fields.Char(String = "lastname", required = True)
    password = fields.Char(String = 'contrasenya', required = True)
    nivel = fields.Integer(default = 1)
    exp = fields.Float(default = 0.1)
    avatar = fields.Image(max_width = 250, max_height = 250) 
    faction = fields.Many2one('galaxy.faction')
    planet = fields.Many2one('galaxy.planet')
    recursototales = fields.Integer(related='planet.recursos')
    ships = fields.Integer(related='planet.naves')
    troops = fields.Integer(related='planet.tropas')
    is_player = fields.Boolean()  


#FACTION STUFF
class faction(models.Model):
    _name = 'galaxy.faction'
    _description = 'las facciones'

    name = fields.Char(Required = True)
    description = fields.Char(String = "history")
    picture = fields.Image(max_width = 500, max_height = 500)

#BUILDINGs AND PLANETs STUFF

class planet(models.Model):
    _name = 'galaxy.planet'
    _description = 'las planeta'

    name = fields.Char(Required = True)
    description = fields.Char()
    picture = fields.Image(max_width = 500, max_height = 500)
    tropas = fields.Integer(default=0)
    naves = fields.Integer(default=0)
    casas = fields.Integer(default = 1)
    cuarteles = fields.Integer(default=0)
    estacionespacial = fields.Integer(default=0)
    recursos = fields.Integer(default = 100)
    fabricas = fields.Integer(default = 1)
    building = fields.One2many('galaxy.building','planet')
    building_available = fields.Many2many('galaxy.building_type', compute='_get_buildings_available')
    population = fields.Integer(default = 0)
    populationtotal = fields.Integer(default = 20)

    @api.constrains('population')
    def population_check(self):
        for planet in self:
            if planet.population > planet.populationtotal:
                raise ValidationError("La poblacion disponible no puede ser mas grande que la poblacion total")

    def _get_buildings_available(self):
        for p in self:
            p.building_available = self.env['galaxy.building_type'].search([])

    @api.model
    def produce(self): # ORM CRON
        self.search([]).produce_resource()

    def produce_resource(self):
        for planet in self:
            resource = planet.recursos + 10 * planet.fabricas

        planet.write({
            "recursos":resource
        })    

    def troopcreate(self):
        for planet in self:

            if planet.cuarteles > 0:
                if planet.recursos >= 15 or planet.populationtotal <= planet.population:
                    planet.tropas = planet.tropas + 1
                    planet.recursos = planet.recursos - 15
                    planet.population = planet.population + 2
                else:
                    raise ValidationError("Fondos Insuficientes o La poblacion esta a tope")
            else:
                raise ValidationError("No tienes cuarteles")        

    def navescreate(self):
        for planet in self:
            if planet.estacionespacial > 0:
                if planet.recursos >= 15 or planet.populationtotal <= planet.population + 2:
                    planet.tropas = planet.tropas + 1
                    planet.recursos = planet.recursos - 15
                    planet.population = planet.population + 2
                else:
                    raise ValidationError("Fondos Insuficientes o La poblacion esta a tope")
            else:
                raise ValidationError("no tienes una estacion espacial")

                
class building(models.Model):
    _name = 'galaxy.building'
    _description = 'las estructuras'

    name = fields.Char()
    description = fields.Char()
    picture = fields.Image()
    population = fields.Integer()
    precio = fields.Integer()
    tipobuild = fields.Selection([('1','recursos'),('2','militar'),('3','estacion espacial'),('4','comun')])
    planet = fields.Many2one('galaxy.planet', ondelete="cascade")

class building_type(models.Model):
    _name = 'galaxy.building_type'
    _description = 'Building type'    

    name = fields.Char()
    description = fields.Char()
    picture = fields.Image(max_width = 500, max_height = 500)
    pop = fields.Integer()
    precio = fields.Integer()
    tipo = fields.Selection([('1','recursos'),('2','militar'),('3','estacion espacial'),('4','comun')])

    def build(self):  
        for b in self:
            planet_id = self.env['galaxy.planet'].browse(self.env.context['ctx_planet'])[0]
            if planet_id.recursos >= b.precio:
                self.env['galaxy.building'].create({
                    "planet": planet_id.id,
                    "name": b.name,
                    "description": b.description,
                    "picture": b.picture,
                    "population": b.pop,
                    "precio": b.precio,
                    "tipobuild":b.tipo
                })

                planet_id.populationtotal += b.pop
                planet_id.recursos -= b.precio

                if b.tipo == '1':
                    fabricatotal = planet_id.fabricas + 1
                    planet_id.write({
                        "fabricas":fabricatotal
                    })
                if b.tipo == '2':
                    cuartelestotal = planet_id.cuarteles + 1
                    planet_id.write({
                        "cuarteles" : cuartelestotal
                    })
                if b.tipo == '3':
                    estaciones = planet_id.estacionespacial +1
                    planet_id.write({
                        "estacionespacial" : estaciones
                    })                    
                if b.tipo == '4':
                    casastotal = planet_id.casas + 1
                    planet_id.write({
                        "casas" : casastotal
                    })

            else:
                raise ValidationError("Fondos Insuficientes")


#Wizards

class battle(models.Model):
    _name = 'galaxy.battle'
    _description = 'Battle'

    playerdefence = fields.Many2one('res.partner')
    defenceplanet = fields.Many2one('galaxy.planet', compute = 'get_planet')
    playerattack = fields.Many2one('res.partner')

    def get_planet(self):
        for p in self:
            p.defenceplanet = self.env['galaxy.planet'].search(['planet','=','p.playerdefence.planet'])
            print(p.defenceplanet) 

    @api.constrains('sameplayer')
    def player_check(self):
        for p in self:
            if p.playerattack.name == p.playerdefence.name:
                raise ValidationError('El jugador atacante tiene que ser distinto al jugador defensivo')