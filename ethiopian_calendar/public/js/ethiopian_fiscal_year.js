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
        if (!frm.is_new() && frappe.user.has_role("HR Manager")) {
            frm.add_custom_button(__("Generate Holiday List"), () => {
                frappe.confirm(
                    __(
                        "Generate/update the Holiday List for this fiscal year? This will add fixed Ethiopian and Gregorian holidays, plus any Movable Holidays already entered for this year. Existing holidays already in the list will not be duplicated."
                    ),
                    () => {
                        frappe.call({
                            method: "ethiopian_calendar.holidays.generate_holiday_list",
                            args: { fiscal_year_name: frm.doc.name },
                            freeze: true,
                            freeze_message: __("Generating Holiday List…"),
                            callback(r) {
                                if (r.message) {
                                    frappe.show_alert({
                                        message: __("Added {0} holiday(s) to {1}", [
                                            r.message.holidays_added,
                                            r.message.holiday_list,
                                        ]),
                                        indicator: "green",
                                    });
                                    frm.reload_doc();
                                }
                            },
                        });
                    }
                );
            });
        }
    },
});
