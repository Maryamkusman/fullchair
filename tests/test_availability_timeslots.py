from datetime import datetime

from app.availability import available_timeslots
from app.models import Appointment

DAY_START = datetime(2026, 11, 3, 9, 0)
DAY_END = datetime(2026, 11, 3, 17, 0)


def at(hour, minute=0):
    """A datetime on the test day, e.g. at(10, 30) -> Nov 3, 10:30."""
    return datetime(2026, 11, 3, hour, minute)


def appt(start_hour, start_minute, end_hour, end_minute):
    """An Appointment with just the times filled in (no database needed)."""
    return Appointment(start_at=at(start_hour, start_minute), end_at=at(end_hour, end_minute))


def find(appointments, duration=90):
    return available_timeslots(
        new_appt_duration=duration,
        appointments=appointments,
        daysstart=DAY_START,
        daysend=DAY_END,
    )


def test_no_appointments_means_whole_day_is_free():
    assert find([]) == [(DAY_START, DAY_END)]


def test_gap_before_first_appointment():
    # Booked 11:00-12:00, so 9:00-11:00 (2 hours) fits a 90-minute service
    slots = find([appt(11, 0, 12, 0)])
    assert (at(9), at(11)) in slots


def test_gap_between_two_appointments():
    # 10:00-11:00 and 13:00-14:00 leave a 2-hour gap from 11:00 to 13:00
    slots = find([appt(10, 0, 11, 0), appt(13, 0, 14, 0)])
    assert (at(11), at(13)) in slots


def test_gap_after_last_appointment():
    # Booked until 14:00, so 14:00-17:00 is free
    slots = find([appt(9, 0, 14, 0)])
    assert slots == [(at(14), DAY_END)]


def test_gap_too_short_is_skipped():
    # 10:00-11:00 and 12:00-13:00 leave only a 1-hour gap: too short for 90 minutes
    slots = find([appt(10, 0, 11, 0), appt(12, 0, 13, 0)])
    assert (at(11), at(12)) not in slots


def test_gap_exactly_long_enough_is_included():
    # A 90-minute gap from 10:00 to 11:30 fits a 90-minute service exactly
    slots = find([appt(9, 0, 10, 0), appt(11, 30, 17, 0)])
    assert slots == [(at(10), at(11, 30))]


def test_back_to_back_appointments_leave_no_gap_between():
    slots = find([appt(9, 0, 10, 0), appt(10, 0, 11, 0)])
    assert slots == [(at(11), DAY_END)]


def test_fully_booked_day_has_no_slots():
    assert find([appt(9, 0, 17, 0)]) == []


def test_unsorted_appointments_still_work():
    # Passed out of order on purpose; the function should sort them first
    slots = find([appt(13, 0, 14, 0), appt(10, 0, 11, 0)])
    assert slots == [(at(11), at(13)), (at(14), DAY_END)]


def test_all_gaps_found_in_order():
    slots = find([appt(11, 0, 12, 0), appt(14, 0, 15, 0)])
    assert slots == [
        (at(9), at(11)),      # before the first
        (at(12), at(14)),     # between
        (at(15), DAY_END),    # after the last
    ]