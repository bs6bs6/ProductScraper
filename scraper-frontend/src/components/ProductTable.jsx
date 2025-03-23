import React from "react";

const ProductTable = ({ products, onDelete }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Image</th>
          <th>Title</th>
          <th>Brand</th>
          <th>Price</th>
          <th>Rating</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {products.length === 0 && (
          <tr><td colSpan="6">No products found.</td></tr>
        )}
        {products.map(product => (
          <tr key={product.id}>
            <td>
              {product.img && (
                <img
                  src={product.img}
                  alt={product.title}
                  style={{ width: "60px", height: "60px", objectFit: "cover" }}
                />
              )}
            </td>
            <td>
              <a href={product.url} target="_blank" rel="noopener noreferrer">
                {product.title}
              </a>
            </td>
            <td>{product.brand || "-"}</td>
            <td>${product.price}</td>
            <td>{product.rating ?? "-"}</td>
            <td>
              <button onClick={() => onDelete(product.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ProductTable;
