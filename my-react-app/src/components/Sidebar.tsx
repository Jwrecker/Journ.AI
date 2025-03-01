import { NavLink } from "react-router-dom"
import { Home, Calendar, MessageSquare } from "lucide-react"

const Sidebar = () => {
  return (
    <aside className="w-64 bg-card border-r border-border h-screen p-4">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-primary">Journal AI</h1>
      </div>
      <nav className="space-y-2">
        <NavLink
          to="/"
          className={({ isActive }) =>
            `flex items-center p-2 rounded-lg transition-colors ${
              isActive ? "bg-primary/10 text-primary" : "hover:bg-muted text-foreground"
            }`
          }
        >
          <Home className="mr-2 h-5 w-5" />
          <span>Home</span>
        </NavLink>
        <NavLink
          to="/memory"
          className={({ isActive }) =>
            `flex items-center p-2 rounded-lg transition-colors ${
              isActive ? "bg-primary/10 text-primary" : "hover:bg-muted text-foreground"
            }`
          }
        >
          <MessageSquare className="mr-2 h-5 w-5" />
          <span>Memory</span>
        </NavLink>
        <NavLink
          to="/calendar"
          className={({ isActive }) =>
            `flex items-center p-2 rounded-lg transition-colors ${
              isActive ? "bg-primary/10 text-primary" : "hover:bg-muted text-foreground"
            }`
          }
        >
          <Calendar className="mr-2 h-5 w-5" />
          <span>Calendar</span>
        </NavLink>
      </nav>
    </aside>
  )
}

export default Sidebar

