from enum import Enum
import sqlite3
import sys
import traceback

class OutputType(Enum):
    SQLITE = "sqlite"

    def __str__(self):
        return self.value

class StorageHandler:
    def __init__(self, outputType, outputPath):
        if outputType == OutputType.SQLITE:
            self.__createTable__(outputPath)
        else:
            NotImplementedError()

    def __createTable__(self, outputPath):
        self.conObj = sqlite3.connect(outputPath)
        self.cursor = self.conObj.cursor()
        creationQuery = "CREATE TABLE IF NOT EXISTS chat (date VARCHAR(15) NOT NULL, time VARCHAR(15) NOT NULL, senderName, content VARCHAR (1000) NOT NULL)"
        self.cursor.execute(creationQuery)
    
    def __del__(self):
        self.conObj.close()
    
    def saveLine(self, parsedLine):
        insertQuery = "INSERT into chat VALUES (?,?,?,?)"
        try:
            self.cursor.execute(insertQuery, [parsedLine["date"], parsedLine["time"], parsedLine["senderName"], parsedLine["content"]])
            self.conObj.commit()
        except sqlite3.Error as er:
            # TODO
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))