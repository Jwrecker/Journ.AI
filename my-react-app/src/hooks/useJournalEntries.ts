"use client"

import { useState, useEffect } from "react"

export type JournalEntry = {
  prompt: string
  response: string
  timestamp: string
}

export type JournalEntries = Record<string, JournalEntry[]>

export const useJournalEntries = () => {
  const [entries, setEntries] = useState<JournalEntries>(() => {
    const savedEntries = localStorage.getItem("journalEntries")
    return savedEntries ? JSON.parse(savedEntries) : {}
  })

  // Save entries to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem("journalEntries", JSON.stringify(entries))
  }, [entries])

  // Add a new entry
  const addEntry = (date: string, entry: JournalEntry) => {
    setEntries((prev) => {
      const dateEntries = prev[date] || []
      return {
        ...prev,
        [date]: [...dateEntries, entry],
      }
    })
  }

  // Get entries for a specific date
  const getEntriesForDate = (date: string): JournalEntry[] => {
    return entries[date] || []
  }

  // Get all dates that have entries
  const getDatesWithEntries = (): string[] => {
    return Object.keys(entries)
  }

  return {
    entries,
    addEntry,
    getEntriesForDate,
    getDatesWithEntries,
  }
}

