import React, { useState, useEffect } from "react";

function Restaurants() {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/restaurants")
      .then((response) => response.json())
      .then((data) => {
        setRestaurants(data); // because it's an array, not an object
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching restaurants:", error);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h1>Restaurants</h1>
      <ul>
        {restaurants.map((restaurant) => (
          <li key={restaurant.id}>
            {restaurant.name} — {restaurant.address}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Restaurants;
