app_name = "ethiopian_calendar"
app_title = "Ethiopian Calendar"
app_publisher = "Your Company"
app_description = "Ethiopian fiscal periods and payroll controls"
app_email = "it@example.com"
app_license = "MIT"

fixtures = ["Custom Field"]

doc_events = {
    "Payroll Entry": {
        "validate": "ethiopian_calendar.integrations.payroll.apply_ethiopian_pay_period",
    }
}

override_doctype_class = {
    "Salary Slip": "ethiopian_calendar.overrides.salary_slip.EthiopianSalarySlip",
}

doctype_js = {
    "Ethiopian Fiscal Year": "public/js/ethiopian_fiscal_year.js",
}
