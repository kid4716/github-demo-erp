"""Fixed 30-day Ethiopian payroll treatment for Frappe HR Salary Slips.

This override deliberately leaves tax, pension, loan and other deductions to
the standard HRMS flow.  It only provides the correct payroll basis before the
standard component calculations run.
"""

from frappe import _
import frappe
from frappe.utils import date_diff, flt, getdate
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip


class EthiopianSalarySlip(SalarySlip):
    def get_working_days_details(self, lwp=None, for_preview=0, lwp_days_corrected=None):
        super().get_working_days_details(
            lwp=lwp,
            for_preview=for_preview,
            lwp_days_corrected=lwp_days_corrected,
        )

        period = self._ethiopian_pay_period()
        if not period:
            return
        if not period.is_payable:
            frappe.throw(_("Salary Slip cannot be created for an unpaid Ethiopian Pagume period."))
        if period.paid_days != 30:
            frappe.throw(_("A payable Ethiopian Pay Period must have exactly 30 paid days."))

        # A normal Ethiopian month corresponds to exactly 30 Gregorian dates.
        # Do not deduct public holidays: paid holidays remain part of the fixed
        # 30-day salary basis.  LWP/absence and joining/relieving boundaries
        # still reduce payment days.
        eligible_days = self._eligible_calendar_days()
        self.total_working_days = 30
        self.payment_days = max(
            0,
            flt(eligible_days) - flt(self.leave_without_pay) - flt(self.absent_days),
        )
        self.ethiopian_pay_period = period.name
        self.ethiopian_period_label = period.ethiopian_period_label
        self.ethiopian_salary_denominator = 30

    def _ethiopian_pay_period(self):
        period_name = self.get("ethiopian_pay_period")
        if not period_name and self.payroll_entry:
            period_name = frappe.db.get_value("Payroll Entry", self.payroll_entry, "ethiopian_pay_period")
        if not period_name:
            return None

        period = frappe.get_cached_doc("Ethiopian Pay Period", period_name)
        if getdate(self.start_date) != getdate(period.gregorian_start_date) or getdate(self.end_date) != getdate(
            period.gregorian_end_date
        ):
            frappe.throw(
                _("Salary Slip dates must match Ethiopian Pay Period {0}.").format(period.name)
            )
        return period

    def _eligible_calendar_days(self):
        """Days the employee is employed within this 30-day Ethiopian month."""
        start = max(getdate(self.start_date), getdate(self.actual_start_date))
        end = min(getdate(self.end_date), getdate(self.actual_end_date))
        if end < start:
            return 0
        return date_diff(end, start) + 1
