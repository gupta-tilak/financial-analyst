import React from "react";
import { Box, Typography, Paper } from "@mui/material";

function LLMResult({ llmResponse, contextChunks }) {
  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Financial Analysis & Recommendation
      </Typography>
      <Paper elevation={2} sx={{ p: 2, mb: 2, background: "#f6f6fa" }}>
        <Typography>{llmResponse}</Typography>
      </Paper>
      <Typography variant="subtitle1" gutterBottom>
        News Context Used:
      </Typography>
      {contextChunks && contextChunks.length > 0 ? (
        contextChunks.map((chunk, i) => (
          <Paper key={i} sx={{ p: 1, mb: 1, background: "#f9f9f9" }}>
            <Typography variant="body2">{chunk}</Typography>
          </Paper>
        ))
      ) : (
        <Typography color="text.secondary">No context chunks available.</Typography>
      )}
    </Box>
  );
}

export default LLMResult;