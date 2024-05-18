create table prices (
    id bigint not null,
    price varchar(50) not null,
    car_id bigint,
    primary key (id)
);