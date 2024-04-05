import psycopg2
class organisation_databes:
    conn: object

    def __init__(self, database="database", user="postgres", password="postgres"):
        self.conn = psycopg2.connect(database="database", user="postgres", password="postgres")

    def __del__(self):
        self.conn.commit()
        self.conn.close()
    def create_tables(self):
        # persons; сотрудники
        # fullnames; список ФИО
        # firstnames; Имена
        # secondnames; Фамилии
        # patronymics; Отчеста
        # positions; Должности
        # organizations; Организации
        # buildins; Строения/ корпуса
        # cabinets; кабинеты
        # divisions; подразделения
        # departments; отделения
        # locations; местоположение кабинетов
        with self.conn.cursor() as cur:
            cur.execute("""
                drop table if exists locations;
                drop table if exists persons;
                drop table if exists fullnames;
                drop table if exists firstnames;
                drop table if exists secondnames;
                drop table if exists patronymics;
                drop table if exists positions;
                drop table if exists organizations;
                drop table if exists buildins;
                drop table if exists cabinets;
                drop table if exists divisions;
                drop table if exists departments;
                """)
            cur.execute("""
                create table if not exists firstnames(
                    id serial primary key,
                    text varchar(40) unique not null
                );
                """)
            cur.execute("""
                create table if not exists secondnames(
                    id serial primary key,
                    text varchar(40) unique not null
                );
                """)
            cur.execute("""
                create table if not exists patronymics(
                    id serial primary key,
                    text varchar(40) unique not null
                );
                """)
            cur.execute("""
                create table if not exists fullnames(
                    id serial primary key,
                    id_firstname integer not null references firstnames(id),
                    id_secondname integer not null references secondnames(id),
                    id_patronymic integer references patronymics(id),
                    constraint UC_Person unique (id_firstname,id_secondname,id_patronymic)
                );
                """)
            cur.execute("""
                create table if not exists positions(
                    id serial primary key,
                    text varchar(40) unique not null
                );
                """)
            cur.execute("""
                create table if not exists persons(
                    id serial primary key,
                    id_fullname integer not null references fullnames(id),
                    id_position integer not null references positions(id)
                );
                """)
            cur.execute("""
                create table if not exists organizations(
                    id serial primary key,
                    name varchar(40) unique not null,
                    address varchar(40)
                );
                """)
            cur.execute("""
                create table if not exists buildins(
                    id serial primary key,
                    name varchar(40) unique not null,
                    address varchar(80)
                );
                """)
            cur.execute("""
                create table if not exists cabinets(
                    id serial primary key,
                    name varchar(40) unique not null
                );
                """)
            cur.execute("""
                create table if not exists divisions(
                    id serial primary key,
                    name varchar(40) unique not null
                );
                """)
            cur.execute("""
                create table if not exists departments(
                    id serial primary key,
                    name varchar(40) unique not null
                );
                """)
            cur.execute("""
                create table if not exists locations(
                    id serial primary key,
                    floor integer not null,
                    id_organization integer not null references organizations(id),
                    id_buildin integer not null references buildins(id),
                    id_division integer not null references divisions(id),
                    id_department integer not null references departments(id),
                    id_cabinet integer not null references cabinets(id),
                    constraint UC_Location unique (floor,id_organization,id_buildin,id_division,id_department,id_cabinet)
                );
                """)
            self.conn.commit()
    def add_building(self, name: str, address: str)-> int:
        cur = self.conn.cursor()
        cur.execute("insert into buildins values(default, %s, %s) returning id;",(name, address))
        return cur.fetchone()

    def add_organization(self, name, address)->int:
        pass

    def add_departament(self, name)->int:
        pass

botkina_db: organisation_databes = organisation_databes()
botkina_db.create_tables()
buildings = [("Взрослая поликлиника №4", "Орловская обл., г. Орёл, ул. Раздольная, д.57"),
            ("Детская поликлиника №4", "Орловская обл., г. Орёл, ул. Металлургов, д.80"),
             ("Главный лечебный корпус",	"Орловская обл., г. Орёл, ул. Металлургов, д.80"),
             ("Инфекционное отделение",	"Орловская обл., г. Орёл, ул. Металлургов, д.80"),
             ("Родильные отделения",	"Орловская обл., г. Орёл, ул. Металлургов, д.80"),
             ("Пищеблок",	"Орловская обл., г. Орёл, ул. Металлургов, д.80"),
             ("Патолого-анатомическое отделение",	"Орловская обл., г. Орёл, ул. Металлургов, д.80"),
             ("Женская консультация № 1", "Орловская обл., г. Орёл, ул. 2 Курская, д.54"),
             ("Отделение лучевой диагностики",	"Орловская обл., г. Орёл, ул. Металлургов, д.80")]

for building in buildings:
    botkina_db.add_building(building[0], building[1]
