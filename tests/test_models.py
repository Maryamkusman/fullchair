from datetime import datetime, timedelta

from sqlalchemy import select

from app.models import Appointment, Client, Salon, Service, Stylist


def test_book_an_appointment(db):
    salon = Salon(name="Juniper Hair Studio")
    stylist = Stylist(name="Aisha", salon=salon)
    service = Service(name="Silk Press", duration_minutes=90, price_cents=8500, salon=salon)
    client = Client(name="Sara", phone="+17345550101", salon=salon)

    start = datetime(2026, 11, 3, 10, 0)
    appointment = Appointment(
        salon=salon,
        stylist=stylist,
        service=service,
        client=client,
        start_at=start,
        end_at=start + timedelta(minutes=service.duration_minutes),
    )
    db.add(appointment)
    db.commit()

    saved = db.scalars(select(Appointment)).one()
    assert saved.stylist.name == "Aisha"
    assert saved.end_at == datetime(2026, 11, 3, 11, 30)
    assert saved.status == "booked"
    assert salon.stylists == [stylist]
    assert client.appointments == [saved]