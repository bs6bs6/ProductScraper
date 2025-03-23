// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ScraperPage from "./pages/ScraperPage";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="page-container">
        <nav style={{ marginBottom: "20px" }}>
          <Link to="/" style={{ marginRight: "20px" }}>Product List</Link>
          <Link to="/scrape">Scraper</Link>
        </nav>

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/scrape" element={<ScraperPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
