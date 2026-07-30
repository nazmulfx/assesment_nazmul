# Copyright (c) 2026, Nazmul Hossain and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: dict | None = None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:
	return [
		{
			"label": _("Requisition Number"),
			"fieldname": "requisition_no",
			"fieldtype": "Link",
			"options": "Procurement Requisition",
			"width": 180,
		},
		{
			"label": _("Requested By"),
			"fieldname": "requested_by",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 160,
		},
		{
			"label": _("Department"),
			"fieldname": "department",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("Estimated Budget"),
			"fieldname": "estimated_total_amount",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Current Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"label": _("Workflow Status"),
			"fieldname": "workflow_state",
			"fieldtype": "Link",
			"options": "Workflow State",
			"width": 140,
		},
	]


def get_data(filters: dict) -> list[dict]:
	conditions = {}
	if filters.get("department"):
		conditions["department"] = filters.get("department")

	if filters.get("status"):
		conditions["status"] = filters.get("status")

	return frappe.db.get_all(
		"Procurement Requisition",
		fields=["name as requisition_no", "requested_by", "department", "estimated_total_amount", "status", "workflow_state"],
		filters=conditions,
		order_by="creation desc",
	)
