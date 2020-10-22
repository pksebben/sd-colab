from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Table,
    DateTime,
    Date,
    Boolean,
    Time
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
import sqlalchemy.types as types


# This is a workaround for an incompatibility between python > 3.6 and sqlite
# retrieved from: https://github.com/jeffknupp/sandman2/issues/84
class HackTime(types.TypeDecorator):
    impl = types.Time

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            return datetime.time.strptime(value, '%H:%M:%S')
        return value


Base = declarative_base()

# certifies a member on a machine, as an instructor if applicable


class MemberToMachine(Base):
    __tablename__ = 'member_to_machine'
    member_id = Column(Integer, ForeignKey('member.id'), primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.id'), primary_key=True)
    instructor = Column(Boolean, nullable=False)

# member registration


class Member(Base):
    __tablename__ = "member"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)
    created = Column(DateTime)
    admin = Column(Boolean, nullable=False)
    passhash = Column(String, nullable=False)

# machine registration


class Machine(Base):
    __tablename__ = "machine"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)

# Trying a new thing
# reservations will track the machine, the date, and the time, and we're going to use
# querying cleverly to check for collissions, rather than trying to reduce problem space via
# multiple tables.


class Reservation(Base):
    __tablename__ = "reservation"
    date = Column(Date, primary_key=True)
    start = Column(String)
    end = Column(String)
    member_id = Column(Integer, ForeignKey('member.id'), primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.id'), primary_key=True)


# ON HOLD: I want to try a simpler method of booking reservations first.  Then we can go bugfuck with all the tables.
# class MachineCalendar(Base):
#     __tablename__ = "machine_calendar"
#     machine_id = Column(Integer, primary_key=True, ForeignKey('machine.id'))
#     dates = relationship('Day', back_populates="machine_calendar")

# class Day(Base):
#     __tablename__ = "day"
#     date = Column(Date, primary_key=True)
#     calendar_id = Column(Integer, primary_key=True, ForeignKey('machine_calendar.machine_id'))
#     machine_calendar = relationship('MachineCalendar', back_populates='day')
#     times = Column(Time)


# # may want to rethink this in favor of a calendar.  Or not.  Think on it.
# class TimeSlot(Base):
#     __tablename__ = "timeslot"
#     id = Column(Integer, primary_key=True)
#     workstation_id = Column(Integer, ForeignKey("workstation.id"), nullable=False)
#     member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
#     time = Column(DateTime)


# I can't think of a world in which the rest of this data is necessary, so
# long as we have calendars for the machines that can track when they're
# available and to whom they're promised.

# class LaserSlot(Base):
#     __tablename__ = "laserslot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class CeramicsSlot(Base):
#     __tablename__ = "ceramicslot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class ThreeDPrintSlot(Base):
#     __tablename__ = "threedprintslot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class DesignSlot(Base):
#     __tablename__ = "designslot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class ElectronicSeat1Slot(Base):
#     __tablename__ = "electronicseat1slot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class ElectronicSeat2Slot(Base):
#     __tablename__ = "electronicseat2slot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class ElectronicSeat3Slot(Base):
#     __tablename__ = "electronicseat3slot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class PlasmaCutterSlot(Base):
#     __tablename__ = "plasmacutterslot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class PrintMakingSlot(Base):
#     __tablename__ = "printmakingslot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class Router1Slot(Base):
#     __tablename__ = "router1slot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class Router2Slot(Base):
#     __tablename__ = "router2slot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class SewingSlot(Base):
#     __tablename__ = "sewingslot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class WeldingSlot(Base):
#     __tablename__ = "weldingslot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)

# class WoodshopSlot(Base):
#     __tablename__ = "woodhopslot"
#     slot = Column(DateTime, unique = True, nullable=False)
#     member_id = Column(Integer, ForeignKey(member.id), nullable=True)
#     closed = Column(Boolean, nullable=False)
