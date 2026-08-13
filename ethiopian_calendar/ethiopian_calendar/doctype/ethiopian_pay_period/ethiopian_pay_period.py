import frappe
from frappe.model.document import Document
from frappe.utils import getdate

from ethiopian_calendar.calendar import EthiopianDate, ethiopian_to_gregorian, days_in_ethiopian_month


class EthiopianPayPeriod(Document):
    def validate(self):
        self._validate_period()
        start = EthiopianDate(self.ethiopian_year, self.ethiopian_month, 1)
        end = EthiopianDate(
            self.ethiopian_year,
            self.ethiopian_month,
            days_in_ethiopian_month(self.ethiopian_year, self.ethiopian_month),
        )
        expected_start, expected_end = ethiopian_to_gregorian(start), ethiopian_to_gregorian(end)
        if getdate(self.gregorian_start_date) != expected_start or getdate(self.gregorian_end_date) != expected_end:
            frappe.throw(
                f"Gregorian dates must be {expected_start.isoformat()} to {expected_end.isoformat()} for this Ethiopian period."
            )
        self.ethiopian_start_date = start.as_text()
        self.ethiopian_end_date = end.as_text()
        self.ethiopian_period_label = f"{self.ethiopian_year:04d}/{self.ethiopian_month:02d}"
        self.paid_days = 0 if self.ethiopian_month == 13 else 30
        self.is_payable = 0 if self.ethiopian_month == 13 else 1

    def _validate_period(self):
        if not self.ethiopian_year or self.ethiopian_year < 1:
            frappe.throw("Ethiopian Year must be a positive number.")
        if self.ethiopian_month not in range(1, 14):
            frappe.throw("Ethiopian Month must be between 1 and 13.")
