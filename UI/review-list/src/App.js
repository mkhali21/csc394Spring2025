import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./Home";
import Restaurant from "./Restaurants";

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Home</Link> | <Link to="/restaurants">Restaurants</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/restaurants" element={<Restaurant />} />
      </Routes>
    </Router>
  );
}

export default App;
