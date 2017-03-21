import os
import sys
import sqlite3


class Database(object):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        """Commit pending changes"""
        return self.conn.commit()

    def create_table(self):
        cursor = self.cursor()
        sql_command = """
            CREATE TABLE IF NOT EXISTS employee (
            employee_id  INTEGER PRIMARY KEY,
            name VARCHAR(30),
            position VARCHAR(10),
            unique (name, position));"""
        cursor.execute(sql_command)

        sql_command = """
            CREATE TABLE IF NOT EXISTS room (
            room_id  INTEGER PRIMARY KEY,
            name VARCHAR(30),
            room_type VARCHAR(20),
            unique (name, room_type));"""
        cursor.execute(sql_command)

        sql_command = """
            CREATE TABLE IF NOT EXISTS allocation (
            allocation_id INTEGER PRIMARY KEY,
            employee_id INTEGER,
            room_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
            FOREIGN KEY (room_id) REFERENCES room(room_id),
            unique (employee_id, room_id));"""
        cursor.execute(sql_command)

        sql_command = """
            CREATE TABLE IF NOT EXISTS unallocated (
            unallocated_id INTEGER PRIMARY KEY,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
            );"""
        cursor.execute(sql_command)

    def close_db(self):
        return self.conn.close()
