"""Gregorian <-> Ethiopian calendar conversion and validation.

Frappe stores ``Date`` values as Gregorian ISO dates.  This module is the only
place that converts user-facing Ethiopian calendar values to those dates.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


# Julian day number for 1 Meskerem 1, using the integer JDN convention.
# This is deliberately verified against the business baseline:
# 07/12/2018 Ethiopian = 2026-08-13 Gregorian.
ETHIOPIAN_EPOCH = 1_724_221


@dataclass(frozen=True)
class EthiopianDate:
    year: int
    month: int
    day: int

    def validate(self) -> None:
        if self.year < 1:
            raise ValueError("Ethiopian year must be greater than zero")
        if not 1 <= self.month <= 13:
            raise ValueError("Ethiopian month must be between 1 and 13")
        if not 1 <= self.day <= days_in_ethiopian_month(self.year, self.month):
            raise ValueError("Invalid Ethiopian day for this month and year")

    def as_text(self) -> str:
        return f"{self.day:02d}/{self.month:02d}/{self.year:04d}"


def is_ethiopian_leap_year(year: int) -> bool:
    """Return whether Pagume has six days in *year*."""
    return year % 4 == 3


def days_in_ethiopian_month(year: int, month: int) -> int:
    if not 1 <= month <= 13:
        raise ValueError("Ethiopian month must be between 1 and 13")
    if month <= 12:
        return 30
    return 6 if is_ethiopian_leap_year(year) else 5


def ethiopian_to_jdn(value: EthiopianDate) -> int:
    value.validate()
    return (
        ETHIOPIAN_EPOCH
        + 365 * (value.year - 1)
        + value.year // 4
        + 30 * (value.month - 1)
        + (value.day - 1)
    )


def jdn_to_ethiopian(jdn: int) -> EthiopianDate:
    r = (jdn - ETHIOPIAN_EPOCH) % 1_461
    n = (r % 365) + 365 * (r // 1_460)
    year = 4 * ((jdn - ETHIOPIAN_EPOCH) // 1_461) + (r // 365) - (r // 1_460) + 1
    month = n // 30 + 1
    day = n % 30 + 1
    result = EthiopianDate(year, month, day)
    result.validate()
    return result


def gregorian_to_jdn(value: date) -> int:
    a = (14 - value.month) // 12
    y = value.year + 4_800 - a
    m = value.month + 12 * a - 3
    return value.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32_045


def jdn_to_gregorian(jdn: int) -> date:
    a = jdn + 32_044
    b = (4 * a + 3) // 146_097
    c = a - (146_097 * b) // 4
    d = (4 * c + 3) // 1_461
    e = c - (1_461 * d) // 4
    m = (5 * e + 2) // 153
    return date(100 * b + d - 4_800 + m // 10, m + 3 - 12 * (m // 10), e - (153 * m + 2) // 5 + 1)


def ethiopian_to_gregorian(value: EthiopianDate) -> date:
    return jdn_to_gregorian(ethiopian_to_jdn(value))


def gregorian_to_ethiopian(value: date) -> EthiopianDate:
    return jdn_to_ethiopian(gregorian_to_jdn(value))
