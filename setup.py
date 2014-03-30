#ZZcat setup.py | grep '#=' | awk -F'#=' '{print $2}'
#=mkdir static
#=mkdir templates
#=echo "
#=drop table if exists users;
#=create table users(
#=id integer primary key autoincrement,
#=username text not null,
#=mpassword text not null,
#=email text,
#=date text, 
#=hint text, 
#=admin text, 
#=author text, 
#=view text 
#=);" > schema.sql
#=
#=echo "
#=drop table if exists blog; 
#=create table blog (
#=id INTEGER PRIMARY KEY autoincrement, 
#=title TEXT, 
#=author TEXT,
#=username TEXT, 
#=content TEXT, 
#=approved TEXT,
#=published TEXT,
#=date TEXT);" >> schema.sql
#=sqlite3 ./multi.db < schema.sql

#=sqlite3 multi.db "insert into users (username,mpassword,admin) values ('count', 'dune02','Yes');" 
#=sqlite3 multi.db "insert into blog (title,author,username,content,approved,published,date) values ('Welcome 1', 'William Gunnells','Hello world','Yes','Yes','3/29/2014);" 
#=sqlite3 multi.db "insert into blog (title,author,username,content,approved,published,date) values ('Welcome 2', 'John Doe','Any data','Yes','Yes','3/29/2014);" 
#=sqlite3 multi.db "insert into blog (title,author,username,content,approved,published,date) values ('Welcome 3', 'Peter Jackson','Add stuff here','No','No','3/29/2014);" 
#=sqlite3 multi.db "insert into blog (title,author,username,content,approved,published,date) values ('Welcome 4', 'Jack Joe','test test','No','No','3/29/2014);" 
