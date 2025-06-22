import React, { useState } from "react";
import { Box, TextField, Button, MenuItem, InputAdornment } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

const FAMOUS_TICKERS = [
  "AAPL", "MSFT", "TSLA", "AMZN", "GOOG", "NVDA", "META", "NFLX", "JPM", "BRK.A"
];

function PromptForm({ onAnalyze, loading }) {
  const [ticker, setTicker] = useState(FAMOUS_TICKERS[0]);
  const [customTicker, setCustomTicker] = useState("");
  const [prompt, setPrompt] = useState("What are the latest developments and outlook for this company?");

  const handleSubmit = (e) => {
    e.preventDefault();
    const finalTicker = customTicker.trim() ? customTicker.trim().toUpperCase() : ticker;
    onAnalyze(finalTicker, prompt);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} display="flex" gap={2} flexWrap="wrap" alignItems="center" justifyContent="center">
      <TextField
        select
        label="Famous Ticker"
        value={ticker}
        onChange={e => setTicker(e.target.value)}
        sx={{ minWidth: 120 }}
        disabled={!!customTicker}
      >
        {FAMOUS_TICKERS.map(t => (
          <MenuItem key={t} value={t}>{t}</MenuItem>
        ))}
      </TextField>
      <TextField
        label="Or Custom Ticker"
        value={customTicker}
        onChange={e => setCustomTicker(e.target.value)}
        sx={{ minWidth: 140 }}
        placeholder="e.g. IBM"
      />
      <TextField
        label="Prompt"
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        sx={{ minWidth: 300, flex: 1 }}
      />
      <Button
        type="submit"
        variant="contained"
        color="primary"
        disabled={loading}
        startIcon={<SearchIcon />}
        sx={{ minWidth: 150, height: 56 }}
      >
        {loading ? "Analyzing..." : "Run Analysis"}
      </Button>
    </Box>
  );
}

export default PromptForm;