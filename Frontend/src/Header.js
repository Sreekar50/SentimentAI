import React, { useState } from "react";
import { AppBar, Toolbar, Typography, Button, CircularProgress } from "@mui/material";

const Header = ({ username, onLogout }) => {
  const [loading, setLoading] = useState(false);

  const handleLogout = async () => {
    setLoading(true);
    try {
      await onLogout();
    } catch (error) {
      console.error('Logout error:', error);
    }
    setLoading(false);
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" style={{ flexGrow: 1 }}>
          Social Media Sentiment Analysis
        </Typography>
        <Typography variant="body1" style={{ marginRight: "16px" }}>
          Welcome, {username}
        </Typography>
        <Button 
          color="inherit" 
          onClick={handleLogout}
          disabled={loading}
        >
          {loading ? <CircularProgress size={20} color="inherit" /> : 'Logout'}
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
