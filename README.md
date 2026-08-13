# Ethiopian Calendar for Frappe

This custom app keeps Frappe's native dates Gregorian, while adding Ethiopian fiscal periods and Ethiopian payroll periods.

## Fiscal-year rule configured for the first period

| Ethiopian | Gregorian |
|---|---|
| 01/11/2018 (Hamle 1, 2018) | 2026-07-08 |
| 01/13/2018 (Pagume 1, 2018) | 2026-09-06 |
| 05/13/2018 (Pagume 5, 2018) | 2026-09-10 |
| 30/10/2019 (Sene 30, 2019) | 2027-07-07 |

Pagume 2018 is a five-day period and is marked unpaid by default. A sixth Pagume day is accepted only for Ethiopian leap years.

## Install

From a Frappe bench (with `frappe` and `hrms` installed):

```bash
bench get-app /path/to/ethiopian_calendar
bench --site your-site install-app ethiopian_calendar
bench --site your-site migrate
```

Then create an **Ethiopian Fiscal Year** for `2018` and click **Generate 13 Pay Periods**. The action creates the fiscal-year sequence from Hamle through Sene, including unpaid Pagume, and never changes a period that already exists. Link a period on **Payroll Entry**; its native Start Date and End Date are populated with the matching Gregorian dates.

## Safety model

* Do **not** change core `Date` fields to Ethiopian dates.
* General Ledger, Payroll Entry, Salary Slip, Fiscal Year and Accounting Period continue to store Gregorian dates.
* Ethiopian fields are business labels and controlled mappings to Gregorian dates.
* Payroll blocks an unpaid Pagume period; it does not create a zero-value payroll accidentally.
* For a payable Ethiopian period, Salary Slip always uses `total_working_days = 30`.
  Payment days are `employed days in period - LWP - absences`; paid holidays do not
  lower the denominator. Standard deductions run after that prorated salary.

## Next increments

1. Add Ethiopian date display/input widgets and print formats.
2. Add Ethiopian budget distribution and budget-control extensions.
4. Add Ethiopian display fields to accounting, HR and stock documents.
