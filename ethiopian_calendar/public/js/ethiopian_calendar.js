(function () {
    "use strict";

    const ETHIOPIAN_EPOCH = 1724221;

    function isEthiopianLeapYear(year) {
        return year % 4 === 3;
    }

    function daysInEthiopianMonth(year, month) {
        if (month < 1 || month > 13) {
            throw new Error("Ethiopian month must be between 1 and 13");
        }

        if (month <= 12) {
            return 30;
        }

        return isEthiopianLeapYear(year) ? 6 : 5;
    }

    function validateEthiopianDate(year, month, day) {
        if (!Number.isInteger(year) || year < 1) {
            throw new Error("Invalid Ethiopian year");
        }

        if (!Number.isInteger(month) || month < 1 || month > 13) {
            throw new Error("Invalid Ethiopian month");
        }

        const maxDay = daysInEthiopianMonth(year, month);

        if (!Number.isInteger(day) || day < 1 || day > maxDay) {
            throw new Error("Invalid Ethiopian day");
        }
    }

    function ethiopianToJdn(year, month, day) {
        validateEthiopianDate(year, month, day);

        return (
            ETHIOPIAN_EPOCH +
            365 * (year - 1) +
            Math.floor(year / 4) +
            30 * (month - 1) +
            (day - 1)
        );
    }

    function jdnToEthiopian(jdn) {
        const r = (jdn - ETHIOPIAN_EPOCH) % 1461;

        const n =
            (r % 365) +
            365 * Math.floor(r / 1460);

        const year =
            4 * Math.floor((jdn - ETHIOPIAN_EPOCH) / 1461) +
            Math.floor(r / 365) -
            Math.floor(r / 1460) +
            1;

        const month = Math.floor(n / 30) + 1;
        const day = (n % 30) + 1;

        validateEthiopianDate(year, month, day);

        return {
            year,
            month,
            day
        };
    }

    function gregorianToJdn(year, month, day) {
        const a = Math.floor((14 - month) / 12);
        const y = year + 4800 - a;
        const m = month + 12 * a - 3;

        return (
            day +
            Math.floor((153 * m + 2) / 5) +
            365 * y +
            Math.floor(y / 4) -
            Math.floor(y / 100) +
            Math.floor(y / 400) -
            32045
        );
    }

    function jdnToGregorian(jdn) {
        const a = jdn + 32044;
        const b = Math.floor((4 * a + 3) / 146097);
        const c = a - Math.floor((146097 * b) / 4);
        const d = Math.floor((4 * c + 3) / 1461);
        const e = c - Math.floor((1461 * d) / 4);
        const m = Math.floor((5 * e + 2) / 153);

        return {
            year:
                100 * b +
                d -
                4800 +
                Math.floor(m / 10),

            month:
                m +
                3 -
                12 * Math.floor(m / 10),

            day:
                e -
                Math.floor((153 * m + 2) / 5) +
                1
        };
    }

    function ethiopianToGregorian(year, month, day) {
        return jdnToGregorian(
            ethiopianToJdn(year, month, day)
        );
    }

    function gregorianToEthiopian(year, month, day) {
        return jdnToEthiopian(
            gregorianToJdn(year, month, day)
        );
    }

    function pad(value) {
        return String(value).padStart(2, "0");
    }

    function formatEthiopian(year, month, day) {
        return `${pad(day)}/${pad(month)}/${year}`;
    }

    function formatGregorian(year, month, day) {
        return `${year}-${pad(month)}-${pad(day)}`;
    }

    function parseGregorian(value) {
        if (!value) {
            return null;
        }

        const match = String(value).match(
            /^(\d{4})-(\d{1,2})-(\d{1,2})$/
        );

        if (!match) {
            return null;
        }

        return {
            year: Number(match[1]),
            month: Number(match[2]),
            day: Number(match[3])
        };
    }

    window.EthiopianCalendar = {
        ETHIOPIAN_EPOCH,

        isEthiopianLeapYear,
        daysInEthiopianMonth,
        validateEthiopianDate,

        ethiopianToJdn,
        jdnToEthiopian,

        gregorianToJdn,
        jdnToGregorian,

        ethiopianToGregorian,
        gregorianToEthiopian,

        formatEthiopian,
        formatGregorian,
        parseGregorian
    };
})();
