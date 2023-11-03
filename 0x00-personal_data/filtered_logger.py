#!/usr/bin/env python3
"""
A script
"""
from os import getenv
from typing import List
import re
import logging
import mysql.connector

PII_FIELDS = {"name", "email", "phone", "ssn", "password"}


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str):
    """
    A function that returns the log message obfuscated
    """
    prgex = '|'.join(map(re.escape, fields)) # \\1 == captured field
    return re.sub(f'({prgex})=[^\\{separator}]+', f'\\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list[str]):
        """
        Initialize class
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        A method to filter values in incoming log records using filter_datum.
        """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR
        )

def get_logger() -> logging.Logger:
    """
    A  function that takes no arguments and returns a logging.Logger object
    """
    newLogger = logging.getLogger("user_data")
    newLogger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    newLogger.propagate = False
    newLogger.addHandler(stream_handler)
    return newLogger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    A function that returns a connector to the database
    (mysql.connector.connection.MySQLConnection object).
    """
    db_name = getenv("PERSONAL_DATA_DB_NAME", "")
    db_host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_user = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pass = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    return mysql.connector.connect(
        host = db_host,
        port = 3306,
        user = db_user,
        password = db_pass,
        database = db_name
    )

def main() -> None:
    """
    a main function that takes no arguments and returns nothing.
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()

if __name__ == "__main__":
    main