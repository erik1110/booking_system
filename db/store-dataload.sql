/*==============================================================*/
-- /* Table: users                                                 */
/*==============================================================*/
insert into users values ('erik1110', 'erik', '123', '5F', '0912345678', '1993-11-10', '可借用');
insert into users values ('dannymonkey', 'danny', '123', '5F', '0912345678', '1993-11-11', '可借用');
insert into users values ('gansulab', 'gansulab', '123', '12F', '0912345678', '1993-11-12', '可借用');
insert into users values ('kyorobert', 'kyorobert', '123', '5F', '0912345678', '1993-11-13', '可借用');
insert into users values ('penchaq', 'chinghsuan.chang', '123', '12F', '0912345678', '1993-11-14', '可借用');
/*==============================================================*/
/* Table: items                                                 */
/*==============================================================*/
insert into items values ('1', '筆電', 30000, 100, 'LC170W001', 5,'5A', 'laptop.png', 'erik1110', '','2021-01-12', '2021-01-23', '', '', '已借出', '未預約');
insert into items values ('2', '筆電', 40000, 100, 'LC170W002', 5,'5A', 'laptop.png', '', '', '', '', '', '', '未借出', '未預約');
insert into items values ('3', '筆電', 50000, 100, 'LC170W003', 5,'12B', 'laptop.png', 'erik1110', '', '2021-01-12', '2021-01-23', '', '', '已借出', '未預約');
insert into items values ('4', '筆電', 30000, 100, 'LC170W004', 5,'12B', 'laptop.png', '', '', '', '', '', '', '未借出', '未預約');
insert into items values ('5', '轉接頭', 320, 30, 'HDMI轉type-c', 2, '5A', 'hdmi.png', '', '', '', '', '', '', '未借出', '未預約');
insert into items values ('6', '轉接頭', 450, 30, 'HDMI轉Lightning', 2, '12B', 'hdmi.png', '', '', '', '', '', '', '未借出', '未預約');
insert into items values ('7', '投影機', 54000, 50, '好用的', 3, '5A', 'projector.png', 'dannymonkey', 'erik1110', '2021-01-09', '2021-01-12', '', '2021-01-10', '已借出', '已預約');
insert into items values ('8', '拖車', 1700, 60, '藍色', 7, '5A', 'office_cart.png', '', '', '', '', '', '', '未借出', '未預約');
insert into items values ('9', '拖車', 1700, 60, '黃色', 7, '12B', 'office_cart.png', '', '', '', '', '', '', '未借出', '未預約');
insert into items values ('10', '投影筆', 160, 15, '黑色', 3, '12B', 'pointer.png', '', '', '', '', '', '', '未借出', '未預約');
insert into items values ('11', '投影筆', 170, 15, '紅色', 3,'5A', 'pointer.png', 'penchaq', '', '2021-01-10', '2021-01-15', '', '', '已借出', '未預約');
/*==============================================================*/
/* Table: orders  單據                                         */
/*==============================================================*/
insert into orders values ('BOR20210109112335', 'borrow', 'dannymonkey', 1, '2021-01-09');
insert into orders values ('RES20210110112624', 'reserve', 'erik1110', 1, '2021-01-10');
insert into orders values ('BOR20210129112325', 'borrow', 'erik1110', 2, '2021-01-12');
insert into orders values ('BOR20210109118235', 'borrow', 'penchaq', 1, '2021-01-10');

/*==============================================================*/
/* Table: items_hist  物品歷史詳細資訊                              */
/*==============================================================*/
insert into items_hist values ('HIST2021010919261610939481', '7', 'dannymonkey', '2021-01-09', '', '', '', '', '', 'BOR20210109112335', '', 'borrow');
insert into items_hist values ('HIST2021011019261610969181', '7', 'erik1110', '', '', '', '2021-01-10', '', '', 'RES20210110112624', '', 'reserve');
insert into items_hist values ('HIST2021011219261610969182', '1', 'erik1110', '2021-01-12', '2021-01-17', '', '', 'BOR20210129112325', '', '', '', 'borrow');
insert into items_hist values ('HIST2021011219261610969982', '3', 'erik1110', '2021-01-12', '2021-01-17', '', '', 'BOR20210129112325', '', '', '', 'borrow');
insert into items_hist values ('HIST2021011019261617969982', '11', 'penchaq', '2021-01-10', '2021-01-15', '', '', 'BOR20210109118235', '', '', '', 'borrow');

/*==============================================================*/
/* Table: comments  評論                                        */
/*==============================================================*/
insert into comments values ('COM20210101118201', '1', 'gansulab', '頭香', '2021-01-01');
insert into comments values ('COM20210102138202', '1', 'gansulab', '啊這個怎麼這麼lag 扣分', '2021-01-02');
insert into comments values ('COM20210103118403', '1', 'kyorobert', '4樓用壞的啦', '2021-01-03');
insert into comments values ('COM20210108788204', '1', 'dannymonkey', '這邊好熱鬧', '2021-01-08');
insert into comments values ('COM20210109116205', '1', 'dannymonkey', '鍵盤縫隙藏了好多屑屑@@', '2021-01-09');
insert into comments values ('COM20210110118206', '1', 'erik1110', '(〒︿〒)', '2021-01-10');
insert into comments values ('COM20210111118407', '1', 'erik1110', '聽說5樓最近有老鼠 好可怕', '2021-01-11');
insert into comments values ('COM20210112148208', '1', 'kyorobert', '漏水是老鼠要的嗎？', '2021-01-12');
insert into comments values ('COM20210113118209', '1', 'dannymonkey', '放了黏鼠板也抓不到R 怎辦', '2021-01-13');
insert into comments values ('COM20210112148210', '10', 'penchaq', '這個是不是壞了(((ﾟДﾟ;)))', '2021-01-12');
insert into comments values ('COM20210112113311', '7', 'erik1110', '......', '2021-01-12');
insert into comments values ('COM20210110114412', '9', 'penchaq', '輪子在某個角度會有點卡卡的，班很重的物品會有點吃力', '2021-01-10');
