from odoo import models, fields, api


# class pos_voucher(models.TransientModel):
# 	_name = 'pos_voucher.test'
# 	name = fields.Char()	


class POSVoucher(models.Model):
	_name = 'pos_voucher.pos_voucher'	
	name = fields.Char()
	stock = fields.Float(compute="_get_stock_count")
	balance = fields.Float(compute="_get_transactions_balance")
	phonenumber = fields.Char()
	stock_lines = fields.One2many('stock.line', 'pos_id', "Lines")
	trans_history = fields.One2many('pos.trans', 'pos_id')
	stock_history= fields.One2many('stock.line','pos_id')
			

	def test_btn(self):
	    comp_obj = self.env['company.company']
	    c = comp_obj.create({})
	    c.write({'name': self.name + ": "+str(c.id)})
	    comp_list = comp_obj.search([])
	    for c in comp_list:
	        print(c.name)
	    return 1
	company = fields.One2many('stock.value','pos_id')
	company_balance = fields.One2many('balance.value','pos_id')
	

	@api.multi
	def update_balance(self):
		view_id = self.env.ref('pos_voucher.balanceTransition_form').id
		return {
			'name':'update balance',
			'view_type':'form',
			'view_mode':'form',
			'res_model':'pos.trans',
			'view_id':view_id,
			'type':'ir.actions.act_window',
			'target':'new'}
	    
	@api.multi
	def update_stock(self):
		view_id = self.env.ref('pos_voucher.stockline_form').id
		return {
            	'name':'update Stock',
				'view_type':'form',
				'view_mode':'form',
				'views':[(view_id,'form')],
				'res_model':'stock.line',
				'view_id': view_id,
				'model':'ir.actions.act_window',
				'type':'ir.actions.act_window',
				'target':'new'
			}

	# @api.multi
	# def confirm(self):
	# 	self.ensure_one()
    #     pass


	# @api.multi
	# def confirm1(self):
	# 	self.ensure_one()
    #     pass


		
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
 
	# def update_stock(self):7
	# 	company_obj= self.env['company.company']
	# 	company_list=company_obj.search([])

	# 	card_obj= self.env['card.card']
	# 	card_list=card_obj.search([])

	# 	# amount

	# 	return 1
	# def update_balance(self):
	# 	return 1
    
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

	@api.onchange('stock_lines')
	def get_company_stock_trancation(self):
		comp = self.env['company.company'].search([])
		res = {}
		for p in comp:
			total_value = 0
			for line in self.stock_history:
				if line.card_trans_type  == 'in' and line.company_id.id == p.id:
					total_value += line.qty
				elif line.card_trans_type == 'out' and line.company_id.id == p.id:
					total_value -= line.qty
			res[p.id] = total_value
		print(res)
		for b in self.company:
			b.stock = res[b.company_id.id]

	@api.onchange('trans_history')
	def get_company_balance(self):
		comp = self.env['company.company'].search([])
		res = {}
		for p in comp:
			total_value = 0
			for line in self.trans_history:
				if line.trans_type == 'in' and line.company_id.id == p.id:
					total_value += line.qty
				elif line.trans_type == 'out' and line.company_id.id == p.id:
					total_value -= line.qty
			res[p.id] = total_value
		print(res)
		for b in self.company_balance:
			b.balance = res[b.company_id.id]

	# @api.onchange('stock_lines','company')
	# def _get_company_stock(self):
	# 	companies = set()
	# 	for record in self:
	# 		companies.add(record.stock_lines.company_id.name)
		
	# 	# for p in self.stock_lines:
	# 	# 	if p.company_id not in companies:
	# 	# 		companies.append(p.company_id)

	# 	comp_balance = []
	# 	for c in companies:
	# 		comp_total = 
	# 		for l in self.stock_lines:
	# 			if l.company_id == c:
	# 				comp_total+= l.qty * l.card_id.value

	# 		comp_balance.append(comp_total)
	# 	return comp_balance
	# def get_stock_details(self):
	# 	comp = self.env['company.company'].search([])
	# 	for c in comp:
	# 		qty * sl.card_id.value
	# 		values[c.id] = comp_total
	# 	for line in self.company:
	                       

class Card(models.Model):
	_name = 'card.card'
	name = fields.Char()
	comp_name = fields.Many2one('company.company', "Manufacturer")
	value = fields.Integer()


class Company(models.Model):
	_name = 'company.company'
	name = fields.Char()
	imag = fields.Binary()
	stock_lines = fields.One2many('stock.line', 'company_id')

class StockValue(models.Model):
	_name = 'stock.value'
	pos_id = fields.Many2one('pos_voucher.pos_voucher')
	company_id = fields.Many2one('company.company')
	stock = fields.Float()	

class BalanceValue(models.Model):
	_name = 'balance.value'
	pos_id = fields.Many2one('pos_voucher.pos_voucher')
	company_id = fields.Many2one('company.company')
	balance = fields.Float()		

class StockLine(models.Model):
	_name = 'stock.line'
	card_id = fields.Many2one('card.card')
	qty = fields.Integer("Quantity")
	# type_of_interaction = fields
	pos_id = fields.Many2one('pos_voucher.pos_voucher')
	company_id = fields.Many2one(related='card_id.comp_name')
	card_trans_type = fields.Selection([('in', "IN"), ('out', "OUT")], default='out', string="Transaction Type")

class Transaction(models.Model):
	_name = 'pos.trans'
	trans_type = fields.Selection([('in', "IN"), ('out', "OUT")], default='out', string="Transaction Type")
	pos_id = fields.Many2one('pos_voucher.pos_voucher', "POS")
	qty = fields.Integer("Quantity")
	company_id = fields.Many2one('company.company', "Company")
