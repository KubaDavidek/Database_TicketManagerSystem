create database tickets
  character set utf8mb4
  collate utf8mb4_unicode_ci;

use tickets;

create table venue (
  id int auto_increment primary key,
  name varchar(120) not null,
  city varchar(80) not null,
  address varchar(160) null
);

create table event (
  id int auto_increment primary key,
  venue_id int not null,
  name varchar(160) not null,
  start_at datetime not null,
  base_price decimal(10,2) not null,
  is_active tinyint(1) not null default 1,
  constraint fk_event_venue foreign key (venue_id) references venue(id)
);

create table seat (
  id int auto_increment primary key,
  venue_id int not null,
  sector varchar(40) not null,
  seat_row int not null,
  seat_no int not null,
  is_accessible tinyint(1) not null default 0,
  constraint uq_seat unique (venue_id, sector, seat_row, seat_no),
  constraint fk_seat_venue foreign key (venue_id) references venue(id)
);

create table customer (
  id int auto_increment primary key,
  full_name varchar(120) not null,
  email varchar(120) not null,
  phone varchar(40) null,
  constraint uq_customer_email unique (email)
);

create table `order` (
  id int auto_increment primary key,
  customer_id int not null,
  status enum('new','reserved','paid','cancelled') not null default 'new',
  created_at datetime not null default current_timestamp,
  paid_at datetime null,
  notes varchar(255) null,
  constraint fk_order_customer foreign key (customer_id) references customer(id)
);

create table ticket (
  id int auto_increment primary key,
  event_id int not null,
  seat_id int not null,
  price decimal(10,2) not null,
  is_sold tinyint(1) not null default 0,
  created_at datetime not null default current_timestamp,
  constraint uq_ticket_event_seat unique (event_id, seat_id),
  constraint fk_ticket_event foreign key (event_id) references event(id),
  constraint fk_ticket_seat foreign key (seat_id) references seat(id)
);

create table order_item (
  order_id int not null,
  ticket_id int not null,
  quantity int not null default 1,
  primary key (order_id, ticket_id),
  constraint fk_item_order foreign key (order_id) references `order`(id),
  constraint fk_item_ticket foreign key (ticket_id) references ticket(id)
);

create table tag (
  id int auto_increment primary key,
  name varchar(50) not null,
  constraint uq_tag_name unique (name)
);

create table event_tag (
  event_id int not null,
  tag_id int not null,
  primary key (event_id, tag_id),
  constraint fk_event_tag_event foreign key (event_id) references event(id),
  constraint fk_event_tag_tag foreign key (tag_id) references tag(id)
);

create view v_event_sales as
select
  e.id as event_id,
  e.name as event_name,
  v.city as city,
  e.start_at as start_at,
  count(t.id) as tickets_total,
  sum(case when t.is_sold = 1 then 1 else 0 end) as tickets_sold,
  sum(case when t.is_sold = 0 then 1 else 0 end) as tickets_available,
  coalesce(sum(case when t.is_sold = 1 then t.price else 0 end), 0) as revenue
from event e
join venue v on v.id = e.venue_id
left join ticket t on t.event_id = e.id
group by e.id, e.name, v.city, e.start_at;

create view v_customer_orders as
select
  c.id as customer_id,
  c.full_name as full_name,
  c.email as email,
  count(o.id) as orders_count,
  max(o.created_at) as last_order_at
from customer c
left join `order` o on o.customer_id = c.id
group by c.id, c.full_name, c.email;

insert into venue (name, city, address) values
('O2 Arena', 'Praha', 'Českomoravská 2345/17'),
('Forum Karlín', 'Praha', 'Pernerova 51'),
('Enteria Arena', 'Pardubice', 'Sukova třída 1735');

insert into event (venue_id, name, start_at, base_price, is_active) values
(1, 'Koncert: Sample Band', '2026-02-10 19:00:00', 990.00, 1),
(2, 'Stand-up Night', '2026-02-15 20:00:00', 590.00, 1),
(3, 'Hokej: Domácí vs Hosté', '2026-02-20 18:00:00', 350.00, 1);

insert into seat (venue_id, sector, seat_row, seat_no, is_accessible) values
(1, 'A', 1, 1, 0),
(1, 'A', 1, 2, 0),
(1, 'A', 1, 3, 1),
(2, 'B', 1, 1, 0),
(2, 'B', 1, 2, 0),
(3, 'C', 1, 1, 0),
(3, 'C', 1, 2, 0);

insert into ticket (event_id, seat_id, price, is_sold) values
(1, 1, 990.00, 0),
(1, 2, 990.00, 0),
(1, 3, 990.00, 0),
(2, 4, 590.00, 0),
(2, 5, 590.00, 0),
(3, 6, 350.00, 0),
(3, 7, 350.00, 0);

insert into tag (name) values
('koncert'),
('sport'),
('komedie');

insert into event_tag (event_id, tag_id) values
(1, 1),
(2, 3),
(3, 2);

insert into customer (full_name, email, phone) values
('Jan Novák', 'jan.novak@email.cz', '777111222'),
('Petra Svobodová', 'petra.svobodova@email.cz', '777333444');
