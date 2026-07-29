# Copyright (c) 2026, Nazmul Hossain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ProcurementRequisition(Document):
	def before_validate(self):
		## set Requisition No if not set by user
		if not self.requisition_no:
			self.requisition_no = self.name

		## set requested by Employee
		employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, ["name"])
		if employee:
			self.requested_by = employee


@frappe.whitelist()
def make_request_for_quotation(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Procurement Requisition",
		source_name,
		{
			"Procurement Requisition": {
				"doctype": "Request for Quotation",
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
					"item_description": "description",
				},
			},
		},
		target_doc,
	)

	return doclist

