import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Items from './pages/Items'

function App() {
  const token = localStorage.getItem('token')

  return (
    <Routes>
      <Route path="/" element={token ? <Navigate to="/items" /> : <Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/items" element={token ? <Todos /> : <Navigate to="/login" />} />
    </Routes>
  )
}

export default App