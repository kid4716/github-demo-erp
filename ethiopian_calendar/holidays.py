"""Generate a native Frappe HR Holiday List from Ethiopian fiscal year data.

Fixed-Ethiopian-date holidays are computed automatically every year using
the app's own calendar conversion. Movable (lunar-based) holidays must be
entered manually per fiscal year via the "Ethiopian Movable Holiday" doctype,
since they cannot be derived from the Ethiopian calendar alone.
"""
import frappe
from frappe.utils import getdate

from ethiopian_calendar.calendar import EthiopianDate, ethiopian_to_gregorian

# (month, day, name) in Ethiopian calendar terms. These always fall in the
# fiscal year's *second* Ethiopian year (the one starting at Meskerem/New Year).
FIXED_ETHIOPIAN_HOLIDAYS = [
	(1, 1, "Enkutatash (Ethiopian New Year)"),
	(1, 17, "Meskel (Finding of the True Cross)"),
	(3, 20, "Ethiopian National Unity Day"),
	(4, 29, "Genna (Ethiopian Christmas)"),
	(5, 11, "Timkat (Ethiopian Epiphany)"),
]

# (month, day) fixed on the Gregorian calendar, "month-day" format.
FIXED_GREGORIAN_HOLIDAYS = [
	("03-02", "Adwa Victory Day"),
]


def _fixed_ethiopian_holiday_dates(fiscal_year):
	"""Fixed-Ethiopian-date holidays for this fiscal year, as Gregorian dates."""
	next_year = fiscal_year.ethiopian_year + 1
	dates = []
	for month, day, name in FIXED_ETHIOPIAN_HOLIDAYS:
		greg_date = ethiopian_to_gregorian(EthiopianDate(next_year, month, day))
		dates.append({"holiday_date": greg_date, "description": name})
	return dates


def _fixed_gregorian_holiday_dates(fiscal_year):
	"""Fixed-Gregorian-date holidays that fall within this fiscal year's range."""
	start_year = getdate(fiscal_year.gregorian_start_date).year
	dates = []
	for month_day, name in FIXED_GREGORIAN_HOLIDAYS:
		for year in (start_year, start_year + 1):
			candidate = getdate(f"{year}-{month_day}")
			if getdate(fiscal_year.gregorian_start_date) <= candidate <= getdate(fiscal_year.gregorian_end_date):
				dates.append({"holiday_date": candidate, "description": name})
	return dates


def _movable_holiday_dates(fiscal_year_name):
	rows = frappe.get_all(
		"Ethiopian Movable Holiday",
		filters={"ethiopian_fiscal_year": fiscal_year_name},
		fields=["holiday_name as description", "gregorian_date as holiday_date"],
	)
	return rows


@frappe.whitelist()
def generate_holiday_list(fiscal_year_name, holiday_list_name=None):
	"""Create or update a Holiday List for the given Ethiopian Fiscal Year."""
	frappe.only_for(["System Manager", "HR Manager"])

	fiscal_year = frappe.get_doc("Ethiopian Fiscal Year", fiscal_year_name)

	all_holidays = (
		_fixed_ethiopian_holiday_dates(fiscal_year)
		+ _fixed_gregorian_holiday_dates(fiscal_year)
		+ _movable_holiday_dates(fiscal_year_name)
	)
	all_holidays.sort(key=lambda h: getdate(h["holiday_date"]))

	list_name = holiday_list_name or f"Ethiopia {fiscal_year.ethiopian_year_label}"

	if frappe.db.exists("Holiday List", list_name):
		holiday_list = frappe.get_doc("Holiday List", list_name)
	else:
		holiday_list = frappe.new_doc("Holiday List")
		holiday_list.holiday_list_name = list_name
		holiday_list.from_date = fiscal_year.gregorian_start_date
		holiday_list.to_date = fiscal_year.gregorian_end_date

	existing_dates = {getdate(row.holiday_date) for row in holiday_list.holidays}
	added = 0
	skipped_no_date = 0

	for h in all_holidays:
		if not h.get("holiday_date"):
			skipped_no_date += 1
			continue
		date = getdate(h["holiday_date"])
		if date not in existing_dates:
			holiday_list.append(
				"holidays", {"holiday_date": date, "description": h["description"], "weekly_off": 0}
			)
			existing_dates.add(date)
			added += 1

	holiday_list.save()
	fiscal_year.db_set("holiday_list", holiday_list.name)

	return {
		"holiday_list": holiday_list.name,
		"holidays_added": added,
		"skipped_missing_date": skipped_no_date,
		"note": "Add movable holidays (Eid, Mawlid, Good Friday, Easter) via "
		"Ethiopian Movable Holiday before running this, so they're included.",
	}
