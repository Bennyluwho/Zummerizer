from summarizer import extract_article_text, summarize_text

def main():
    url = input("Enter the article URL: ")
    try:
        print("\nExtracting article...")
        article_text = extract_article_text(url)
        print("\nSummarizing article...")
        summary = summarize_text(article_text)
        print("\n📄 Summary:\n")
        print(summary)
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
