// Copyright (c) 2026, Nazmul Hossain and contributors
// For license information, please see license.txt

frappe.ui.form.on('Procurement Requisition', {
	refresh(frm) {
		// your code here
	}
})

frappe.ui.form.on('Procurement Requisition Item', {
	refresh(frm) {
		// your code here
	},
    item_code(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn)
    },
    qty(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
    rate(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
	item_code(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
	items_remove(frm) {
		calculate_total_amount(frm);
	}
})


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