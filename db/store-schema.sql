drop table if exists users;
drop table if exists items;
drop table if exists records;
drop table if exists records_items;

/*==============================================================*/
/* Table: users                                                 */
/*==============================================================*/
create table users
(
   user_id             varchar(20) primary key,
   name                varchar(50) not null,
   password            varchar(20) not null,
   address             varchar(100),
   phone               varchar(20),
   birthday            varchar(20)
);

/*==============================================================*/
/* Table: items                                                 */
/*==============================================================*/
create table items
(
   item_id             integer primary key autoincrement,
   name                varchar(100) not null,
   price               float,
   description         varchar(200),
   available_day       integer,
   location            varchar(10),
   image               varchar(100),
   user_id             varchar(20),
   borrow_date         date,
   return_date         date,
   status              varchar(20)
);

/*==============================================================*/
/* Table: records                                               */
/*==============================================================*/
create table records
(
   records_id           varchar(100) primary key,
   action               varchar(20),
   user_id              varchar(20) not null references users(user_id),
   records_date         DATEFROMPARTS,
   total                integer
);

/*==============================================================*/
/* Table: records_items                                               */
/*==============================================================*/
create table records_items
(
   id                   integer primary key autoincrement,
   records_id           integer not null references records(records_id),
   item_id              integer not null references items(item_id),
   user_id              varchar(20) not null references users(user_id),
   records_date         date,
   status               varchar(20)
);


-- /*==============================================================*/
-- /* Table: reservation                                           */
-- /*==============================================================*/
-- create table reservation
-- (
--    reservation_id       integer primary key autoincrement,
--    item_id              integer not null references items(item_id),
--    user_id              varchar(20) not null references users(user_id),
--    reverse_date         date format 'YYYY-MM-DD'
-- );