import React, { useEffect, useState } from "react";

function App() {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/restaurants")
      .then((response) => response.json())
      .then((data) => {
        setRestaurants(data.restaurants);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching restaurants:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: "1rem", fontFamily: "sans-serif" }}>
      <h2>Mariyam's Restaurants</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {restaurants.map((review, index) => (
            <li key={index}>{review}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
