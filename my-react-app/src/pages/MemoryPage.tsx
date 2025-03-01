import type React from "react"

import { useState, useRef, useEffect } from "react"
// import { Button } from "@/components/ui/button"
// import { Textarea } from "@/components/ui/textarea"
// import { Card } from "@/components/ui/card"

export default function ChatInterface() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: "/api/chat",
  })
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [isMobile, setIsMobile] = useState(false)

  // Check if the device is mobile
  useEffect(() => {
    const checkIfMobile = () => {
      setIsMobile(window.innerWidth < 768)
    }

    checkIfMobile()
    window.addEventListener("resize", checkIfMobile)

    return () => {
      window.removeEventListener("resize", checkIfMobile)
    }
  }, [])

  // Auto scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // Handle form submission
  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (input.trim() === "") return
    handleSubmit(e)
  }

  // Handle Ctrl+Enter to submit
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      const form = e.currentTarget.form
      if (form) {
        e.preventDefault()
        handleSubmit(new Event("submit") as any)
      }
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="border-b bg-white p-4">
        <h1 className="text-xl font-semibold text-center">AI Chat Interface</h1>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.length === 0 ? (
            <div className="text-center py-20">
              <h2 className="text-2xl font-semibold text-gray-700 mb-2">Welcome to AI Chat</h2>
              <p className="text-gray-500">Start a conversation with the AI assistant</p>
            </div>
          ) : (
            messages.map((message) => (
              <Card
                key={message.id}
                className={`p-4 ${
                  message.role === "user" ? "bg-white border-gray-200" : "bg-primary/5 border-primary/10"
                }`}
              >
                <div className="flex items-start gap-3">
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.role === "user" ? "bg-blue-100 text-blue-600" : "bg-primary/10 text-primary"
                    }`}
                  >
                    {message.role === "user" ? <User size={18} /> : <Bot size={18} />}
                  </div>
                  <div className="flex-1 prose max-w-none">
                    <div className="whitespace-pre-wrap">{message.content}</div>
                  </div>
                </div>
              </Card>
            ))
          )}
          {isLoading && (
            <Card className="p-4 bg-primary/5 border-primary/10">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center flex-shrink-0">
                  <Bot size={18} />
                </div>
                <div className="flex-1">
                  <div className="flex space-x-2">
                    <div
                      className="h-2 w-2 bg-primary/40 rounded-full animate-bounce"
                      style={{ animationDelay: "0ms" }}
                    ></div>
                    <div
                      className="h-2 w-2 bg-primary/40 rounded-full animate-bounce"
                      style={{ animationDelay: "150ms" }}
                    ></div>
                    <div
                      className="h-2 w-2 bg-primary/40 rounded-full animate-bounce"
                      style={{ animationDelay: "300ms" }}
                    ></div>
                  </div>
                </div>
              </div>
            </Card>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t bg-white p-4">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={onSubmit} className="flex flex-col space-y-2">
            <div className="relative">
              <Textarea
                value={input}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                placeholder="Type your message here..."
                className="pr-12 resize-none min-h-[80px] max-h-[200px]"
                rows={isMobile ? 2 : 3}
              />
              <Button
                type="submit"
                size="icon"
                className="absolute bottom-2 right-2"
                disabled={isLoading || input.trim() === ""}
              >
                <SendIcon size={18} />
              </Button>
            </div>
            <div className="text-xs text-gray-500 text-center">Press Ctrl + Enter to send</div>
          </form>
        </div>
      </div>
    </div>
  )
}

