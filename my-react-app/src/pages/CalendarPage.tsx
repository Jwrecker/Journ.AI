"use client"

import { useState } from "react"
import {
  format,
  addMonths,
  subMonths,
  startOfMonth,
  endOfMonth,
  eachDayOfInterval,
  isSameMonth,
  isToday,
} from "date-fns"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { useJournalEntries } from "@/hooks/useJournalEntries"

const CalendarPage = () => {
  const [currentMonth, setCurrentMonth] = useState(new Date())
  const { entries } = useJournalEntries()

  // Get days in current month
  const monthStart = startOfMonth(currentMonth)
  const monthEnd = endOfMonth(currentMonth)
  const daysInMonth = eachDayOfInterval({ start: monthStart, end: monthEnd })

  // Navigation functions
  const prevMonth = () => setCurrentMonth(subMonths(currentMonth, 1))
  const nextMonth = () => setCurrentMonth(addMonths(currentMonth, 1))
  const goToToday = () => setCurrentMonth(new Date())

  // Check if a date has entries
  const hasEntries = (date: Date) => {
    const dateStr = format(date, "yyyy-MM-dd")
    return entries[dateStr] && entries[dateStr].length > 0
  }

  // Days of week header
  const weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Journal Calendar</h1>
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={prevMonth}>
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <h2 className="text-xl font-semibold px-4">{format(currentMonth, "MMMM yyyy")}</h2>
          <Button variant="outline" onClick={nextMonth}>
            <ChevronRight className="h-4 w-4" />
          </Button>
          <Button variant="outline" onClick={goToToday} className="ml-2">
            Today
          </Button>
        </div>
      </div>

      <Card>
        <CardContent className="p-4">
          {/* Calendar grid */}
          <div className="grid grid-cols-7 gap-2">
            {/* Days of week header */}
            {weekDays.map((day) => (
              <div key={day} className="text-center font-medium p-2">
                {day}
              </div>
            ))}

            {/* Calendar days */}
            {Array.from({ length: monthStart.getDay() }).map((_, index) => (
              <div key={`empty-start-${index}`} className="p-2" />
            ))}

            {daysInMonth.map((day) => {
              const dateHasEntries = hasEntries(day)
              const isCurrentDay = isToday(day)

              return (
                <div
                  key={day.toISOString()}
                  className={`
                    p-2 h-24 border rounded-md relative
                    ${!isSameMonth(day, currentMonth) ? "text-muted-foreground" : ""}
                    ${isCurrentDay ? "border-primary" : "border-border"}
                    ${dateHasEntries ? "bg-primary/5" : ""}
                  `}
                >
                  <div className="absolute top-2 right-2">{day.getDate()}</div>

                  {dateHasEntries && (
                    <div className="absolute bottom-2 left-2 right-2">
                      <div className="h-2 w-2 bg-primary rounded-full" />
                    </div>
                  )}
                </div>
              )
            })}

            {Array.from({ length: 6 - monthEnd.getDay() }).map((_, index) => (
              <div key={`empty-end-${index}`} className="p-2" />
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="mt-6">
        <h3 className="text-lg font-medium mb-2">Legend</h3>
        <div className="flex items-center gap-2">
          <div className="h-3 w-3 bg-primary rounded-full" />
          <span>Days with journal entries</span>
        </div>
      </div>
    </div>
  )
}

export default CalendarPage

