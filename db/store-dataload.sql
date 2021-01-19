/*==============================================================*/
/* Table: users                                                 */
/*==============================================================*/
insert into users values ('erik1110', 'erik', '123', '5F', '0912345678', '1993-11-10');
insert into users values ('dannymonkey', 'danny', '123', '5F', '0912345678', '1993-11-11');
insert into users values ('gansulab', 'gansulab', '123', '12F', '0912345678', '1993-11-12');
insert into users values ('kyorobert', 'kyorobert', '123', '5F', '0912345678', '1993-11-13');
insert into users values ('penchaq', 'chinghsuan.chang', '123', '12F', '0912345678', '1993-11-14');
/*==============================================================*/
/* Table: items                                                 */
/*==============================================================*/
insert into items values (1, '筆電', 30000, 'LC170W001', 5,'5A', 'laptop.png', 'erik1110', '2021-01-18', '2021-01-23', '已借出', '未預約');
insert into items values (2, '筆電', 40000, 'LC170W002', 5,'5A', 'laptop.png', '', '', '', '未借出', '未預約');
insert into items values (3, '筆電', 50000, 'LC170W003', 5,'12B', 'laptop.png', 'erik1110', '2021-01-18', '2020-01-23', '已借出', '未預約');
insert into items values (4, '筆電', 30000, 'LC170W004', 5,'12B', 'laptop.png', '', '', '', '未借出', '未預約');
insert into items values (5, '轉接頭', 320, 'HDMI轉type-c', 2, '5A', 'hdmi.png', '', '', '', '未借出', '未預約');
insert into items values (6, '轉接頭', 450, 'HDMI轉Lightning', 2, '12B', 'hdmi.png', 'dannymonkey', '2020-01-09', '2020-01-11', '已借出', '未預約');
insert into items values (7, '投影機', 54000, '', 3, '5A', 'projector.png', '', '', '', '未借出', '未預約');
insert into items values (8, '拖車', 1700, '', 7, '5A', 'office_cart.png', '', '', '', '未借出', '未預約');
insert into items values (9, '拖車', 1700, '', 7, '12B', 'office_cart.png', 'dannymonkey', '2020-01-09', '2020-01-16', '已借出', '未預約');
insert into items values (10, '投影筆', 160, '', 3, '12B', 'pointer.png', '', '', '', '未借出', '未預約');
insert into items values (11, '投影筆', 170, '', 3,'5A', 'pointer.png', 'penchaq', '2020-01-13', '2020-01-15', '已借出', '未預約');
/*==============================================================*/
/* Table: records  單據                                         */
/*==============================================================*/
insert into records values ('BR2021011219261610969182', '借閱', 'erik1110', '2021-01-12', 2);
insert into records values ('BR2021011319371610969854', '借閱', 'penchaq', '2021-01-13', 1);
insert into records values ('RE2021011719321610969537', '歸還', 'erik1110', '2021-01-17', 1);
insert into records values ('RE2021011819321610969537', '歸還', 'erik1110', '2021-01-18', 1);
insert into records values ('BR2021011819261610969185', '借閱', 'erik1110', '2021-01-18',2);
insert into records values ('BR2021011819351610969741', '借閱', 'dannymonkey', '2021-01-09', 2);

/*==============================================================*/
/* Table: records_item  單據詳細資訊                              */
/*==============================================================*/
insert into records_items values (1, 'BR2021011219261610969182', 2, 'erik1110', '2021-01-12', '借出');
insert into records_items values (2, 'BR2021011219261610969182', 5, 'erik1110', '2021-01-12', '借出');
insert into records_items values (3, 'BR2021011319371610969854', 11, 'penchaq', '2021-01-13', '借出');
insert into records_items values (4, 'RE2021011719321610969537', 2, 'erik1110', '2021-01-17', '歸還');
insert into records_items values (5, 'RE2021011819321610969537', 5, 'erik1110', '2021-01-18', '歸還');
insert into records_items values (6, 'BR2021011819261610969185', 1, 'erik1110', '2021-01-18', '借出');
insert into records_items values (7, 'BR2021011819261610969185', 3, 'erik1110', '2021-01-18', '借出');
insert into records_items values (8, 'BR2021011819351610969741', 6, 'dannymonkey', '2021-01-09', '借出');
insert into records_items values (9, 'BR2021011819351610969741', 9, 'dannymonkey', '2021-01-09', '借出');
