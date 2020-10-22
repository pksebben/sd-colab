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
    notes=Column(String, nullable=True)
    reservations = relationship("Reservation", back_populates="member")

# machine registration


class Machine(Base):
    __tablename__ = "machine"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)

# reservations for time on machines


class Reservation(Base):
    __tablename__ = "reservation"
    date = Column(Date, primary_key=True)
    start = Column(String)
    end = Column(String)
    notes = Column(String, nullable=True)
    member_id = Column(Integer, ForeignKey('member.id'), primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.id'), primary_key=True)
    member = relationship("Member", back_populates='reservations')
    
