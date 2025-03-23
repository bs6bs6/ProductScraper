import React, { useState } from "react";
import { triggerScrape } from "../services/productService";

const ScraperPage = () => {
  const [pages, setPages] = useState(3);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleScrape = async () => {
    setLoading(true);
    setMessage("");
    try {
      const res = await triggerScrape(pages);
      setMessage(`Scraped successfully: ${res.message || "Data saved."}`);
    } catch (err) {
      console.error("Scraping failed", err);
      setMessage("Scraping failed. Check the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Start Scraper</h1>
      <label>
        Pages to scrape:
        <input
          type="number"
          min={1}
          max={20}
          value={pages}
          onChange={(e) => setPages(Number(e.target.value))}
          style={{ marginLeft: "10px", width: "60px" }}
        />
      </label>
      <br /><br />
      <div style={{ textAlign: "center", marginTop: "20px" }}>
        <button onClick={handleScrape} disabled={loading}>
            {loading ? "Scraping..." : "Start Scraper"}
        </button>
      </div>

      <br /><br />
      {message && <p>{message}</p>}
    </div>
  );
};

export default ScraperPage;
