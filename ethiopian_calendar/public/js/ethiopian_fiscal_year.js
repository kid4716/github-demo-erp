frappe.ui.form.on("Ethiopian Fiscal Year", {
    refresh(frm) {
        if (!frm.is_new() && frappe.user.has_role("System Manager")) {
            frm.add_custom_button(__("Generate 13 Pay Periods"), () => {
                frappe.confirm(
                    __(
                        "Create all missing Ethiopian Pay Periods for this fiscal year? Existing periods will not be changed."
                    ),
                    () => {
                        frappe.call({
                            method: "ethiopian_calendar.ethiopian_calendar.doctype.ethiopian_fiscal_year.ethiopian_fiscal_year.create_pay_periods",
                            args: { fiscal_year_name: frm.doc.name },
                            freeze: true,
                            freeze_message: __("Creating Ethiopian Pay Periods…"),
                            callback(r) {
                                if (r.message) {
                                    frappe.show_alert({ message: r.message.message, indicator: "green" });
                                }
                            },
                        });
                    }
                );
            });
        }
    },
});
