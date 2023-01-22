import { useState } from "react";
import "./App.css";

function App() {
  const [searchText, setSearchText] = useState("");

  const handleSearch = async (e: any) => {
    e.preventDefault();
    console.log(`Searching for ${searchText}`);
    const res = await fetch("/hello");
    const data = await res.json();
    console.log(data);
  };
  return (
    <div className="App">
      <h1>Ask FSDL</h1>

      <form className="fancy-search-bar" onSubmit={handleSearch}>
        <input
          type="text"
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          className="fancy-search-bar__input"
          placeholder="What do you want to know?..."
        />
        <button className="fancy-search-bar__button">Search</button>
      </form>


    </div>
  );
}

export default App;
