# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Example(http.Controller):

    # @http.route('/pos/get_info', type='json', auth='public',csrf=False)
    # def get_pos_info(self):
    #     pos_ids =  request.env['pos_voucher.pos_voucher'].sudo().search([]).ids
    #     for id in pos_ids:
    #         print(id)
    #     return True

    @http.route('/pos/get_info', type='json', auth='public',csrf=False)
    def get_pos_info(self, *args, **kwargs):
        pos_id = request.params["pos_id"]
        pos_data =  request.env['pos_voucher.pos_voucher'].sudo().search([('id','=',pos_id)]).read(['name','phonenumber','stock','balance'])
        return pos_data

    @http.route('/pos/purchase_voucher', type='json', auth='public',csrf=False)
    def purchase_vouchers(self, *args, **kwargs):
        purchase_proces =  request.env['stock.line'].sudo().create({
            'company_id': request.params["company_name"],
            'card_id': request.params["card_value"],
            'qty': request.params["qty"],
            })
        print(purchase_proces)
        return purchase_proces

    @http.route('/pos/sale_voucher', type='json', auth='public',csrf=False)
    def sale_vouchers(self, *args, **kwargs):
        sale_proces =  request.env['stock.line'].sudo().create({
            'company_id': request.params["company_name"],
            'card_id': request.params["card_value"],
            'qty': request.params["qty"],
            })
        print(sale_proces)
        return sale__proces

    #     @http.route('/pos/purchase_balance', type='json', auth='public',csrf=False)
    # def purchase_balance(self, *args, **kwargs):
    #     purchase_proces =  request.env['balance.value']balance.value.sudo().create({
    #         'company_id': request.params["company_name"],
    #         'card_id': request.params["card_value"],
    #         'qty': request.params["qty"],
    #         })
    #     print(purchase_proces)
    #     return purchase_proces


    


    # @http.route('/example/detail', type='http', auth='public', website=True)
    # def navigate_to_detail_page(self):
    #     # This will get all company details (in case of multicompany this are multiple records)
    #     companies = http.request.env['res.company'].sudo().search([])
    #     return http.request.render('create_webpage_demo.detail_page', {
    #       # pass company details to the webpage in a variable
    #       'companies': companies})


