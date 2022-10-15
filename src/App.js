import "./App.css";
import FileUpload from "./FileUpload";
import Dashboard from "./Dashboard";
import Home from "./Home";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/donate/" element={<FileUpload />} />
          <Route path="/dashboard/" element={<Dashboard />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
