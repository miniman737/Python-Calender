#!/usr/bin/env python
#Marcus Ganz V00952336

import datetime
import sys
from typing import Counter

def main():
    x, y = 10, 1000
    countY = 0
    events = [[0 for x in range(x)] for y in range(y)]
    startDate = 0
    endDate = 0
    filename = None
    #print("hello world")
    for j in sys.argv:
        if "--start=" in j:
            line = j.split("=")[1]
            startY = line.split("/")[0]
            startyM  = line.split("/")[1]
            startD = line.split("/")[2]
            startDate = datetime.datetime(int(startY), int(startyM), int(startD))
        elif "--end=" in j:
            line = j.split("=")[1]
            endY = line.split("/")[0]
            endM = line.split("/")[1]
            endD = line.split("/")[2]
            endDate = datetime.datetime(int(endY), int(endM), int(endD))
        elif "--file=" in j:
            line = j.split("=")[1]
            filename = line
            f = open(filename, "r")
            readLines = f.readlines()

    #print(startDate)
    #print(endDate)

    

    for line in readLines:
        if "DTSTART:" in line:
            parse = line.split(":")[1]
            year = parse[0:4]
            month = parse[4:6]
            day = parse[6:8]
            hour = parse[9:11]
            min = parse[11:13]
            sec = parse[13:15]
            dayStart = datetime.datetime(int(year), int(month), int(day), int(hour), int(min), int(sec), 0)
            events[countY][0] = dayStart
        elif "DTEND:" in line:
            parse = line.split(":")[1]
            year = parse[0:4]
            month = parse[4:6]
            day = parse[6:8]
            hour = parse[9:11]
            min = parse[11:13]
            sec = parse[13:15]
            dayEnd = datetime.datetime(int(year), int(month), int(day), int(hour), int(min), int(sec), 0)
            events[countY][1] = dayEnd
        elif "LOCATION:" in line:
            parse = line.split(":")[1]
            location = parse
            events[countY][2] = location
        elif "SUMMARY:" in line:
            parse = line.split(":")[1]
            summary = parse
            events[countY][3] = summary
        elif "RRULE:" in line:
            parse = line.split("UNTIL=")[1]
            date = parse.split(";")[0]
            year = parse[0:4]
            month = parse[4:6]
            day = parse[6:8]
            hour = parse[9:11]
            min = parse[11:13]
            sec = parse[13:15]
            RepeatEnd = datetime.datetime(int(year), int(month), int(day), int(hour), int(min), int(sec), 0)
            events[countY][4] = RepeatEnd
            events[countY][5] = 1
            #time = date.split("T")[1]
            #date = date.split("T")[0]
        elif "END:VEVENT" in line:
            countY = countY + 1


    def repeatEvents(events, countY):
        counter = 0
        counterTwo = 0
        increment = datetime.timedelta(days = 7)
        y = 0
        countX = countY
        while y < countX:
            #print(events[2][5])
            check = int(events[y][5])
            if ( check != 0):
                comp = events[y][0]
                counter = y
                while comp + increment <= events[y][4]:
                    dayStart = comp + increment
                    dayEnd = events[y][1]
                    location = events[y][2]
                    summary = events[y][3]
                    countY = countY + 1
                    events.insert(countY,[dayStart, dayEnd, location, summary])
                    counter = counter + 1
                    counterTwo = counterTwo + 1
                    comp = comp + increment
            y += 1
        
        return events, countY
    
    events, countY = repeatEvents(events, countY)

    #print(events[10][0:5])
    #print(countY)
    
    #print(events[120][0])

    ##now we will sort all the events into a 2D array of valid events 
    def valid(gatheredEvents, startDate, endDate, countY):
        x = 10
        ValidEvents = [[0 for x in range(x)] for y in range(countY)]
        countX = 0
        count = 0
        while countX <= countY:
            #print(countX)
            compDay = gatheredEvents[countX][0]
            check = isinstance(compDay, int)
            if check is True:
                countX += 1
            else:
                compDay = datetime.datetime.date(compDay)
                #print(countX)
                if(compDay >= datetime.datetime.date(startDate) and compDay <= datetime.datetime.date(endDate)):
                    ValidEvents[count][0:10] = gatheredEvents[countX][0:10]
                    count = count + 1
                countX += 1
                
        
        GatheredValidEvents = [[0 for x in range(x)] for y in range(count)]
        GatheredValidEvents = ValidEvents[0:count][0:10]
        
        return GatheredValidEvents, count
    ValidEvents, countY = valid(events, startDate, endDate, countY)
    #print(ValidEvents)

    #now we will sort via chronological order
    def chrono(ValidEvents):
        ValidEvents.sort()
        return ValidEvents
    chronoEvents = chrono(ValidEvents)
    #print(chronoEvents)

    def output(chronoEvents, countY):
        x = 0
        prevDate = datetime.datetime(1, 1, 1, 1, 1, 1, 1)
        for count in chronoEvents:
            
                
            Sdate = chronoEvents[x][0]
            
            Edate = chronoEvents[x][1]
            location = chronoEvents[x][2]
            summary = chronoEvents[x][3]
            if (datetime.datetime.date(prevDate) != datetime.datetime.date(Sdate)) or (x == 0):
                prevDate = Sdate
                format = Sdate.strftime( "%B %d, %Y(%a)")
                dashAmmount = "-" * len(format)
                print(format)
                print(dashAmmount)
            elif(x != 0 and (datetime.datetime.date(prevDate) != datetime.datetime.date(Sdate))):
                print("")
            Shour = Sdate.strftime("%I:%M %p ")
            Shour = Shour.lstrip('0')
            Ehour = Edate.strftime("%I:%M %p: ")
            Ehour = Ehour.lstrip('0')
            summary = summary.strip("\n")
            location = location.strip("\n")
            string = Shour+ "to "+ Ehour+ summary+  " {{"+ location+ "}}"
            print(string)
            prevDate = Sdate
            x = x + 1
    output(chronoEvents, countY)


    


if __name__ == "__main__":
    main()