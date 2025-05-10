import { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
    const [url, setUrl] = useState("");
    const [summary, setSummary] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSummarize = async () => {
        if (!url) {
            toast.warn("Please enter a URL!");
            return;
        }

        setLoading(true);
        setSummary("");

        try {
            const response = await fetch("https://YOUR-BACKEND-URL/summarize", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url }),
            });

            if (!response.ok) throw new Error("Network response was not ok.");

            const data = await response.json();
            setSummary(data.summary);
            toast.success("Summary generated successfully!");
        } catch (error) {
            console.error(error);
            setSummary("❌ Error generating summary.");
            toast.error("Failed to generate summary.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app">
            <h1>📰 Article Digest Bot</h1>
            <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Enter Article URL"
            />
            <button onClick={handleSummarize}>Summarize</button>

            {loading && <div className="spinner"></div>}

            {summary && (
                <div className="summary">
                    <h2>📑 Summary:</h2>
                    <p dangerouslySetInnerHTML={{ __html: summary.replace(/\n/g, "<br>") }} />
                </div>
            )}

            <ToastContainer position="top-center" />
        </div>
    );
}

export default App;
