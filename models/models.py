# -*- coding: utf-8 -*-

from odoo import models, fields, api

class pos_voucher(models.TransientModel):
	_name = 'pos_voucher.test'

	name = fields.Char()	


class pos_voucher(models.Model):
	_name = 'pos_voucher.pos_voucher'	
	name = fields.Char()
	stock = fields.Float(compute="_get_stock_count")
	balance = fields.Float(compute="_get_transactions_balance")
	phonenumber = fields.Char()
	stock_lines = fields.One2many('stock.line', 'pos_id', "Lines")
	trans_history = fields.One2many('pos.trans', 'pos_id')
	company = fields.One2many('stock.value','pos_id')




	@api.onchange('stock_lines')
	def _get_stock_count(self):
		for p in self:
			total_value = 0
			for line in p.stock_lines:
				total_value += line.qty * line.card_id.value
			p.stock = total_value

	@api.onchange('trans_history')
	def _get_transactions_balance(self):
		for p in self:
			total_value = 0
			for line in p.trans_history:
				if line.trans_type == 'in':
					total_value += line.qty
				else:
					total_value -= line.qty
			p.balance = total_value


	@api.onchange('stock_lines')
	def get_company_stock(self):
		comp = self.env['company.company'].search([])
		values = {}
		for c in comp:
			comp_total = 0
			for sl in self.stock_lines:
				if sl.company_id.id == c.id:
					comp_total += sl.qty * sl.card_id.value
			values[c.id] = comp_total
		for line in self.company:
			line.stock = values[line.company_id.id]


	# def get_stock_details(self):
	# 	comp = self.env['company.company'].search([])
	# 	for c in comp:
	# 		qty * sl.card_id.value
	# 		values[c.id] = comp_total
	# 	for line in self.company:



			




		                       

class card(models.Model):
	_name = 'card.card'
	name = fields.Char()
	comp_name = fields.Many2one('company.company', "Manufacturer")
	value = fields.Integer()


class company(models.Model):
	_name = 'company.company'
	name = fields.Char()
	imag = fields.Binary()
	stock_lines = fields.One2many('stock.line', 'company_id')
	

	
	

class StockValue(models.Model):
	_name = 'stock.value'
	pos_id = fields.Many2one('pos_voucher.pos_voucher')
	company_id = fields.Many2one('company.company')
	stock = fields.Float()	


	

class StockLine(models.Model):
	_name = 'stock.line'
	card_id = fields.Many2one('card.card')
	qty = fields.Integer("Quantity")
	pos_id = fields.Many2one('pos_voucher.pos_voucher')
	company_id = fields.Many2one(related='card_id.comp_name')


class Transaction(models.Model):
	_name = 'pos.trans'
	trans_type = fields.Selection([('in', "IN"), ('out', "OUT")], default='out', string="Transaction Type")
	pos_id = fields.Many2one('pos_voucher.pos_voucher', "POS")
	qty = fields.Integer("Quantity")

