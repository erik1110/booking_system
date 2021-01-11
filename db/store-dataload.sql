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
insert into items values (1, '筆電', 30000, 'LC170W001', 5,'5A', '', '', '', '', '未借出');
insert into items values (2, '筆電', 40000, 'LC170W002', 5,'5A', '', '', '', '', '未借出');
insert into items values (3, '筆電', 50000, 'LC170W003', 5,'12B', '', 'kyorobert', '2020-01-08', '2020-01-13', '已借出');
insert into items values (4, '筆電', 30000, 'LC170W004', 5,'12B', '', '', '', '', '未借出');
insert into items values (5, '轉接頭', 320, 'HDMI轉type-c', 2, '5A', '', '', '', '', '未借出');
insert into items values (6, '轉接頭', 450, 'HDMI轉Lightning', 2, '12B', '', 'dannymonkey', '2020-01-09', '2020-01-11', '已借出');
insert into items values (7, '投影機', 54000, '', 3, '5A', '', '', '', '', '未借出');
insert into items values (8, '拖車', 1700, '', 7, '5A', '', '', '', '', '未借出');
insert into items values (9, '拖車', 1700, '', 7, '12B', '', 'dannymonkey', '2020-01-09', '2020-01-16', '已借出');
insert into items values (10, '投影筆', 160, '', 3, '12B', '', '', '', '', '未借出');
insert into items values (11, '投影筆', 170, '', 3,'5A', '', 'erik1110', '2020-01-09', '2020-01-12', '已借出');



