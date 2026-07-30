# Copyright (c) 2026, Nazmul Hossain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, today
from erpnext.stock.get_item_details import get_conversion_factor

class ProcurementRequisition(Document):
	def before_validate(self):
		## set Requisition No if not set by user
		if not self.requisition_no:
			self.requisition_no = self.name

		## set requested by Employee
		employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, ["name"])
		if employee:
			self.requested_by = employee

		## calculate total qty
		total_qty = 0
		for item in self.items:
			total_qty += item.qty
		self.total_quantity = total_qty

	def validate(self):
		self.set_uom_and_conversion_factor()
		self.validate_fields()

	def set_uom_and_conversion_factor(self):
		for item in self.get("items") or []:
			if not item.item_code:
				continue
			conversion_factor_dict = get_conversion_factor(item.item_code, item.uom)
			item.conversion_factor = flt(conversion_factor_dict.get("conversion_factor"))
			item.stock_qty = flt(item.qty) * flt(item.conversion_factor)

	def validate_fields(self):
		if flt(self.estimated_total_amount) < 1:
			frappe.throw("Estimated Budget must be greater than zero.")

		current_date = today()
		if self.required_date and getdate(self.required_date) < getdate(current_date):
			frappe.throw("Required Date cannot be earlier than today's date.")

		if self.total_quantity < 1:
			frappe.throw("Quantity must be greater than zero.")
			

@frappe.whitelist()
def make_request_for_quotation(source_name, target_doc=None):
	def postprocess(source, target):
		for item in target.items:
			item.schedule_date = source.required_date

	doclist = get_mapped_doc(
		"Procurement Requisition",
		source_name,
		{
			"Procurement Requisition": {
				"doctype": "Request for Quotation",
				"field_map": {
					"required_date": "schedule_date",
				},
				"validation": {
					"docstatus": ["=", 1],
				},
			},
			"Procurement Requisition Item": {
				"doctype": "Request for Quotation Item",
				"field_map": {
					"item_code": "item_code",
					"item_name": "item_name",
					"qty": "qty",
					"uom": "uom",
					"stock_uom": "stock_uom",
					"conversion_factor": "conversion_factor",
					"stock_qty": "stock_qty",
					"item_description": "description",
				},
			},
		},
		target_doc,
		postprocess,
	)

	return doclist

