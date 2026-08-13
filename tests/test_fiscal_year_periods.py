from datetime import date

from ethiopian_calendar.calendar import EthiopianDate, days_in_ethiopian_month, ethiopian_to_gregorian


def test_efy_2018_period_boundaries():
    fiscal_months = [(2018, month) for month in range(11, 14)] + [(2019, month) for month in range(1, 11)]
    assert len(fiscal_months) == 13
    assert fiscal_months[0] == (2018, 11)
    assert fiscal_months[-1] == (2019, 10)
    assert ethiopian_to_gregorian(EthiopianDate(2018, 11, 1)) == date(2026, 7, 8)
    assert ethiopian_to_gregorian(EthiopianDate(2018, 13, 1)) == date(2026, 9, 6)
    assert ethiopian_to_gregorian(EthiopianDate(2018, 13, days_in_ethiopian_month(2018, 13))) == date(2026, 9, 10)
    assert ethiopian_to_gregorian(EthiopianDate(2019, 10, 30)) == date(2027, 7, 7)
