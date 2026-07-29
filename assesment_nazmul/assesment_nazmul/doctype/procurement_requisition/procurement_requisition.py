# Copyright (c) 2026, Nazmul Hossain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProcurementRequisition(Document):
	def before_validate(self):
		## set Requisition No if not set by user
		if not self.requisition_no:
			self.requisition_no = self.name

		## set requested by Employee
		employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, ["name"])
		if employee:
			self.requested_by = employee
			
			
