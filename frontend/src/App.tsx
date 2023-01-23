import { useState } from "react";
import "./App.css";

function getId(url: string) {
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);

  return match && match[2].length === 11 ? match[2] : null;
}

function App() {
  const [searchText, setSearchText] = useState("");
  const [response, setResponse] = useState<string>();
  const [isLoading, setIsLoading] = useState(false);

  const getYTPreviews = (body: string) => {
    const youtubeLinks = body.match(/(https?:\/\/www\.youtube\.com\/watch\?v=\S+)/g);
    const youtubeIds = youtubeLinks?.map((link) => getId(link));
    const timeStamps = youtubeLinks?.map((link) => {
      let tValue = link.match(/t=(\S+)/);
      return tValue ? tValue[1] : null;
    });
    const youtubePreviews = youtubeIds?.map((id, index) => {
      const ts = timeStamps ? timeStamps[index] : null;
      if (ts) {
        const iframeMarkup =
        '<iframe width="560" height="315" src="//www.youtube.com/embed/' +
        id + "&t=" + ts +
        '" frameborder="0" allowfullscreen></iframe>';
      }
      const iframeMarkup =
        '<iframe width="560" height="315" src="//www.youtube.com/embed/' +
        id + 
        '" frameborder="0" allowfullscreen></iframe>';
      return iframeMarkup;
    });
    return youtubePreviews;
  };
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
        <div>
          <h4>{response}</h4>
          <div>
            {getYTPreviews(response)?.map((preview) => (
              <div dangerouslySetInnerHTML={{ __html: preview }} />
            ))}
          </div>
        </div>
      ) : (
        <form className="fancy-search-bar" onSubmit={handleSearch}>
          <input
            type="text"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            className="fancy-search-bar__input"
            placeholder="Ask me anything..."
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
