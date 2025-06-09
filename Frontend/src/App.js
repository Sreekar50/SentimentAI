import React, { useState } from "react";
import axios from "axios";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from "recharts";
import { TextField, Button, Card, CardContent, Typography, CircularProgress } from "@mui/material";

const COLORS = ["#0088FE", "#FF8042"];

export default function Dashboard() {
  const [url, setUrl] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/fetch_comments/", { url });
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data", error);
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", padding: "20px" }}>
      <Typography variant="h4" gutterBottom>
        Social Media Sentiment Analysis
      </Typography>
      <Card variant="outlined">
        <CardContent>
          <TextField
            fullWidth
            label="Enter social media or e-commerce URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            variant="outlined"
          />
          <Button onClick={handleAnalyze} disabled={loading} variant="contained" color="primary" fullWidth style={{ marginTop: "10px" }}>
            {loading ? <CircularProgress size={24} /> : "Analyze"}
          </Button>
        </CardContent>
      </Card>

      {data && (
        <div style={{ marginTop: "20px", display: "flex", gap: "20px", justifyContent: "center", flexWrap: "wrap" }}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6">Sentiment Distribution</Typography>
              <PieChart width={300} height={300}>
                <Pie
                  dataKey="value"
                  data={[
                    { name: "Positive", value: data.positive_percent },
                    { name: "Negative", value: data.negative_percent },
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
              <BarChart width={300} height={300} data={[{ name: "Intent", value: data.purchase_intent_percent }]}>
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
  );
}
