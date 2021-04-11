from sqlalchemy import Column, String, Integer, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
import pdb
Base = declarative_base()


class Log(Base):
    __tablename__ = "ddos"

    id = Column(Integer,primary_key=True)
    tcp_srcport = Column(Integer)
    frame_len = Column(Integer)
    tcp_flags_push = Column(Integer)
    ip_flags_df = Column(Integer)
    frame_time = Column(DateTime)
    byte = Column(Integer)
    label = Column(String)
    def __init__(
        self, tcp_srcport, frame_len, tcp_flags_push, ip_flags_df, byte, label
    ):
        self.tcp_srcport = tcp_srcport
        self.frame_len = frame_len
        self.tcp_flags_push = tcp_flags_push
        self.ip_flags_df = ip_flags_df
        self.byte = byte
        self.frame_time = datetime.datetime.utcnow()
        self.label = label