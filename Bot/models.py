import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean
from database import Base

try:
    PREFIX = os.environ["PREFIX"]
except:
    PREFIX = "*"

class Clients(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(Integer, index=True, nullable=False)
    prefix = Column(String, default=PREFIX)
    channel = Column(Integer, index=True, nullable=False)

    def __init__(self, guild_id, channel, prefix=PREFIX):
        self.guild_id = guild_id
        self.prefix = prefix
        self.channel = channel