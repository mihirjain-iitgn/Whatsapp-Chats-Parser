import re
from enum import Enum

class MessageType(Enum):
    NEW_MSSG = 1
    LAST_MSSG_CONT = 2
    INFO_MSSG = 3

class LineProcessor:
    
    def __init__(self):
        datePattern = '[0-3][0-9]\\/[0-1][0-9]\\/[0-9][0-9]'
        timePattern = '[0-1]?[0-9]:[0-6][0-9]\\s[ap]m'
        contentPattern = '.+'
        self.messagePattern = r"^(%s),\s(%s)\s-\s(%s)$"%(datePattern, timePattern, contentPattern)
        self.userContentPattern = r"(.+):(.+)"
    
    def processLine(self, line):
        parsedLine = re.search(self.messagePattern, line.rstrip())
        if parsedLine:
            parsedContent = re.search(self.userContentPattern, parsedLine.group(3))
            if parsedContent:
                return {
                    "type" : MessageType.NEW_MSSG,
                    "data" : {
                        "date" : parsedLine.group(1),
                        "time" : parsedLine.group(2),
                        "senderName" : parsedContent.group(1),
                        "content" : parsedContent.group(2)
                    }
                }
            else:
                return {
                    "type" : MessageType.INFO_MSSG,
                    "data" : {
                        "date" : parsedLine.group(1),
                        "time" : parsedLine.group(2),
                        "senderName" : "N/A",
                        "content" : parsedLine.group(3)
                    }
                }
        else:
            return {
                "type" : MessageType.LAST_MSSG_CONT,
                "data" : {
                    "content" : line
                }
            }