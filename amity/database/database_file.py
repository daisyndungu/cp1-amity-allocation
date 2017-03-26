import os
import sys
import sqlite3


class Database(object):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

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
            room_type VARCHAR(20),
            FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
            unique (employee_id, room_type));"""
        cursor.execute(sql_command)

    def close_db(self):
        return self.conn.close()

    def query_allocation_records(self):
        #
        cursor = self.cursor()
        load_allocation_query = """
            SELECT
                employee.name,
                employee.position,
                room.name,
                room.room_type
            FROM allocation
            LEFT OUTER JOIN employee
                ON employee.employee_id = allocation.employee_id
            LEFT OUTER JOIN room
                ON room.room_id = allocation.room_id;"""
        return cursor.execute(load_allocation_query)

    def query_unallocated_records(self):
        #
        cursor = self.cursor()
        load_unallocated_query = """
            SELECT
                employee.name,
                room_type
            FROM unallocated
            JOIN employee
                ON employee.employee_id = unallocated.employee_id;"""
        return cursor.execute(load_unallocated_query)

    def load_all_persons_from_db(self):
        cursor = self.cursor()
        data = "SELECT name, position FROM employee"
        return cursor.execute(data)

    def load_all_rooms_from_db(self):
        cursor = self.cursor()
        rooms_query = "SELECT name, room_type FROM room"
        return cursor.execute(rooms_query)
