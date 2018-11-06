# -*- coding: utf-8 -*-
from odoo import http

# class PosVoucher(http.Controller):
#     @http.route('/pos_voucher/pos_voucher/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_voucher/pos_voucher/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_voucher.listing', {
#             'root': '/pos_voucher/pos_voucher',
#             'objects': http.request.env['pos_voucher.pos_voucher'].search([]),
#         })

#     @http.route('/pos_voucher/pos_voucher/objects/<model("pos_voucher.pos_voucher"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_voucher.object', {
#             'object': obj
#         })