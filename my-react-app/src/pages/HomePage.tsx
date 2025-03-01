"use client"

import { useState } from "react"
import { Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Card } from "@/components/ui/card"
import api from "@/utils/api";

const myApi = api();

type Message = {
  id: string
  content: string
  role: "user" | "assistant"
  timestamp: Date
}

const MemoryPage = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content:
        "Hello! I'm your journal assistant. I can help you reflect on your entries or answer questions about your journaling experience. How can I help you today?",
      role: "assistant",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async () => {
    if (!input.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    // Simulate AI response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `I've processed your message: "${input}". This is a simulated response. In a real application, this would connect to an AI service to generate a meaningful response based on your journal entries and question.`,
        role: "assistant",
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])
      setIsLoading(false)
    }, 1000)
  }

  const handleTestApi = async () => {
    console.log("Testing API");
    const response = await myApi.testapi();
    console.log(response);
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className="flex items-start max-w-[80%] gap-2">
              {message.role === "assistant" && (
                <Avatar className="h-8 w-8">
                  <AvatarImage src="/placeholder-avatar.jpg" />
                  <AvatarFallback>AI</AvatarFallback>
                </Avatar>
              )}
              <Card className={`p-3 ${message.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"}`}>
                <p className="text-sm">{message.content}</p>
              </Card>
              {message.role === "user" && (
                <Avatar className="h-8 w-8">
                  <AvatarImage src="/placeholder-avatar.jpg" />
                  <AvatarFallback>ME</AvatarFallback>
                </Avatar>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-start max-w-[80%] gap-2">
              <Avatar className="h-8 w-8">
                <AvatarFallback>AI</AvatarFallback>
              </Avatar>
              <Card className="p-3 bg-muted">
                <p className="text-sm">Thinking...</p>
              </Card>
            </div>
          </div>
        )}
      </div>
      <div className="border-t p-4">
        <div className="flex gap-2">
          <Textarea
            placeholder="Ask me anything about your journal..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 min-h-[60px]"
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault()
                handleSendMessage()
              }
            }}
          />
          <Button onClick={handleSendMessage} disabled={!input.trim() || isLoading} className="self-end">
            <Send className="h-4 w-4" />
            <span className="sr-only">Send</span>
          </Button>
          <Button onClick={handleTestApi}> Test Api </Button>
        </div>
      </div>
    </div>
  )
}

export default MemoryPage

