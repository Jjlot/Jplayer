from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from prettytable import PrettyTable

# sa.Column, sa.String, sa.create_engine

Base = declarative_base()

server_ip = '127.0.0.1'
user_name = 'root'
password = ''
db_name = 'Jplayer'

"""
pip3 install PyMySQL
pip3 install sqlalchemy
pip3 install prettytable
"""

"""
create database Jplayer;
"""

"""
CREATE TABLE `media_list` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255),
  `path` varchar(255) NOT NULL,
  `priority` int(10) unsigned NOT NULL,
  `played` int(10) unsigned NOT NULL,
  `failed` int(10) unsigned NOT NULL,
  `jumped` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class MediaListDB(Base):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False
    __tablename__ = 'media_list'

    id = sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    name = sa.Column(sa.String(255), nullable=True)
    path = sa.Column(sa.String(255), nullable=False)
    priority = sa.Column('priority', sa.Integer(), nullable=False)
    played = sa.Column('played', sa.Integer(), nullable=False)
    failed = sa.Column('failed', sa.Integer(), nullable=False)
    jumped = sa.Column('jumped', sa.Integer(), nullable=False)


class MediaList(object):
    def __init__(self):
        print('MediaList init start')

        # self.connection = 'mysql+pymysql://root@127.0.0.1/Jplayer'
        connection = 'mysql+pymysql://' + user_name + '@' + server_ip + '/' + db_name
        print('connection = ', connection)
        engine = create_engine(connection)
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    def get_list_all(self):
        list_all = self.session.query(MediaListDB).all()

        return list_all

    def get_id_by_path(self, media_path):
        media = self.session.query(MediaListDB).filter_by(path=media_path).one_or_none()
        if media:
            return media.id

    def create(self, path, name=None):
        new_list = MediaListDB(path=path, name=name, priority=100, played=0, failed=0, jumped=0)
        self.session.add(new_list)
        self.session.commit()

    def delete_by_id(self, vid):
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            self.session.delete(media)
            self.session.commit()

    def update(self, vid, name=None, priority=None, played=None, failed=None, jumped=None):
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            if name:
                media.name = name
            if priority:
                media.priority = priority

            if played:
                media.played = played

            if failed:
                media.failed = failed

            if jumped:
                media.jumped = jumped

            self.session.commit()

    def update_name(self, vid, name):
        self.update(vid, name=name)

    def update_priority(self, vid, action='add'):
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            raw_priority = media.priority

            if action == 'add':
                priority = raw_priority + 1
            else:
                if raw_priority > 0:
                    priority = raw_priority - 1
                else:
                    priority = 0
            self.update(vid, priority=priority)

    def increase_fail_count(self, vid):
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            self.update(vid, failed=media.failed + 1)

    def increase_play_count(self, vid):
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            self.update(vid, played=media.played + 1)

    def increase_jump_count(self, vid):
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            self.update(vid, jumped=media.jumped + 1)

    @staticmethod
    def show_info(medias):
        table = PrettyTable(['id', 'name', 'priority', 'played', 'failed', 'jumped', 'path'])
        for media in medias:
            table.add_row([
                media.id,
                media.name,
                media.priority,
                media.played,
                media.failed,
                media.jumped,
                media.path[:70],
            ])
        print(table)
