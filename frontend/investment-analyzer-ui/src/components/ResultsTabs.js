import React, { useState } from "react";
import { Tabs, Tab, Box } from "@mui/material";
import NewsList from "./NewsList";
import LLMResult from "./LLMResult";

function ResultsTabs({ llmResponse, contextChunks, allNews }) {
  const [tab, setTab] = useState(0);

  return (
    <Box>
      <Tabs value={tab} onChange={(_, v) => setTab(v)} centered>
        <Tab label="📰 News" />
        <Tab label="🤖 LLM Analysis" />
      </Tabs>
      <Box sx={{ mt: 2 }}>
        {tab === 0 && <NewsList news={allNews} />}
        {tab === 1 && <LLMResult llmResponse={llmResponse} contextChunks={contextChunks} />}
      </Box>
    </Box>
  );
}

export default ResultsTabs;