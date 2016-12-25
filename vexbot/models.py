import sqlalchemy as _alchy
from sqlalchemy import String, Integer, Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base as _declarative_base


Base = _declarative_base()


robot_address = Table('robot_address',
                      Base.metadata,
                      Column('robot_model_id',
                             Integer,
                             ForeignKey('robot_models.id')),
                      Column('address_id',
                             Integer,
                             ForeignKey('zmq_addresses.id')))

adapter_address = Table('adapter_address',
                        Base.metadata,
                        Column('adapter_id',
                               Integer,
                               ForeignKey('adapters.id')),
                        Column('address_id',
                               Integer,
                               ForeignKey('zmq_addresses.id')))

startup_adapters_assoc = Table('startup_adapters',
                         Base.metadata,
                         Column('robot_model_id',
                                Integer,
                                ForeignKey('robot_models.id')),
                        Column('adapter_id',
                               Integer,
                               ForeignKey('adapters.id')))

class RobotModel(Base):
    __tablename__ = 'robot_models'
    id = Column(Integer, primary_key=True)
    context = Column(String(length=50), unique=True)
    name = Column(String(length=100), default='vexbot')
    monitor_address = Column(Integer, ForeignKey('zmq_addresses.id'))
    publish_address = Column(Integer, ForeignKey('zmq_addresses.id'))
    subscribe_addresses = relationship('ZmqAddress', secondary=robot_address)
    startup_adapters = relationship('Adapter', secondary=startup_adapters_assoc)


class ZmqAddress(Base):
    __tablename__ = 'zmq_addresses'
    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False)

    def zmq_address(self):
        """
        default to tcp transport for now
        """
        return 'tcp://{}'.format(self.address)


class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class Adapter(Base):
    __tablename__ = 'adapters'
    id = Column(Integer, primary_key=True)
    module_name = Column(Integer, ForeignKey('modules.id'), nullable=False)
    service_name = Column(String(100), nullable=False)
    publish_address = Column(Integer, ForeignKey('zmq_addresses.id'))
    subscribe_addresses = relationship('ZmqAddress', secondary=adapter_address)