// src/pages/HomePage.jsx
import React, { useEffect, useState } from "react";
import ProductTable from "../components/ProductTable";
import { fetchProducts, deleteProduct, getBrands } from "../services/productService";

const HomePage = () => {
    const [products, setProducts] = useState([]);
    const [selectedBrands, setSelectedBrands] = useState([]);
    const [minPrice, setMinPrice] = useState("");
    const [maxPrice, setMaxPrice] = useState("");
    const [minRating, setMinRating] = useState("");
    const [maxRating, setMaxRating] = useState("");
    const [availableBrands, setAvailableBrands] = useState([]);

    const [total, setTotal] = useState(0);
    const [page, setPage] = useState(1);
    const pageSize = 10;

    const loadData = async () => {
        try {
            const data = await fetchProducts(
                page,
                pageSize,
                selectedBrands,
                minPrice,
                maxPrice,
                minRating,
                maxRating
            );
            setProducts(data.items);
            setTotal(data.total);
        } catch (err) {
            console.error("Failed to fetch data:", err);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure you want to delete this product?")) return;
        try {
            await deleteProduct(id);
            loadData();
        } catch (err) {
            console.error("Failed to delete product:", err);
        }
    };

    useEffect(() => {
        const loadBrands = async () => {
            try {
                const brands = await getBrands();
                setAvailableBrands(brands);
            } catch (err) {
                console.error("Failed to load brands:", err);
            }
        };
        loadBrands();
    }, []);


    useEffect(() => {
        loadData();
    }, [page, selectedBrands, minPrice, maxPrice, minRating, maxRating]);

    const totalPages = Math.ceil(total / pageSize);

    return (
        <>
            <h1>Scraped Products</h1>

            <div className="filter-container">
  <div className="filter-row">
    <strong>Brands:</strong>
    <div className="brand-buttons">
      {availableBrands.map((b) => {
        const isActive = selectedBrands.includes(b);
        return (
          <button
            key={b}
            onClick={() => {
              if (isActive) {
                setSelectedBrands(selectedBrands.filter((brand) => brand !== b));
              } else {
                setSelectedBrands([...selectedBrands, b]);
              }
              setPage(1);
            }}
            className={`brand-button ${isActive ? "active" : ""}`}
          >
            {b}
          </button>
        );
      })}
      <button className="brand-button" onClick={() => setSelectedBrands([])}>
        Clear
      </button>
    </div>
  </div>

  <div className="filter-row">
    <div className="filter-group">
      <strong>Price:</strong>
      <div>
        <input
          type="number"
          placeholder="Min"
          value={minPrice}
          onChange={(e) => {
            setMinPrice(e.target.value);
            setPage(1);
          }}
        />
        <span> - </span>
        <input
          type="number"
          placeholder="Max"
          value={maxPrice}
          onChange={(e) => {
            setMaxPrice(e.target.value);
            setPage(1);
          }}
        />
      </div>
    </div>

    <div className="filter-group">
      <strong>Rating:</strong>
      <div>
        <input
          type="number"
          step="0.1"
          placeholder="Min"
          value={minRating}
          onChange={(e) => {
            setMinRating(e.target.value);
            setPage(1);
          }}
        />
        <span> - </span>
        <input
          type="number"
          step="0.1"
          placeholder="Max"
          value={maxRating}
          onChange={(e) => {
            setMaxRating(e.target.value);
            setPage(1);
          }}
        />
      </div>
    </div>
  </div>
</div>



            <ProductTable products={products} onDelete={handleDelete} />

            <div className="pagination">
                <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>
                    Prev
                </button>
                <span>
                    Page {page} of {totalPages}
                </span>
                <button onClick={() => setPage(p => p + 1)} disabled={page >= totalPages}>
                    Next
                </button>
            </div>
        </>
    );
};

export default HomePage;
