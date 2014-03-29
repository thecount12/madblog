
drop table if exists users;
create table users(
id integer primary key autoincrement,
username text not null,
mpassword text not null,
email text,
date text, 
hint text, 
admin text, 
author text, 
view text 
);

drop table if exists blog; 
create table blog (
id INTEGER PRIMARY KEY autoincrement, 
title TEXT, 
author TEXT,
username TEXT, 
content TEXT, 
approved TEXT,
published TEXT,
date TEXT);
