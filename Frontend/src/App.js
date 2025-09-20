import React, { useState, useEffect } from "react";
import axios from "axios";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from "recharts";
import { TextField, Button, Card, CardContent, Typography, CircularProgress, Alert } from "@mui/material";
import Login from "./Login";
import Register from "./Register";
import Header from "./Header";

const COLORS = ["#0088FE", "#FF8042"];

axios.defaults.withCredentials = true;

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [token, setToken] = useState('');
  const [showLogin, setShowLogin] = useState(true);
 
  const [url, setUrl] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    const savedToken = localStorage.getItem('authToken');
    const savedUsername = localStorage.getItem('username');
    
    if (savedToken && savedUsername) {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/auth-status/", {
          headers: {
            'Authorization': `Bearer ${savedToken}`
          }
        });
        
        if (response.data.authenticated) {
          setIsAuthenticated(true);
          setUsername(savedUsername);
          setToken(savedToken);
        } else {
          clearAuthData();
        }
      } catch (error) {
        console.log('Auth check failed:', error);
        clearAuthData();
      }
    }
  };

  const clearAuthData = () => {
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('username');
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
    setUsername('');
    setToken('');
  };

  const handleLoginSuccess = (userData) => {
    setIsAuthenticated(true);
    setUsername(userData.username);
    setToken(userData.token);
    
    localStorage.setItem('isAuthenticated', 'true');
    localStorage.setItem('username', userData.username);
    localStorage.setItem('authToken', userData.token);
  };

  const handleLogout = async () => {
    try {
      await axios.post("http://127.0.0.1:8000/api/logout/", {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
    
    clearAuthData();
  };

  const handleAnalyze = async () => {
    if (!url.trim()) {
      setError('Please enter a valid URL');
      return;
    }

    setLoading(true);
    setError('');
    setData(null);

    try {
      console.log('Sending request to analyze:', url);
      console.log('Using token:', token);
      
      const response = await axios.post(
        "http://127.0.0.1:8000/api/fetch_comments/", 
        { url: url.trim() },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );

      console.log('Response received:', response.data);
      setData(response.data);
      
    } catch (error) {
      console.error("Error fetching data:", error);
      
      if (error.response) {
        if (error.response.status === 401) {
          setError('Authentication failed. Please login again.');
          clearAuthData();
        } else if (error.response.status === 400) {
          setError(error.response.data.error || 'Invalid request. Please check the URL.');
        } else {
          setError(error.response.data.error || 'Server error occurred');
        }
      } else if (error.request) {
        setError('Network error. Please check if the server is running.');
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div>
        <div style={{ textAlign: "center", padding: "20px" }}>
          <Typography variant="h3" component="h1" gutterBottom>
            Social Media Sentiment Analysis
          </Typography>
        </div>
        
        {showLogin ? (
          <Login 
            onLoginSuccess={handleLoginSuccess} 
            onSwitchToRegister={() => setShowLogin(false)}
          />
        ) : (
          <Register 
            onSwitchToLogin={() => setShowLogin(true)}
          />
        )}
      </div>
    );
  }

  return (
    <div>
      <Header username={username} onLogout={handleLogout} />
      
      <div style={{ maxWidth: "800px", margin: "20px auto", padding: "20px" }}>
        <Typography variant="h4" gutterBottom align="center">
          Dashboard
        </Typography>
        
        <Card variant="outlined" style={{ marginBottom: "20px" }}>
          <CardContent>
            <TextField
              fullWidth
              label="Enter social media or e-commerce URL"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              variant="outlined"
              style={{ marginBottom: "16px" }}
              placeholder="https://twitter.com/... or https://youtube.com/..."
            />
            <Button 
              onClick={handleAnalyze} 
              disabled={loading || !url.trim()} 
              variant="contained" 
              color="primary" 
              fullWidth
            >
              {loading ? <CircularProgress size={24} /> : "Analyze"}
            </Button>
            
            {error && (
              <Alert severity="error" style={{ marginTop: "16px" }}>
                {error}
              </Alert>
            )}
          </CardContent>
        </Card>

        {loading && (
          <Card variant="outlined" style={{ marginBottom: "20px" }}>
            <CardContent style={{ textAlign: "center" }}>
              <CircularProgress size={40} />
              <Typography variant="body1" style={{ marginTop: "16px" }}>
                Analyzing comments... This may take a moment.
              </Typography>
            </CardContent>
          </Card>
        )}

        {data && (
          <div style={{ display: "flex", gap: "20px", justifyContent: "center", flexWrap: "wrap" }}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6">Sentiment Distribution</Typography>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Total Comments: {data.total_comments || 0}
                </Typography>
                <PieChart width={300} height={300}>
                  <Pie
                    dataKey="value"
                    data={[
                      { name: "Positive", value: data.positive_percent || 0 },
                      { name: "Negative", value: data.negative_percent || 0 },
                    ]}
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label
                  >
                    {COLORS.map((color, index) => (
                      <Cell key={`cell-${index}`} fill={color} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </CardContent>
            </Card>

            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6">Purchase Intent</Typography>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Platform: {data.platform || 'Unknown'}
                </Typography>
                <BarChart width={300} height={300} data={[{ name: "Intent", value: data.purchase_intent_percent || 0 }]}>
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" fill="#82ca9d" />
                </BarChart>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}
