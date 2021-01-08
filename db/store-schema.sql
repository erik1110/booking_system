drop table if exists users;
drop table if exists items;
drop table if exists items_info;
drop table if exists records;
drop table if exists reservation;

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
   image               varchar(100)
);

/*==============================================================*/
/* Table: items_info                                            */
/*==============================================================*/
create table items_info
(
   item_id              integer primary key,
   user_id              varchar(20) not null references users(user_id),
   borrow_date          date format 'YYYY-MM-DD',
   status               integer default 0
);


/*==============================================================*/
/* Table: records                                               */
/*==============================================================*/
create table records
(
   records_id           integer primary key autoincrement,
   item_id              integer not null references items_info(item_id),
   user_id              integer not null references users(user_id),
   borrow_date          date format 'YYYY-MM-DD',
   status               integer not null
   etl_date             date format 'YYYY-MM-DD',
);
/*==============================================================*/
/* Table: reservation                                           */
/*==============================================================*/
create table reservation
(
   reservation_id       integer primary key autoincrement,
   item_id              integer not null references items_info(item_id),
   user_id              integer not null references users(user_id),
   etl_date             date format 'YYYY-MM-DD'
);
