import { useState } from "react";
import "./App.css";

function App() {
  const [searchText, setSearchText] = useState("");
  const [response, setResponse] = useState<string>();
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e: any) => {
    setIsLoading(true);
    e.preventDefault();
    console.log(`Searching for ${searchText}`);
    const res = await fetch("/prompt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: searchText,
        config: {
          type: "WEB",
        },
      }),
    });
    const data = await res.json();

    setIsLoading(false);
    setResponse(data);
    console.log(data);
  };
  return (
    <div className="App">
      <h1>Ask FSDL</h1>

      {response ? (
        <h4>{response}</h4>
      ) : (
        <form className="fancy-search-bar" onSubmit={handleSearch}>
          <input
            type="text"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            className="fancy-search-bar__input"
            placeholder="What do you want to know?..."
            disabled={isLoading}
          />
          <button type="button" disabled={isLoading} style={{ backgroundColor: "#646cff" }}>
            Search
          </button>
        </form>
      )}

      {isLoading && <h3>Loading...</h3>}

      {response && (
        <button
          type="button"
          onClick={(e) => {
            e.preventDefault();
            setResponse(undefined);
            setIsLoading(false);
          }}
        >
          Ask another question
        </button>
      )}
    </div>
  );
}

export default App;
