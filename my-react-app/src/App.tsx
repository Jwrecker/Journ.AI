import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Layout from "./components/layout"
import HomePage from "./pages/HomePage"
import MemoryPage from "./pages/MemoryPage"
import CalendarPage from "./pages/CalendarPage"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="memory" element={<MemoryPage />} />
          <Route path="calendar" element={<CalendarPage />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App

