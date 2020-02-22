from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Table,
    DateTime,
    Date,
    Boolean
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine


Base = declarative_base()

class MemberToMachine(Base):
    __tablename__ = 'member_to_machine'
    member_id = Column(Integer, ForeignKey('member.id'), primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.id'), primary_key=True)
    instructor = Column(Boolean, nullable=False)

class Member(Base):
    __tablename__ = "member"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    created = Column(DateTime)
    admin = Column(Boolean, nullable=False)
    passhash = Column(String, nullable=False)

class Machine(Base):
    __tablename__ = "machine"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)

class Workstation(Base):
    __tablename__ = "workstation"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)
    
    
class TimeSlot(Base):
    __tablename__ = "timeslot"
    id = Column(Integer, primary_key=True)
    workstation_id = Column(Integer, ForeignKey("workstation.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    time = Column(DateTime)



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

