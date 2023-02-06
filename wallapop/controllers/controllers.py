# -*- coding: utf-8 -*-
# from odoo import http


# class Wallapop(http.Controller):
#     @http.route('/wallapop/wallapop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wallapop/wallapop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wallapop.listing', {
#             'root': '/wallapop/wallapop',
#             'objects': http.request.env['wallapop.wallapop'].search([]),
#         })

#     @http.route('/wallapop/wallapop/objects/<model("wallapop.wallapop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wallapop.object', {
#             'object': obj
#         })
