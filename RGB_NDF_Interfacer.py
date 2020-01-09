'''
    RGB Name Definition Finder | Python Interfacer
    Created by Janrey "CodexLink" Licas
    Supported by Janos Angelo Jantoc and Johnell Casey Murillo Panotes
    Made for Embedded Systems | Prelim Case Study

    github.com/CodexLink

'''
from os import system as CommandLine
from sys import exit as Terminate
from time import sleep as delay

import pymysql as MySQLConnector
import serial as SerialLib
import serial.tools.list_ports as SerialTools

# * A Wrapper Class that contains all MySQL functions. Formalized for Future Use.
# ! This Class contains minimal functions that is wrapped. Unlike PyODBC, it contains additional function that can be used for better debugging experience.
class MySQLEssentialHelper(object):
    # * We initialize our MySQL by __init__ without using any OpenCon() or doing it manually.
    def __init__(self, ServerHost=None, UCredential=None, PCredential=None, DB_Target=None):
        try:
            self.MySQLDataWire = MySQLConnector.connect(host=ServerHost, user=UCredential, password=PCredential, db=DB_Target, charset='utf8mb4', cursorclass=MySQLConnector.cursors.DictCursor)

        except MySQLConnector.MySQLError as OpenConErrorMsg:
            print('Connection Error | Cannot Connect to Database. Detailed Info |> %s' %
                  OpenConErrorMsg)
            Terminate()  # ! Terminate the program, when we're unable to connect to the database.

    # ! Used for querying data in database.
    def MySQL_ExecuteState(self, ExecuteStatement=None):
        try:
            cursorSet = self.MySQLDataWire.cursor()
            cursorSet.execute(ExecuteStatement)
            return cursorSet.fetchone() # ! Since it outputs a number of rows. We gonna fetch the first value.

        except MySQLConnector.MySQLError as ExecErrMsg:
            print('Execution State Error | Please check your statements. Detailed Info |> %s' % ExecErrMsg)

    # ! Not required in this case study but required for formality.
    def MSSQL_CommitData(self, SourceFunction=None):
        try:
            return self.MSSQLDataWire.commit()

        except MySQLConnector.MySQLError as CommitError:
            print(
                'Commitment Error | [Unexplainable Reason]. Detailed Info |> %s' % CommitError)

