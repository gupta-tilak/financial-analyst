import React, { useState } from "react";
import { Container, Typography, Box, CircularProgress, Snackbar, Alert } from "@mui/material";
import PromptForm from "./components/PromptForm";
import ResultsTabs from "./components/ResultsTabs";
import axios from "axios";

function App() {
  const [loading, setLoading] = useState(false);
  const [llmResponse, setLlmResponse] = useState("");
  const [contextChunks, setContextChunks] = useState([]);
  const [allNews, setAllNews] = useState([]);
  const [error, setError] = useState("");

  const handleAnalyze = async (ticker, prompt) => {
    setLoading(true);
    setError("");
    setLlmResponse("");
    setContextChunks([]);
    setAllNews([]);
    try {
      const res = await axios.post("http://localhost:8000/analyze", { ticker, prompt });
      setLlmResponse(res.data.llm_response);
      setContextChunks(res.data.context_chunks);
      setAllNews(res.data.all_news);
    } catch (err) {
      setError("Failed to fetch analysis. Please try again.");
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h3" align="center" gutterBottom>
        💹 Investment Analyzer
      </Typography>
      <Typography align="center" color="text.secondary" sx={{ mb: 4 }}>
        Enter your prompt and select a stock ticker to get the latest news and an AI-powered analysis.
      </Typography>
      <PromptForm onAnalyze={handleAnalyze} loading={loading} />
      <Box sx={{ mt: 4 }}>
        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
            <CircularProgress />
          </Box>
        ) : (
          (llmResponse || allNews.length > 0) && (
            <ResultsTabs
              llmResponse={llmResponse}
              contextChunks={contextChunks}
              allNews={allNews}
            />
          )
        )}
      </Box>
      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError("")}>
        <Alert severity="error" onClose={() => setError("")}>{error}</Alert>
      </Snackbar>
    </Container>
  );
}

export default App;