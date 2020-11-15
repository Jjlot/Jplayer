from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
# sa.Column, sa.String, sa.create_engine

Base = declarative_base()

server_ip='127.0.0.1'
user_name='root'
password=''
db_name='Jplayer'

"""
CREATE TABLE `media_list` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255),
  `path` varchar(255) NOT NULL,
  `priority` int(10) unsigned NOT NULL,
  `played` int(10) unsinged NOT NULL,
  `failed` int(10) unsinged NOT NULL,
  `jumped` int(10) unsinged NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class MediaListDB(Base):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False
    __tablename__ = 'media_list'

    id = sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    name = sa.Column(sa.String(255), nullable=True))
    path = sa.Column(sa.String(255), nullable=False))
    priortity = sa.Column('priority', sa.Integer(), nullable=False))
    played = sa.Column('played', sa.Integer(), nullable=False))
    failed = sa.Column('failed', sa.Integer(), nullable=False))
    jumped = sa.Column('jumped', sa.Integer(), nullable=False))

class MediaList():
    def __init__(self):
        print('MediaList init start')

        # self.connection = 'mysql+pymysql://root@127.0.0.1/Jplayer'
        self.connection='mysql+pymysql://' + uesr_name '@' + server_ip +'/' + db_name
        print('connection = ', self.connection)
        self.engine = create_engine(connection)
        self.session = sessionmaker(bind=engine)

    def get_list_all(self):
        list_all = self.session.query(MediaListDB).all()

        return list_all

    def get_id_by_path(self, path):
        media = self.session.query(MediaListDB).filter(path=path)one_or_none()
        if media:
            return media['id']

    def create(self, path, name=None):
        new_list = User(path=path, name=name, priority=100, played=0, failed=0, jumped=0)
        self.session.add(new_user)
        self.session.commit()

    def delete_by_id(self, id)
        media = self.session.query(MediaListDB).filter(id=id)one_or_none()
        if media:
            self.session.delete(media)
            self.session.commit()

    '''
    def _db_update_database_ips(self, bypass_db, fips=None, dummys=None):
        db = NatGatewayBypass(
            nat_gateway_id=bypass_db['nat_gateway_id'],
            route_id=bypass_db['route_id'],
            pbr_id=bypass_db['pbr_id'],
            fips=self._to_string(fips) if fips else bypass_db['fips'],
            dummys=self._to_string(dummys) if dummys else bypass_db['dummys'],
            gname=bypass_db['gname']
        )
        bypass_db.update(db)
        self.session.commit()
    '''

    def update(self, id, name=None, priority=None, played=None, failed=None, jumped=None)
        media = self.session.query(MediaListDB).filter(id=id)one_or_none()
        if media:
            db = User(
                path=media['path'],
                name=name if name else media['name'],
                priority=priority if priority else media['priority'],
                played=played if played else media['played']
                failed=failed if failed else media['failed']
                jumped=jumped if jumped else media['jumped']
            )
            db.update(db)
            self.session.commit()

    def update_name(self, id, name)
        self.update(id, name=name)

    def update_priority(self, id, action='add')
        media = self.session.query(MediaListDB).filter(id=id)one_or_none()
        if media:
            raw_priority = media['priority']

            if action == 'add':
                priority = raw_priority + 1
            else
                if raw_priority > 0:
                    priority = raw_priority - 1
                else:
                    priority = 0
            self.update(id, priority=priority)

    def increase_fail_count(self, id)
        media = self.session.query(MediaListDB).filter(id=id)one_or_none()
        if media:
            self.update(id, failed=media['failed'] + 1)

    def increase_play_count(self, id)
        media = self.session.query(MediaListDB).filter(id=id)one_or_none()
        if media:
            self.update(id, played=media['played'] + 1)

    def increase_jump_count(self, id)
        media = self.session.query(MediaListDB).filter(id=id)one_or_none()
        if media:
            self.update(id, jumped=media['jumped'] + 1)


# Test
import random
r = random.randint(1, 10000)
test_name = 'test' + str(r)

Medialist m
list_all = m.get_list_all()
for one in list_all:
    print(one)

'''
# create table `media_list`(`id` INT(20), `name` VARCHAR(20), primary key (`id`))engine=InnoDB default charset=utf8;
class MediaList(Base):
    __tablename__ = 'media_list'

    id = Column(Int(20), primary_key=True)
    path = Column(String(128))
    priority = Column(Int(100))
    name = Column(String(20))

connection='mysql+pymysql://root@127.0.0.1/test'
engine = create_engine(connection)
DBSession = sessionmaker(bind=engine)
new_user = User(id='5', name='Bob')

# ADD
print('ADD')
session = DBSession()
session.add(new_user)
session.commit()
session.close()

# GET
print('GET')
session = DBSession()
ret = session.query(User).first()
session.close()
print(ret.id, ret.name)

# DELETE
print('DELETE')
session = DBSession()
session.delete(ret)
session.commit()
session.close()
'''
