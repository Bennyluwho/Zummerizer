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
            const response = await fetch("https://zummerizer.onrender.com/summarize", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url }),
            });

            if (!response.ok) throw new Error("Failed to connect to backend.");

            const data = await response.json();

            if (data.summary) {
                setSummary(data.summary);
                toast.success("Summary generated successfully!");
            } else if (data.error) {
                setSummary("❌ Error: " + data.error);
                toast.error("Backend Error: " + data.error);
            }

        } catch (error) {
            console.error(error);
            toast.error("Failed to generate summary.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app">
        <h1>📰 Zummerizer</h1>
        <div className="input-container">
            <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Enter Article URL"
            />
            <button onClick={handleSummarize}>Summarize</button>
        </div>

        {loading && (
            <div className="loading-container">
                <div className="spinner"></div>
                <p>Loading...</p>
            </div>
        )}

        {summary && (
            <div className="summary-container">
                <div className="summary">
                    <h2>📑 Summary:</h2>
                    <p dangerouslySetInnerHTML={{ __html: summary.replace(/\n/g, "<br>") }} />
                </div>
            </div>
        )}
            <ToastContainer position="top-center" />
        </div>
    );
}

export default App;
