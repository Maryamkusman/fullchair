from app.database import Base

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
# Salon ──< Stylist ──< Appointment >── Client
#   │                       │
#   └──< Service ───────────┘ has many 

class Salon(Base):
    # A Python class that becomes a database table. "(Base)" signs it up
    # with SQLAlchemy so it knows this class is a table.
    __tablename__ = "salons"
    # The table's name inside the database. ForeignKeys use this name.
    id: Mapped[int] = mapped_column(primary_key=True)
    # A whole-number column called "id". primary_key=True means it's the
    # unique ID for each salon; the database numbers them 1, 2, 3...

    name: Mapped[str] = mapped_column(String(100))
    # A text column called "name", up to 100 characters long.

    services: Mapped[list["Service"]] = relationship(back_populates="salon")
    # Not a column. A shortcut that gives you salon.services, a list of
    # every Service at this salon. It pairs with Service.salon.

    appointments: Mapped[list["Appointment"]] = relationship(back_populates="salon")
    # salon.appointments: a list of every appointment at this salon.
    # Pairs with Appointment.salon.

    stylists: Mapped[list["Stylist"]] = relationship(back_populates="salon")
    # salon.stylists: a list of every stylist at this salon. Plural,
    # because it's a list. Pairs with Stylist.salon.

    clients: Mapped[list["Client"]] = relationship(back_populates="salon")
    # salon.clients: a list of every client of this salon.
    # Pairs with Client.salon.


class Stylist(Base):
    __tablename__ = "stylists"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"))
    
    salon: Mapped["Salon"] = relationship(back_populates="stylists")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="stylist")


class Service(Base):
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"))
    price_cents: Mapped[int] = mapped_column(Integer)
    duration_minutes: Mapped[int]
    salon: Mapped["Salon"] = relationship(back_populates="services")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="service")

class Appointment(Base):
    __tablename__ = "appointments"
    id : Mapped[int] = mapped_column(primary_key=True)
    stylist_id: Mapped[int] = mapped_column(ForeignKey("stylists.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"))
    start_at: Mapped[datetime]
    end_at: Mapped[datetime]
    status: Mapped[str] = mapped_column(String(50), default="booked")

    salon: Mapped["Salon"] = relationship(back_populates="appointments")
    stylist: Mapped["Stylist"] = relationship(back_populates="appointments")
    client: Mapped["Client"] = relationship(back_populates="appointments")
    service: Mapped["Service"] = relationship(back_populates="appointments")

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"))
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))

    salon: Mapped["Salon"] = relationship(back_populates="clients")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="client")
