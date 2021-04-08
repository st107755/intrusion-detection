from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base = declarative_base()
class Log(Base):
    __tablename__ = 'data'

    index = Column(Integer)
    tcp_srcport = Column(Integer)
    frame_len = Column(Integer)
    tcp_flags_push = Column(Integer)
    ip_flags_df = Column(Integer)
    frame_time = Column(String)
    bytes = Column(Integer)
    label = Column(String)

    def __init__(self,tcp_srcport,frame_len,tcp_flags_push,ip_flags_df,bytes,label):
        self.tcp_srcport = tcp_srcport
        self.frame_len = frame_len
        self.tcp_flags_push = tcp_flags_push
        self.ip_flags_df = ip_flags_df
        self.frame_time = 
        self.bytes = bytes








