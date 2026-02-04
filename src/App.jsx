import { BrowserRouter, Routes, Route } from "react-router-dom";
import Chat from "./Chat";
import Appointments from "./Appointments";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/appointments" element={<Appointments />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
