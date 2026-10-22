import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Register from './Register';
import Login from './Login';
import Home from './Home';

function App() {
 

 
  
  return (
    <>
      <Router>
        <nav>
          <Link to="/">Home Page</Link> | <Link to="/login">Log in</Link> | <Link to="/register">Register</Link>
        </nav>

    
        <Routes>
          <Route path="/" element={<Home/>}/>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </Router>
    </>
    
  )
}

export default App
