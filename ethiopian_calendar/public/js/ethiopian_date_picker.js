(function () {
    "use strict";

    if (!window.EthiopianCalendar) {
        console.error("EthiopianCalendar is not loaded.");
        return;
    }

    const EC = window.EthiopianCalendar;

    const MONTHS = [
        "Meskerem",
        "Tikimt",
        "Hidar",
        "Tahsas",
        "Tir",
        "Yekatit",
        "Megabit",
        "Miyazya",
        "Ginbot",
        "Sene",
        "Hamle",
        "Nehase",
        "Pagume"
    ];

    const WEEKDAYS = [
        "Sun",
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat"
    ];

    let picker = null;

    function getTodayEthiopian() {
        const today = frappe.datetime.now_date();
        const parts = today.split("-");

        return EC.gregorianToEthiopian(
            Number(parts[0]),
            Number(parts[1]),
            Number(parts[2])
        );
    }

    function getFieldValue(field) {
        return field.get_value ? field.get_value() : "";
    }

    function getInitialDate(field) {
        const value = getFieldValue(field);

        if (value) {
            const gregorian = EC.parseGregorian(value);

            if (gregorian) {
                return EC.gregorianToEthiopian(
                    gregorian.year,
                    gregorian.month,
                    gregorian.day
                );
            }
        }

        return getTodayEthiopian();
    }

    function createPicker() {
        const element = document.createElement("div");

        element.className = "ethiopian-date-picker";

        element.innerHTML = `
            <div class="ec-header">

                <button type="button" class="ec-nav ec-prev-year">
                    «
                </button>

                <button type="button" class="ec-nav ec-prev-month">
                    ‹
                </button>

                <div class="ec-title">

                    <select class="ec-month"></select>

                    <input
                        type="number"
                        class="ec-year"
                        min="1"
                    >

                </div>

                <button type="button" class="ec-nav ec-next-month">
                    ›
                </button>

                <button type="button" class="ec-nav ec-next-year">
                    »
                </button>

            </div>

            <div class="ec-weekdays"></div>

            <div class="ec-days"></div>

            <div class="ec-footer">

                <button type="button" class="ec-today">
                    Today
                </button>

                <button type="button" class="ec-clear">
                    Clear
                </button>

            </div>
        `;

        document.body.appendChild(element);

        const monthSelect =
            element.querySelector(".ec-month");

        MONTHS.forEach((month, index) => {
            const option =
                document.createElement("option");

            option.value = index + 1;
            option.textContent = month;

            monthSelect.appendChild(option);
        });

        const weekdays =
            element.querySelector(".ec-weekdays");

        WEEKDAYS.forEach(day => {
            const item =
                document.createElement("div");

            item.className = "ec-weekday";
            item.textContent = day;

            weekdays.appendChild(item);
        });

        return element;
    }

    function getWeekday(year, month, day) {
        const gregorian =
            EC.ethiopianToGregorian(
                year,
                month,
                day
            );

        const date = new Date(
            gregorian.year,
            gregorian.month - 1,
            gregorian.day
        );

        return date.getDay();
    }

    function render() {
        if (!picker) {
            return;
        }

        const element = picker.element;
        const state = picker.state;

        element.querySelector(".ec-month").value =
            state.month;

        element.querySelector(".ec-year").value =
            state.year;

        const daysContainer =
            element.querySelector(".ec-days");

        daysContainer.innerHTML = "";

        const firstWeekday =
            getWeekday(
                state.year,
                state.month,
                1
            );

        const numberOfDays =
            EC.daysInEthiopianMonth(
                state.year,
                state.month
            );

        for (
            let i = 0;
            i < firstWeekday;
            i++
        ) {
            const empty =
                document.createElement("div");

            empty.className =
                "ec-day ec-empty";

            daysContainer.appendChild(empty);
        }

        for (
            let day = 1;
            day <= numberOfDays;
            day++
        ) {
            const button =
                document.createElement("button");

            button.type = "button";
            button.className = "ec-day";
            button.textContent = day;

            if (
                state.selected &&
                state.selected.year === state.year &&
                state.selected.month === state.month &&
                state.selected.day === day
            ) {
                button.classList.add("ec-selected");
            }

            const today =
                getTodayEthiopian();

            if (
                today.year === state.year &&
                today.month === state.month &&
                today.day === day
            ) {
                button.classList.add("ec-today-date");
            }

            button.addEventListener(
                "click",
                function (event) {
                    event.stopPropagation();

                    selectDate(
                        state.year,
                        state.month,
                        day
                    );
                }
            );

            daysContainer.appendChild(button);
        }
    }

    function selectDate(year, month, day) {
        if (!picker) {
            return;
        }

        const gregorian =
            EC.ethiopianToGregorian(
                year,
                month,
                day
            );

        const value =
            EC.formatGregorian(
                gregorian.year,
                gregorian.month,
                gregorian.day
            );

        picker.field.set_value(value);

        closePicker();
    }

    function positionPicker(field) {
        if (
            !field ||
            !field.$input ||
            !field.$input.length
        ) {
            return;
        }

        const input = field.$input[0];
        const rect = input.getBoundingClientRect();

        picker.element.style.top =
            `${rect.bottom + window.scrollY + 4}px`;

        picker.element.style.left =
            `${rect.left + window.scrollX}px`;
    }

    function openPicker(field) {
        if (!picker) {
            picker = {
                element: createPicker(),
                field: field,
                state: null
            };

            bindEvents();
        }

        picker.field = field;
        picker.state = getInitialDate(field);

        positionPicker(field);
        render();

        picker.element.classList.add("ec-visible");
    }

    function closePicker() {
        if (picker) {
            picker.element.classList.remove("ec-visible");
        }
    }

    function bindEvents() {
        const element = picker.element;

        element.querySelector(".ec-prev-month")
            .addEventListener("click", function (event) {
                event.stopPropagation();

                let month = picker.state.month - 1;
                let year = picker.state.year;

                if (month < 1) {
                    month = 13;
                    year--;
                }

                picker.state.month = month;
                picker.state.year = year;

                render();
            });

        element.querySelector(".ec-next-month")
            .addEventListener("click", function (event) {
                event.stopPropagation();

                let month = picker.state.month + 1;
                let year = picker.state.year;

                if (month > 13) {
                    month = 1;
                    year++;
                }

                picker.state.month = month;
                picker.state.year = year;

                render();
            });

        element.querySelector(".ec-prev-year")
            .addEventListener("click", function (event) {
                event.stopPropagation();

                picker.state.year--;

                render();
            });

        element.querySelector(".ec-next-year")
            .addEventListener("click", function (event) {
                event.stopPropagation();

                picker.state.year++;

                render();
            });

        element.querySelector(".ec-month")
            .addEventListener("change", function () {
                picker.state.month =
                    Number(this.value);

                render();
            });

        element.querySelector(".ec-year")
            .addEventListener("change", function () {
                const year = Number(this.value);

                if (year >= 1) {
                    picker.state.year = year;
                }

                render();
            });

        element.querySelector(".ec-today")
            .addEventListener("click", function (event) {
                event.stopPropagation();

                const today =
                    getTodayEthiopian();

                selectDate(
                    today.year,
                    today.month,
                    today.day
                );
            });

        element.querySelector(".ec-clear")
            .addEventListener("click", function (event) {
                event.stopPropagation();

                picker.field.set_value("");

                closePicker();
            });
    }

    function attachToField(field) {
    if (
        !field ||
        !field.$input ||
        !field.$input.length
    ) {
        return;
    }

    if (
        field.$input.data(
            "ethiopian-picker-attached"
        )
    ) {
        return;
    }

    field.$input.data(
        "ethiopian-picker-attached",
        true
    );

    field.$input.attr(
        "autocomplete",
        "off"
    );

    /*
     * Frappe v16 creates an Air Datepicker for every
     * Date field. We keep that datepicker alive because
     * ControlDate expects it, but hide its visual popup.
     *
     * This affects only Date fields to which our
     * Ethiopian picker is attached.
     */
    if (
        field.datepicker &&
        field.datepicker.$datepicker
    ) {
        field.datepicker.$datepicker.addClass(
            "ec-native-datepicker-hidden"
        );

        field.datepicker.hide();
    }

    /*
     * Open the Ethiopian picker when the user interacts
     * with this field.
     */
    field.$input.on(
        "click.ethiopianCalendar",
        function (event) {
            event.preventDefault();
            event.stopImmediatePropagation();

            if (
                field.datepicker &&
                typeof field.datepicker.hide === "function"
            ) {
                field.datepicker.hide();
            }

            openPicker(field);
        }
    );

    field.$input.on(
        "focus.ethiopianCalendar",
        function () {
            if (
                field.datepicker &&
                typeof field.datepicker.hide === "function"
            ) {
                field.datepicker.hide();
            }
        }
    );
}

    function attachToForm(frm) {
        if (!frm || !frm.fields_dict) {
            return;
        }

        Object.values(frm.fields_dict).forEach(
            field => {
                if (
                    field &&
                    field.df &&
                    field.df.fieldtype === "Date"
                ) {
                    attachToField(field);
                }
            }
        );
    }

    function setupForm(frm) {
        setTimeout(function () {
            attachToForm(frm);
        }, 100);
    }

    frappe.ui.form.on(
        "Ethiopian Fiscal Year",
        {
            onload(frm) {
                setupForm(frm);
            },

            refresh(frm) {
                setupForm(frm);
            }
        }
    );

frappe.ui.form.on(
    "Ethiopian Movable Holiday",
    {
        onload(frm) {
            setupForm(frm);
        },

        refresh(frm) {
            setupForm(frm);
        }
    }
);

  
    frappe.ui.form.on(
        "Ethiopian Pay Period",
        {
            onload(frm) {
                setupForm(frm);
            },

            refresh(frm) {
                setupForm(frm);
            }
        }
    );

    $(document).on(
        "click",
        function (event) {
            if (!picker) {
                return;
            }

            if (
                $(event.target).closest(
                    ".ethiopian-date-picker"
                ).length
            ) {
                return;
            }

            closePicker();
        }
    );

    $(window).on(
        "resize scroll",
        function () {
            if (
                picker &&
                picker.element.classList.contains(
                    "ec-visible"
                )
            ) {
                positionPicker(picker.field);
            }
        }
    );

})();
