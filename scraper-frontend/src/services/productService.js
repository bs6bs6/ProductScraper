import axios from "axios";

const API_BASE = "http://localhost:8001/data";

const SCRAPER_PATH = "scrape";

const BRANDS_PATH = "brands";

export const fetchProducts = async (
    page,
    pageSize,
    brands,
    minPrice,
    maxPrice,
    minRating,
    maxRating
) => {
    let url = `${API_BASE}?page=${page}&page_size=${pageSize}`;

    const params = new URLSearchParams();

    params.append("page", page);
    params.append("page_size", pageSize);

    if (brands?.length > 0) {
        brands.forEach((brand) => {
            params.append("brands", brand);
        });
    }
    if (minPrice) params.append("min_price", minPrice);
    if (maxPrice) params.append("max_price", maxPrice);
    if (minRating) params.append("min_rating", minRating);
    if (maxRating) params.append("max_rating", maxRating);

    const fullUrl = `${url}&${params.toString()}`;
    const res = await axios.get(fullUrl);
    return res.data;
};


export const deleteProduct = async (id) => {
    await axios.delete(`${API_BASE}/${id}`);
};

export const triggerScrape = async (pages = 3) => {
    const res = await axios.post(`${API_BASE}/${SCRAPER_PATH}?max_pages=${pages}`);
    return res.data;
};

export const getBrands = async () => {
    const res = await axios.get(`${API_BASE}/${BRANDS_PATH}`);
    return res.data;
};
