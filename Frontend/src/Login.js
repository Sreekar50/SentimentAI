import React, { useState } from "react";
import axios from "axios";
import { TextField, Button, Card, CardContent, Typography, Alert, CircularProgress } from "@mui/material";

const Login = ({ onLoginSuccess, onSwitchToRegister }) => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      console.log('Attempting login for:', credentials.username);
      
      const response = await axios.post(
        "http://127.0.0.1:8000/api/login/", 
        credentials,
        {
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );
      
      console.log('Login successful:', response.data);
      
      onLoginSuccess({
        username: response.data.username,
        user_id: response.data.user_id,
        token: response.data.token
      });
      
    } catch (error) {
      console.error('Login error:', error);
      setError(error.response?.data?.error || 'Login failed');
    }
    
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "400px", margin: "50px auto", padding: "20px" }}>
      <Card variant="outlined">
        <CardContent>
          <Typography variant="h5" component="h1" gutterBottom align="center">
            Login
          </Typography>
          
          {error && (
            <Alert severity="error" style={{ marginBottom: "16px" }}>
              {error}
            </Alert>
          )}
          
          <form onSubmit={handleLogin}>
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
            
            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={loading}
              style={{ marginTop: "24px", marginBottom: "16px" }}
            >
              {loading ? <CircularProgress size={24} /> : 'Login'}
            </Button>
            
            <Button
              fullWidth
              variant="text"
              onClick={onSwitchToRegister}
            >
              Don't have an account? Register
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default Login;
