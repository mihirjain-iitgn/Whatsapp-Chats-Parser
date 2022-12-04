from enum import Enum
from line_processor import LineProcessor, MessageType
from storage_handler import StorageHandler, OutputType
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Whatsapp chat parser')
parser.add_argument('--in_path', help ='path for the chats file', required = True)
parser.add_argument('--out_type', help ='output file type', type = OutputType, default = OutputType.SQLITE, choices = list(OutputType))
parser.add_argument('--out_path', help ='output file path', default = "./chat.db")

def handleErrState():
    print("Program in unexpected state, MessageType.LAST_MSSG_CONT receieved but lastMessage is None")
    os.remove(outputPath)
    sys.exit()

if __name__ == '__main__':
    args = parser.parse_args()
    inputPath = args.in_path
    outputType = args.out_type
    outputPath = args.out_path
    with open(inputPath, "r", encoding = "UTF-8") as fp:
        lineProcessor = LineProcessor()
        storageHandler = StorageHandler(outputType, outputPath)
        lastMessage = None
        for line in fp:
            parsedLine = lineProcessor.processLine(line)
            match parsedLine["type"]:
                case MessageType.NEW_MSSG:
                    if lastMessage:
                        storageHandler.saveLine(lastMessage)
                    lastMessage = parsedLine["data"]
                case MessageType.LAST_MSSG_CONT:
                    if lastMessage:
                        lastMessage["content"] += parsedLine["data"]["content"]
                    else:
                        handleErrState()
                case MessageType.INFO_MSSG:
                    if lastMessage:
                        storageHandler.saveLine(lastMessage)
                        lastMessage = None
                    storageHandler.saveLine(parsedLine["data"])
        print("Execution complete, chats stored in %s file a %s" % (OutputType, outputPath))