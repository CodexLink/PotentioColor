'''
    RGB Name Definition Finder | Arduino UNO Sketch
    Created by Janrey "CodexLink" Licas
    Supported by Janos Angelo Jantoc and Johnell Casey Murillo Panotes
    Made for Embedded Systems | Prelim Case Study

    github.com/CodexLink

'''
// ! We can do this in multiple ways.
/*
    ! First Method, Local Server Query | RECOMMENDED TO DO SO.
    - We can have this working by letting arduino output all data by itself.
    And let another program in python interface through Serial Monitor and read
    all data outputted from the sketch. Then we require the use of MySQL Server
    to query by python program to output the color.

    * Second Method, Class Based Query
    - We can do this by using a custom library header and query all colors that corresponds
    to the potentiometer output. This requires only arduino and doesn't need a python program
    to output all colors.

    * Third Method, JSON Query Data
    - Although this method quite tricky, we aren't going to do it but added here when asked for possibly methods.
    This was an alternative method from second method. Though, this was quite practical on non-arduino programs.
    This can be done along with first method but using only JSON file or second method but again using only JSON
    as the content of the header file. Those can be contained with PROGMEM if possible done in second method.


*/
#include "Arduino.h"
//#include "CustomHeader.h"

// ! First Approach / Method | Class Based Configuration with Python Interfacer
const int LED_R = 11;
const int LED_G = 10;
const int LED_B = 9;
const int PTMTR_R = A1;
const int PTMTR_G = A3;
const int PTMTR_B = A5;

const int LIMITER_RANGE = 4;
bool isRGBReturn = false; // ! Required Adjustment, set this to 'true' if you want to return RGB Values in String Form.
// ! We can implement a button or a switch that can change the isRGBReturn value to any boolean values.

// ! Create a container of Struct for LED_DATA Containment. This was done for formality and indication that
// ! "Hey this one contains all LED Analog Values That You Will Output Later!"
struct LED_DATA
{
    unsigned char LED_R_DAT;
    unsigned char LED_G_DAT;
    unsigned char LED_B_DAT;
};

void normalizeOutput(bool colorTypeReturn);
/*
    ! INLINE FUNCTION normalizeOutput
    * - outputs color data based from parameters given.
        *   required parameters
        !       - colorTypeReturn, TYPE bool

        *   involved variables
        *       - R_DATA,TYPE uint8_t ~= unsigned char (range of 0-255), global
        *       - G_DATA,TYPE uint8_t ~= unsigned char (range of 0-255), global
        *       - B_DATA,TYPE uint8_t ~= unsigned char (range of 0-255), global

        !   returns a STRING of the following values:
        *       - RGB Numerical Values
        *       - Hex String with # Delimiter
*/

LED_DATA LED_PLCMNT; // * Initialize The Container To Be Stored With Analog Values of Potentiometer.

void setup()
{
    Serial.begin(9600); // ! Personal Preference. Keep Python Interfacer have the same value with this!

    // * We declare their intentions.
    pinMode(LED_R, OUTPUT);
    pinMode(LED_G, OUTPUT);
    pinMode(LED_B, OUTPUT);
    pinMode(PTMTR_R, INPUT);
    pinMode(PTMTR_G, INPUT);
    pinMode(PTMTR_B, INPUT);

    // * The Python Interfacer ignores this Serial Print Out. Go to that file to know more.
    Serial.println(F("/ RGB Name Color Definition Finder | -"));
    Serial.println(F("/ Arduino Serial Sketch"));
    Serial.println(F("/ Created by Janrey Licas, Janos Garcia Jantoc"));
    Serial.println(F("/ and Johnell Casey Murillo Panotes"));
    Serial.println();
    Serial.println(F("- Starting in 2 Seconds..."));
    delay(2000);
}

void loop()
{

    // ! We first have to store the data on last read and map them without dividing it raw.
    LED_PLCMNT.LED_R_DAT = map(analogRead(PTMTR_R), 0, 1023, 0, 255);
    LED_PLCMNT.LED_G_DAT = map(analogRead(PTMTR_G), 0, 1023, 0, 255);
    LED_PLCMNT.LED_B_DAT = map(analogRead(PTMTR_B), 0, 1023, 0, 255);

    // ! Then we have to print out for the user by this function.
    normalizeOutput(isRGBReturn);

    // ! We write the analog values to LED before we iterate from the beginning.
    analogWrite(LED_R, LED_PLCMNT.LED_R_DAT);
    analogWrite(LED_G, LED_PLCMNT.LED_G_DAT);
    analogWrite(LED_B, LED_PLCMNT.LED_B_DAT);
    delay(200); // ! Give time to interfacer to process data. Null value of this delay will result to noticeable delay. (~3 seconds!)
}

// ! Allow Ourselves To Complicate our Interfacer by adding styles for debugging experience.
void normalizeOutput(bool colorTypeReturn)
{
    if (colorTypeReturn)
    {
        // * The Code below in this scope constructs the following: (X, X, X), where Delimiter is '(' and ')'
        Serial.print(F("* RGB Output |> ("));
        Serial.print(LED_PLCMNT.LED_R_DAT);
        Serial.print(F(", "));
        Serial.print(LED_PLCMNT.LED_G_DAT);
        Serial.print(F(", "));
        Serial.print(LED_PLCMNT.LED_B_DAT);
        Serial.println(F(")"));
    }
    else
    {
        // * Since std::setfill and std::setw is not available in Arduino as they are from C++ libraries. We divide the output by delimiter
        Serial.print(F("* HEX Equiv |> #"));
        Serial.print(LED_PLCMNT.LED_R_DAT, HEX);
        Serial.print(F("|"));
        Serial.print(LED_PLCMNT.LED_G_DAT, HEX);
        Serial.print(F("|"));
        Serial.println(LED_PLCMNT.LED_B_DAT, HEX);
    }
    return;
}
'''
    RGB Name Definition Finder | Python Interfacer
    Created by Janrey "CodexLink" Licas
    Supported by Janos Angelo Jantoc and Johnell Casey Murillo Panotes
    Made for Embedded Systems | Prelim Case Study

    github.com/CodexLink

'''