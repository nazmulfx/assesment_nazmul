// Copyright (c) 2026, Nazmul Hossain and contributors
// For license information, please see license.txt

frappe.ui.form.on('Procurement Requisition', {
	refresh(frm) {
		calculate_total_amount(frm);

		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__('Request for Quotation'), function() {
				frappe.model.open_mapped_doc({
					method: "assesment_nazmul.assesment_nazmul.doctype.procurement_requisition.procurement_requisition.make_request_for_quotation",
					frm: frm,
				});
			}, __('Create'));
		}
	}
});

frappe.ui.form.on('Procurement Requisition Item', {
	item_code(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
	qty(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
	rate(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
	items_remove(frm) {
		calculate_total_amount(frm);
	}
});


function calculate_amount(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	if (row) {
		let amount = flt(row.qty) * flt(row.rate);
		frappe.model.set_value(cdt, cdn, 'amount', amount);
		calculate_total_amount(frm);
	}
}

function calculate_total_amount(frm) {
	let total = 0;
	(frm.doc.items || []).forEach(row => {
		total += flt(row.amount);
	});
	frm.set_value('estimated_total_amount', total);
}