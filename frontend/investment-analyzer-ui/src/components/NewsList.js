import React from "react";
import { Card, CardContent, Typography, CardActions, Button, Grid, Chip, Avatar, Box } from "@mui/material";

function NewsList({ news }) {
  if (!news || news.length === 0) {
    return <Typography>No news found for this ticker.</Typography>;
  }
  return (
    <Grid container spacing={2}>
      {news.map((article, idx) => (
        <Grid item xs={12} md={6} key={article.article_id || idx}>
          <Card variant="outlined" sx={{ height: "100%", display: "flex", flexDirection: "column" }}>
            <CardContent sx={{ flexGrow: 1 }}>
              <Typography variant="h6" gutterBottom>
                {article.title}
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {article.description}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {article.published_utc && new Date(article.published_utc).toLocaleString()}
              </Typography>
              <Box sx={{ mt: 1 }}>
                {article.keywords && article.keywords.map((kw, i) => (
                  <Chip key={i} label={kw} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                ))}
              </Box>
            </CardContent>
            <CardActions>
              <Button size="small" href={article.article_url} target="_blank" rel="noopener">
                Read More
              </Button>
              {article.source && (
                <Chip
                  avatar={<Avatar>{article.source[0]}</Avatar>}
                  label={article.source}
                  size="small"
                  sx={{ ml: 1 }}
                />
              )}
            </CardActions>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}

export default NewsList;