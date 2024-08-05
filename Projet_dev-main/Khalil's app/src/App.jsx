import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import AdminPage from './pages/AdminPage';
import UserPage from './pages/UserPage';
import { AuthProvider, useAuth } from './pages/AuthContext';
import ProtectedRoute from './pages/ProtectedRoute';

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Navbar bg="light" expand="lg">
          <Navbar.Brand href="/">  K @ D  </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ml-auto">
              <Nav.Link as={Link} to="/">Home</Nav.Link>
              <Nav.Link as={Link} to="/login">Login</Nav.Link>
              <AuthNavLinks />
            </Nav>
          </Navbar.Collapse>
        </Navbar>

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/admin" element={<ProtectedRoute role="admin"><AdminPage /></ProtectedRoute>} />
          <Route path="/user" element={<ProtectedRoute role="user"><UserPage /></ProtectedRoute>} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};


const AuthNavLinks = () => {
  const { token, role, logout } = useAuth();

  if (!token) return null;

  return (
    <>
      <Nav.Link as={Link} to={`/${role}`}>{role === 'admin' ? 'Admin Page' : 'User Page'}</Nav.Link>
      <Nav.Link onClick={logout}>Logout</Nav.Link>
    </>
  );
};

export default App;