# Main Driver Class for RGB Interface to Database
class RGBInterfacer(MySQLEssentialHelper):
    # On Starting Point we have to supply the given arguments to __init__() function.
    # ! Because we have to initialize the class from the object itself.
    def __init__(self, COMPort=None, BaudRate=None):
        try:
            # ! Super Function
            # ! We have to initialize superclass 'MySQLEssentialHelper' to gather functions from 'that' class.
            super().__init__(ServerHost='localhost', UCredential='root', PCredential=None, DB_Target='RGB_DataSet')
            self.AVInt = SerialLib.Serial(port=COMPort, baudrate=BaudRate)

            # * We save last com port to be used by def isDeviceConnected() for Device isAlive Status Check.
            self.LastCOMPort = COMPort

        except SerialLib.SerialException as SerialErr:
            print(
                'Serial Interface Error | COM Port or Baudrate is Invalid. Detailed Info |> %s' % SerialErr)
            Terminate()

    # * Extra | LITERALLY Needed for Checking if Device COM Port still exists.
    def isDeviceConnected(self):
        # We check recently instantiated object attribute if Serial Monitoring is really OPEN.
        if self.AVInt.is_open:
            # If that is opened, we iterate to the Library declared with the name of SerialTools
            for ports in SerialTools.comports():
                if ports.device == self.LastCOMPort:
                    return True # ! We identify each and if one is one of them then return true.
                else:
                    continue
        else:
            return False # ! If none is valid or equivalent to the supplemented arguments then we return False and terminate the program.

    # ! STEP 1 | First we have to gather the data from the serial from Arduino.
    # * This function reads the whole serial data line given by Arduino. All data is here unprocessed except data encoding which is utf-8.
    def gatherData(self):
        # ! We get the data and encode them to read them better without any special characters processing and strip all **SPACES**.
        dataSerial = self.AVInt.readline().decode('utf-8', errors='ignore').strip()

        # ! We then read the first character by [:1] and ensure that first character is '*' then check as well if the dataSerial is actually NOT EMPTY.
        if dataSerial[:1] == '*' and dataSerial is not None:
            self.interpretData(dataSerial)
        else:
            return False # * do nothing

    # ! STEP 2 | Second, we pass the data from 'this' function to interpret the data received recently from gatherData function.
    def interpretData(self, stringReceived):
        # * The data that is being sent by Arduino based from Sketch has its delimeter from the first character line.
        # ! The python program wants to read data that is important that is delimited with # or ( characters.

        # ! Also take note that, the program can interpret RGB and HEX data at the same time and can also switch from each other.

        # ! Read HEX Lines Statement
        if "#" in stringReceived: # * If the string contains '#' on it
            # * Starting from here, result of BaseHexData is ['* Hex Equiv |>', '#00|00|00']
            # * Then we access the 2nd element (1st index) which then we would get #00|00|00
            # * After that, we split them with '|' and get the value of each, seperated into 3 indexes for each has its own value of hexadecimal.
            # * Therefore, for instance, [0] = FA, [1] = FF, [2] = CD. Those are assigned to each R, G, and B Variables below.
            BaseHexData = stringReceived.split('#')[1].split('|')
            # * At some point, we have to convert some arguments from HEX into an DEC.
            # * TO do this we have to supply HEX String to INT function and type Base 16 as a second parameter.
            RedValue = int(BaseHexData[0], 16)
            GreenValue = int(BaseHexData[1], 16)
            BlueValue = int(BaseHexData[2], 16)
            # * Uncomment the line below and add print function to see the result.
            # ! CombinedHexString = '#%s%s%s' % (BaseHexData[0].zfill(2), BaseHexData[1].zfill(2), BaseHexData[2].zfill(2))
            # ! print(CombineHexString)
            # ! Then we pass this to displayColor function. Please refer to the function itself to understand what parameters need to be supplemented.

            self.displayColors(BaseHexData[0], BaseHexData[1], BaseHexData[2], RedValue, GreenValue, BlueValue)

        # ! Read RGB Lines Statement
        elif "(" in stringReceived:
            # * Starting from here, result of BaseRGBData is ['* RGB Output |> (', '100, 255, 244)]
            # * And then, split all those values by ','. Which we would get all of R, G, and B Values by accessing 3 index from BaseRGBData variable.
            BaseRGBData = stringReceived.split('(')[1].split(',')
            # * Since we noticed we have a ')' from the third index. We have to replace it from ')' to null.
            BaseRGBData[2] = BaseRGBData[2].replace(')', '')

            # ! This one goes complex due to multiple casting of type change and strip with character accessing.

            # * first we have to undestand that the inside of it, is we have to strip all spaces from those numbers
            # * From (100,  255,  244) -> (100,255,244)
            # * Then we convert the string numbers to literals by casting it with int on them.
            # * Then we cast HEX from integer numbers. The output of 15 would probably be 0xFF.
            # * Since we dont want 0x on them we have to access only the 2nd index / element of the output which starting from F which would output FF.
            RedHEXValue = hex(int(BaseRGBData[0].strip()))[2:]
            GreenHEXValue = hex(int(BaseRGBData[1].strip()))[2:]
            BlueHEXValue = hex(int(BaseRGBData[2].strip()))[2:]

            # Uncomment the line below and add print function to see the result.
            # ConvertedHexString = '#%s%s%s' % (hex(int(BaseRGBData[0].strip()))[2:], hex(int(BaseRGBData[1].strip()))[2:], hex(int(BaseRGBData[2].strip()))[2:])
            # ! print(ConvertedHexString)
            # ! Then we pass this to displayColor function. Please refer to the function itself to understand what parameters need to be supplemented.

            # * In this variable, we strip EACH index string. We cannot do this from the first line of data processing because they are LIST.
            self.displayColors(RedHEXValue, GreenHEXValue, BlueHEXValue, BaseRGBData[0].strip(), BaseRGBData[1].strip(), BaseRGBData[2].strip())
        else:
            pass # do nothing.

    # ! STEP 3 | Third, we query from the database by receiving the interpretedData.
    # * This function doesn't need data error handling due to interpretData has sterelized the data.
    # * But we still need it specifically for exceeded data from database.

    def displayColors(self, RHex, GHex, BHex, RValue, GValue, BBlue):
        try:
            ColorName = self.MySQL_ExecuteState("SELECT ColorName FROM RGB WHERE HexValue = '#%s%s%s'" % (RHex.zfill(2).upper(), GHex.zfill(2).upper(), BHex.zfill(2).upper()))
            # ! Output Structure of ColorName depends if they find a row that matches the query given values.
            # * When query returns None, it does NOT defined itself as LIST because there is nothing to output.
            # * Therefore we run and display the color as unknown.
            if ColorName is None:
                lastColorSaved = 'Unknown'
            else:
                # ! This code line is shorthand of IF and ELSE. Please research about this one to understand how it works.
                # * But the clue is, The VALUE is THIS IF Value is True or ELSE this will be the value when the value is false
                lastColorSaved = ColorName['ColorName'] if ColorName['ColorName'] is not None else lastColorSaved

            # ! We output the result now.
            return print('HEX |> #%s%s%s | RGB |> (%s, %s, %s) | Color: %s' % (RHex.zfill(2).upper(), GHex.zfill(2).upper(), BHex.zfill(2).upper(), RValue, GValue, BBlue, lastColorSaved))

        # ! Recently, due to error from ColorName value, I was able to bypass it with this I GUESS.
        except TypeError:
            pass

if __name__ == '__main__':
    CommandLine('CLS')
    print('RGB Interfacer for Arduino Sketch | Serial Receiver')
    print("Created by Janrey Licas, Janos Garcia Jantoc and Johnell Casey Murillo Panotes")
    delay(1.5)

    # * We initialize this class with parameters.
    PrimaryClass = RGBInterfacer('COM12', 9600)
    try:
        while PrimaryClass.isDeviceConnected():
            PrimaryClass.gatherData()
        else:
            # ! We end program with exception raised to print out data.
            raise Exception
    except:
        print('Device Communication Error | Device COM Port Supplemented Suddenly Disconnected.')
        Terminate()
'''
    RGB Name Definition Finder | Python Interfacer
    Created by Janrey "CodexLink" Licas
    Supported by Janos Angelo Jantoc and Johnell Casey Murillo Panotes
    Made for Embedded Systems | Prelim Case Study

    github.com/CodexLink

'''