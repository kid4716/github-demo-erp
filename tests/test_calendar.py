from datetime import date

from ethiopian_calendar.calendar import EthiopianDate, ethiopian_to_gregorian, gregorian_to_ethiopian


def test_user_supplied_calendar_mappings():
    assert ethiopian_to_gregorian(EthiopianDate(2018, 12, 7)) == date(2026, 8, 13)
    assert ethiopian_to_gregorian(EthiopianDate(2018, 11, 1)) == date(2026, 7, 8)
    assert ethiopian_to_gregorian(EthiopianDate(2018, 13, 1)) == date(2026, 9, 6)
    assert ethiopian_to_gregorian(EthiopianDate(2018, 13, 5)) == date(2026, 9, 10)
    assert ethiopian_to_gregorian(EthiopianDate(2019, 10, 30)) == date(2027, 7, 7)


def test_round_trip():
    assert gregorian_to_ethiopian(date(2026, 8, 13)) == EthiopianDate(2018, 12, 7)
