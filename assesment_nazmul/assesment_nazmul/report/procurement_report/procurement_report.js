// Copyright (c) 2026, Nazmul Hossain and contributors
// For license information, please see license.txt

frappe.query_reports["Procurement Report"] = {
	filters: [
		{
			fieldname: "department",
			label: __("Department"),
			fieldtype: "Link",
			options: "Department",
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nDraft\nPending Approval\nApproved\nRejected\nCancelled\nOrdered",
		},
	],
	formatter: function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && (column.fieldname === "status" || column.fieldname === "workflow_state")) {
			let status_val = data[column.fieldname];
			if (!status_val) return value;

			let color = "gray";
			if (["Approved", "Ordered"].includes(status_val)) {
				color = "green";
			} else if (["Pending Approval", "Waiting For RFQ"].includes(status_val)) {
				color = "orange";
			} else if (["Rejected", "Cancelled"].includes(status_val)) {
				color = "red";
			} else if (status_val === "Draft") {
				color = "blue";
			}
			return `<span class="indicator-pill ${color}">${status_val}</span>`;
		}
		return value;
	},
};
