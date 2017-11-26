# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 14:52:58 2017

@author: pawel.cwiek
"""
from pony import orm
from decimal import Decimal

db = orm.Database()

class Project(db.Entity):
    _table_ = 'projects'

    id = orm.PrimaryKey(int, auto=True)
    room_types = orm.Set("RoomType")
    rooms = orm.Set("Room")
    ahus = orm.Set("Ahu")
    fans = orm.Set("Fan")

    name = orm.Optional(str, nullable=True)
    number = orm.Optional(str, nullable=True)
    path = orm.Required(str, unique=True)
    date_modified = orm.Optional(str, nullable=True)
    date_parsed = orm.Optional(str, nullable=True)
    spreadsheet_version = orm.Required(str, default='unrecognised')
    stage = orm.Optional(str, nullable=True)
    sub_stage = orm.Optional(str, nullable=True)
    reparse = orm.Required(bool, default=True)
    xl_mapping_present = orm.Required(bool, default=False)
    show = orm.Required(bool, default=True)
    debug = orm.Optional(str, nullable=True)

class RoomType(db.Entity):
    _table_ = 'room_types'

    id = orm.PrimaryKey(int, auto=True)
    rooms = orm.Set("Room")
    project = orm.Required(Project)
    
    name = orm.Required(str, nullable=True)
    category = orm.Optional(str, nullable=True)
    show = orm.Required(bool, default=True)

    people_density = orm.Optional(float, nullable=True)
    air_per_person = orm.Optional(float, nullable=True)
    air_changes = orm.Optional(float, nullable=True)
    gains_people_sensible = orm.Optional(float, nullable=True)
    gains_people_latent = orm.Optional(float, nullable=True)
    gains_lighting = orm.Optional(float, nullable=True)
    gains_low_voltage = orm.Optional(float, nullable=True)
    gains_other = orm.Optional(float, nullable=True)

class Room(db.Entity):
    _table_ = 'rooms'

    id = orm.PrimaryKey(int, auto=True)
    project = orm.Required(Project)
    room_type = orm.Optional(RoomType)

    room_type_name = orm.Optional(str, nullable=True)
    show = orm.Required(bool, default=True)

    number = orm.Required(str, nullable=True)
    level = orm.Optional(str, nullable=True)
    name = orm.Optional(str, nullable=True)
    area = orm.Optional(float, nullable=True)
    volume = orm.Optional(float, nullable=True)
    people = orm.Optional(float, nullable=True)

    air_fresh_from_persons = orm.Optional(float, nullable=True)
    air_fresh_from_airchanges = orm.Optional(float, nullable=True)
    air_fresh = orm.Optional(float, nullable=True)
    air_transfer = orm.Optional(float, nullable=True)
    air_transfer_source = orm.Optional(str, nullable=True)
    air_fresh_system = orm.Optional(str, nullable=True)
    air_return1 = orm.Optional(float, nullable=True)
    air_return1_system = orm.Optional(str, nullable=True)
    air_return2 = orm.Optional(float, nullable=True)
    air_return2_system = orm.Optional(str, nullable=True)

    gains_people_sensible = orm.Optional(float, nullable=True)
    gains_people_latent = orm.Optional(float, nullable=True)
    gains_lighting = orm.Optional(float, nullable=True)
    gains_low_voltage = orm.Optional(float, nullable=True)
    gains_other = orm.Optional(float, nullable=True)

    gains_ext_sun = orm.Optional(float, nullable=True)
    gains_ext_total = orm.Optional(float, nullable=True)
    gains_system = orm.Optional(str, nullable=True)

    losses_conduction = orm.Optional(float, nullable=True)
    losses_total = orm.Optional(float, nullable=True)
    losses_system = orm.Optional(float, nullable=True)

    gains_winter = orm.Optional(float, nullable=True)
    losses_with_gains = orm.Optional(float, nullable=True)

class Ahu(db.Entity):
    _table_ = 'ahus'

    id = orm.PrimaryKey(int, auto=True)
    project = orm.Required(Project)

    name = orm.Required(str, nullable=True)
    description = orm.Optional(str, nullable=True)
    show = orm.Required(bool, default=True)

    air_fresh = orm.Optional(float, nullable=True)
    air_return = orm.Optional(float, nullable=True)
    air_fresh_plus = orm.Optional(float, nullable=True)

    heating1 = orm.Optional(float, nullable=True)
    heating1_system = orm.Optional(str, nullable=True)

    cooling_sensible = orm.Optional(float, nullable=True)
    cooling_total = orm.Optional(float, nullable=True)
    cooling_system = orm.Optional(str, nullable=True)

    heating2 = orm.Optional(float, nullable=True)
    heating2_system = orm.Optional(str, nullable=True)

class Fan(db.Entity):
    _table_ = 'fans'

    id = orm.PrimaryKey(int, auto=True)
    project = orm.Required(Project)

    show = orm.Required(bool, default=True)
    name = orm.Required(str, nullable=True)
    
    description = orm.Optional(str, nullable=True)
    flow = orm.Optional(float, nullable=True)
    
if __name__ == '__main__':
    db.bind('sqlite', ':memory:', create_db=True)
    orm.sql_debug(True)
    db.generate_mapping(create_tables=True)