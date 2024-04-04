import psycopg2

conn = psycopg2.connect(database="database", user="postgres", password="postgres")
with conn.cursor() as cur:
    cur.execute("""
        drop table if exists fsp_relation;
        drop table if exists firstname;
        drop table if exists secondname;
        drop table if exists patronymic;
        """)
    cur.execute("""
        create table if not exists firstname(
            id serial primary key,
            text varchar(40) unique not null
        );
        """)
    cur.execute("""
        create table if not exists secondname(
            id serial primary key,
            text varchar(40) unique not null
        );
        """)
    cur.execute("""
        create table if not exists patronymic(
            id serial primary key,
            text varchar(40) unique not null
        );
        """)
    cur.execute("""
        create table if not exists fsp_relation(
            id serial primary key,
            id_firstname integer not null references firstname(id),
            id_secondname integer not null references secondname(id),
            id_patronymic integer not null references patronymic(id),
            constraint UC_Person unique (id_firstname,id_secondname,id_patronymic)
        );
        """)
    cur.execute("""
        create table if not exists person(
            id serial primary key,
            id_name integer
        );
        """)
    conn.commit()
conn.close()