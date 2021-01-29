drop table if exists users;
drop table if exists items;
drop table if exists orders;
drop table if exists items_hist;
drop table if exists comments;

/*==============================================================*/
/* Table: users                                                 */
/*==============================================================*/
create table users
(
   user_id             varchar(100) primary key,
   name                varchar(30) not null,
   password            varchar(30) not null,
   address             varchar(30),
   phone               varchar(20),
   birthday            varchar(20),
   available_status    varchar(20)
);

/*==============================================================*/
/* Table: items                                                 */
/*==============================================================*/
create table items
(
   item_id             varchar(100) primary key,
   name                varchar(30) not null,
   price               integer,
   fine                integer,
   description         varchar(100),
   available_day       integer,
   location            varchar(30),
   image               varchar(100),
   borrow_user_id      varchar(100),
   reserve_user_id     varchar(100),
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
   order_type          varchar(30),
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
   borrow_order_id      varchar(100),
   return_order_id      varchar(100),
   reserve_order_id     varchar(100),
   cancel_order_id      varchar(100),
   order_status         varchar(30)
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
