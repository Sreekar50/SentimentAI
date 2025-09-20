// Register.js
import React, { useState } from "react";
import axios from "axios";
import { TextField, Button, Card, CardContent, Typography, Alert, CircularProgress } from "@mui/material";

const Register = ({ onSwitchToLogin }) => {
  const [credentials, setCredentials] = useState({ 
    username: '', 
    password: '', 
    confirmPassword: '' 
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleInputChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    
    if (credentials.password !== credentials.confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/register/", {
        username: credentials.username,
        password: credentials.password
      });
      setSuccess('Registration successful! Please login.');
      setCredentials({ username: '', password: '', confirmPassword: '' });
    } catch (error) {
      setError(error.response?.data?.error || 'Registration failed');
    }
    
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "400px", margin: "50px auto", padding: "20px" }}>
      <Card variant="outlined">
        <CardContent>
          <Typography variant="h5" component="h1" gutterBottom align="center">
            Register
          </Typography>
          
          {error && (
            <Alert severity="error" style={{ marginBottom: "16px" }}>
              {error}
            </Alert>
          )}
          
          {success && (
            <Alert severity="success" style={{ marginBottom: "16px" }}>
              {success}
            </Alert>
          )}
          
          <form onSubmit={handleRegister}>
            <TextField
              fullWidth
              label="Username"
              name="username"
              value={credentials.username}
              onChange={handleInputChange}
              margin="normal"
              required
            />
            
            <TextField
              fullWidth
              label="Password"
              name="password"
              type="password"
              value={credentials.password}
              onChange={handleInputChange}
              margin="normal"
              required
            />
            
            <TextField
              fullWidth
              label="Confirm Password"
              name="confirmPassword"
              type="password"
              value={credentials.confirmPassword}
              onChange={handleInputChange}
              margin="normal"
              required
            />
            
            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={loading}
              style={{ marginTop: "24px", marginBottom: "16px" }}
            >
              {loading ? <CircularProgress size={24} /> : 'Register'}
            </Button>
            
            <Button
              fullWidth
              variant="text"
              onClick={onSwitchToLogin}
            >
              Already have an account? Login
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default Register;
