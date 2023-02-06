# -*- coding: utf-8 -*-
# from odoo import http


# class Galaxy(http.Controller):
#     @http.route('/galaxy/galaxy', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/galaxy/galaxy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('galaxy.listing', {
#             'root': '/galaxy/galaxy',
#             'objects': http.request.env['galaxy.galaxy'].search([]),
#         })

#     @http.route('/galaxy/galaxy/objects/<model("galaxy.galaxy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('galaxy.object', {
#             'object': obj
#         })
