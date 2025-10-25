# Find Books MCP Server

A Model Context Protocol (MCP) server that provides book search capabilities using the Google Books API. This server includes intelligent caching to improve performance and reduce API calls.

## Features

- **Book Search Tool**: Search for books by title using the Google Books API
- **Smart Caching**: Automatically caches up to 100 books locally for faster repeated queries
- **Resource Endpoint**: Access the latest searched book via MCP resources
- **Prompt Template**: Generate summaries of cached book themes

## How It Works

The server provides a `get_book` tool that:
1. Checks if the book exists in the local cache (`books_cache.txt`)
2. If found, returns cached information immediately
3. If not found, queries the Google Books API
4. Caches the result for future queries
5. Automatically manages cache size (maintains max 100 books)

Each book entry includes:
- Title
- Author(s)
- Published Date
- Maturity Rating

## Prerequisites

- Python 3.13 or higher
- Google Books API key
- `uv` package manager (recommended) or `pip`

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /path/to/mcp-server
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```
   Or with pip:
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```
   API_KEY=your_google_books_api_key_here
   ```

   To get a Google Books API key:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Books API
   - Create credentials (API Key)

## Testing with Claude Desktop

### 1. Install the MCP Server

Run the following command from the project directory:

```bash
uv run mcp install server.py
```

This will register the server with Claude Desktop.

### 2. Configure Claude Desktop

Alternatively, you can manually add the server to Claude's configuration file:

**On macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**On Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration:

```json
{
  "mcpServers": {
    "find-books": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/your-path/to-project/mcp-server",
        "run",
        "server.py"
      ],
      "env": {
        "API_KEY": "your_google_books_api_key_here"
      }
    }
  }
}
```

### 3. Restart Claude Desktop

Close and reopen Claude Desktop for the changes to take effect.

### 4. Test the Server

Open Claude Desktop and try these example queries:

**Search for a book**:
```
Can you search for the book "The Great Gatsby"?
```

**Search multiple books**:
```
Find information about "1984" and "Brave New World"
```

**Check the latest book**:
```
What's the latest book in the cache?
```

**Generate a theme summary**:
```
Can you summarize the themes of books in the cache?
```

## Available MCP Components

### Tools

- **`get_book(book: str)`**: Search for a book by title
  - Parameters: `book` - The title of the book to search for
  - Returns: Formatted string with book information

### Resources

- **`books://latest`**: Access the most recently searched book

### Prompts

- **`note_summary_prompt()`**: Generate a summary of major themes from cached books

## Project Structure

```
mcp-server/
├── main.py              # Main MCP server implementation
├── pyproject.toml       # Project dependencies and metadata
├── .env                 # Environment variables (not in git)
├── books_cache.txt      # Local cache for book data
├── README.md            # This file
└── .venv/               # Virtual environment
```

## Development

### Running the Server Standalone

For testing purposes, you can run the main.py file directly:

```bash
uv run main.py
```

This will execute a test query for "Introduction to Machine Learning with Python".

### Cache Management

- Cache file: `books_cache.txt`
- Maximum cached books: 100
- When limit is reached, oldest entries are automatically removed
- Cache uses a sliding window algorithm for efficient book matching

## Troubleshooting

**Server not appearing in Claude Desktop**:
- Ensure Claude Desktop is fully closed and restarted
- Check the configuration file path and JSON syntax
- Verify the server path in the configuration is correct

**API errors**:
- Verify your API key is valid and the Books API is enabled
- Check your `.env` file is in the correct location
- Ensure you haven't exceeded Google Books API rate limits

**Cache issues**:
- Delete `books_cache.txt` to clear the cache
- The file will be recreated automatically on the next search

## License

This project is for educational purposes.

## Contributing

Feel free to submit issues and enhancement requests!
