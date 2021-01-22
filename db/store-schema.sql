drop table if exists users;
drop table if exists items;
<<<<<<< HEAD
drop table if exists orders;
drop table if exists items_hist;
drop table if exists comments;
=======
drop table if exists items_info;
drop table if exists records;
drop table if exists reservation;
>>>>>>> 1c0eeb2b34844ad231327eb992107b6a4a9ae571

/*==============================================================*/
/* Table: users                                                 */
/*==============================================================*/
create table users
(
<<<<<<< HEAD
   user_id             varchar(100) primary key,
   name                varchar(30) not null,
   password            varchar(30) not null,
   address             varchar(30),
   phone               varchar(20),
   birthday            varchar(20),
   available_status    varchar(20)
=======
   user_id             varchar(20) primary key,
   name                varchar(50) not null,
   password            varchar(20) not null,
   address             varchar(100),
   phone               varchar(20),
   birthday            varchar(20)
>>>>>>> 1c0eeb2b34844ad231327eb992107b6a4a9ae571
);

/*==============================================================*/
/* Table: items                                                 */
/*==============================================================*/
create table items
(
<<<<<<< HEAD
   item_id             varchar(100) primary key,
   name                varchar(30) not null,
   price               integer,
   fine                integer,
   description         varchar(100),
   available_day       integer,
   location            varchar(30),
   image               varchar(100),
   user_id             varchar(100),
   borrow_date         date,
   expected_date       date,
   return_date         date,
   reserve_date        date,
   booking_status      varchar(30),
   reserve_status      varchar(30)
);

/*==============================================================*/
/* Table: orders （單據）                                       */
/*==============================================================*/
create table orders
(
   order_id            varchar(100) primary key,
   action              varchar(30),
   user_id             varchar(100) not null references users(user_id),
   total               integer,
   order_date          date
);

/*==============================================================*/
/* Table: items_hist (物品歷史資訊)                               */
/*==============================================================*/
create table items_hist
(
   hist_id              varchar(100) primary key,
   item_id              varchar(100) not null references items(item_id),
   user_id              varchar(100) not null references users(user_id),
   borrow_date          date,
   expected_date        date,
   return_date          date,
   reserve_date         date,
   borrow_order_id      varchar(100) references orders(order_id),
   return_order_id      varchar(100) references orders(order_id),
   reserve_order_id     varchar(100) references orders(order_id)
);


/*==============================================================*/
/* Table: comment (評論)                                         */
/*==============================================================*/
create table comments
(
   comment_id           varchar(100) primary key,
   item_id              varchar(100) not null references items(item_id),
   user_id              varchar(100) not null references users(user_id),
   content              varchar(100),
   comment_date         date
);
=======
   item_id             integer primary key autoincrement,
   name                varchar(100) not null,
   price               float,
   description         varchar(200),
   available_day       integer,
   location            varchar(10),
   image               varchar(100),
   user_id             varchar(20),
   borrow_date         date format 'YYYY-MM-DD',
   return_date         date format 'YYYY-MM-DD',
   status              integer default '未借出'
);

/*==============================================================*/
/* Table: records                                               */
/*==============================================================*/
create table records
(
   records_id           integer primary key autoincrement,
   item_id              integer not null references items(item_id),
   user_id              integer not null references users(user_id),
   borrow_date          date format 'YYYY-MM-DD',
   return_date          date format 'YYYY-MM-DD',
   status               integer not null
);
/*==============================================================*/
/* Table: reservation                                           */
/*==============================================================*/
create table reservation
(
   reservation_id       integer primary key autoincrement,
   item_id              integer not null references items(item_id),
   user_id              integer not null references users(user_id),
   reverse_date         date format 'YYYY-MM-DD'
);
>>>>>>> 1c0eeb2b34844ad231327eb992107b6a4a9ae571
