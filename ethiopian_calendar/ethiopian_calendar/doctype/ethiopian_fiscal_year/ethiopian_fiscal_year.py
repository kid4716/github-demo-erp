import frappe
from frappe.model.document import Document
from frappe.utils import getdate

from ethiopian_calendar.calendar import EthiopianDate, days_in_ethiopian_month, ethiopian_to_gregorian


class EthiopianFiscalYear(Document):
    def validate(self):
        self._validate_ethiopian_year()
        expected_start = ethiopian_to_gregorian(EthiopianDate(self.ethiopian_year, 11, 1))
        expected_end = ethiopian_to_gregorian(EthiopianDate(self.ethiopian_year + 1, 10, 30))
        if getdate(self.gregorian_start_date) != expected_start:
            frappe.throw(f"Gregorian start must be {expected_start.isoformat()} for this Ethiopian fiscal year.")
        if getdate(self.gregorian_end_date) != expected_end:
            frappe.throw(f"Gregorian end must be {expected_end.isoformat()} for this Ethiopian fiscal year.")
        self.ethiopian_start_date = f"01/11/{self.ethiopian_year:04d}"
        self.ethiopian_end_date = f"30/10/{self.ethiopian_year + 1:04d}"
        self.ethiopian_year_label = f"{self.ethiopian_year:04d}/{self.ethiopian_year + 1:04d} E.C."

    def _validate_ethiopian_year(self):
        if not self.ethiopian_year or self.ethiopian_year < 1:
            frappe.throw("Ethiopian Year must be a positive number.")


@frappe.whitelist()
def create_pay_periods(fiscal_year_name):
    """Create missing periods for a fiscal year, leaving existing records intact."""
    frappe.only_for("System Manager")
    fiscal_year = frappe.get_doc("Ethiopian Fiscal Year", fiscal_year_name)
    if fiscal_year.docstatus == 2:
        frappe.throw("Cannot create pay periods for a cancelled Ethiopian Fiscal Year.")

    created, existing = [], []
    # Ethiopian fiscal year runs Hamle (11) through Sene (10) of the next year.
    months = [(fiscal_year.ethiopian_year, month) for month in range(11, 14)] + [
        (fiscal_year.ethiopian_year + 1, month) for month in range(1, 11)
    ]
    for year, month in months:
        filters = {
            "company": fiscal_year.company,
            "ethiopian_year": year,
            "ethiopian_month": month,
        }
        if frappe.db.exists("Ethiopian Pay Period", filters):
            existing.append(f"{year:04d}/{month:02d}")
            continue

        start = ethiopian_to_gregorian(EthiopianDate(year, month, 1))
        end = ethiopian_to_gregorian(EthiopianDate(year, month, days_in_ethiopian_month(year, month)))
        period = frappe.get_doc(
            {
                "doctype": "Ethiopian Pay Period",
                "company": fiscal_year.company,
                "ethiopian_fiscal_year": fiscal_year.name,
                "ethiopian_year": year,
                "ethiopian_month": month,
                "gregorian_start_date": start,
                "gregorian_end_date": end,
            }
        )
        period.insert()
        created.append(period.name)

    return {
        "created": created,
        "existing": existing,
        "message": f"Created {len(created)} Ethiopian Pay Period(s); {len(existing)} already existed.",
    }
