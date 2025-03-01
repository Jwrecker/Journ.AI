import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import MemoryPage from "./pages/MemoryPage";

function App() {

  return (
    <Router>
      <nav className="p-4 bg-gray-800 text-white flex gap-4">
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>
      <div className="p-4">
        <Routes>
          <Route path="/" element={<MemoryPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
