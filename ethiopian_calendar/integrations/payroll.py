"""Payroll Entry integration.

The linked Ethiopian Pay Period is the source of truth for the payroll range.
Its Gregorian dates are copied to Frappe's native date fields before salary
slips or accounting entries are generated.
"""

import frappe
from frappe import _


def apply_ethiopian_pay_period(doc, method=None):
    if not doc.get("ethiopian_pay_period"):
        return

    period = frappe.get_doc("Ethiopian Pay Period", doc.ethiopian_pay_period)
    if period.company != doc.company:
        frappe.throw(_("Ethiopian Pay Period company must match Payroll Entry company."))
    if not period.is_payable:
        frappe.throw(
            _("{0} is an unpaid Ethiopian period. Payroll Entry cannot be created for it.").format(
                period.name
            )
        )

    doc.start_date = period.gregorian_start_date
    doc.end_date = period.gregorian_end_date
    doc.ethiopian_period_label = period.ethiopian_period_label
    doc.ethiopian_salary_denominator = period.paid_days
