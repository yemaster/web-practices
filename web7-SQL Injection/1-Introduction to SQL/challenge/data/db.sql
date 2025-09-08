/*
 * db.sql 文件
 *
 * 此文件用于初始化你的 MySQL 数据库。
 * 它将在 Docker 容器启动时运行，
 * 并执行所有的 SQL 命令来设置你的数据库。
 *
 * 你可以在这里创建你的数据库，创建表，
 * 插入数据，或执行任何其他的 SQL 命令。
 *
 * 例如：
 *   CREATE DATABASE IF NOT EXISTS your_database;
 *   USE your_database;
 *   CREATE TABLE your_table (...);
 *   INSERT INTO your_table VALUES (...);
 *
 * 请根据你的需要修改此文件，
 */

CREATE DATABASE ctf;
use ctf;

create table users (id varchar(300),username varchar(300),motto varchar(300));
create table secret_users (id varchar(300),username varchar(300),motto varchar(300));
insert into users values('1','admin','我是admin，今年20岁，拥有30年SQL开发经验');
insert into users values('2','yema','我是yema，今年20岁，拥有300年SQL开发经验');
insert into users values('3','yemama','我是yemama，今年20岁，拥有3000年SQL开发经验');
insert into users values('4','yemamama','我是yemamama，今年20岁，拥有30000年SQL开发经验');
insert into users values('5','yemamamama','我是yemamamama，今年20岁，拥有114514年SQL开发经验');
insert into secret_users values('1','flag','flag{test_flag}');