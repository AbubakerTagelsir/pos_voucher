# -*- coding: utf-8 -*-
from odoo import http

# class VouchersPos(http.Controller):
#     @http.route('/vouchers_pos/vouchers_pos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vouchers_pos/vouchers_pos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vouchers_pos.listing', {
#             'root': '/vouchers_pos/vouchers_pos',
#             'objects': http.request.env['vouchers_pos.vouchers_pos'].search([]),
#         })

#     @http.route('/vouchers_pos/vouchers_pos/objects/<model("vouchers_pos.vouchers_pos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vouchers_pos.object', {
#             'object': obj
#         })