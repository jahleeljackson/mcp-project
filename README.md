# MCP Project

A complete Model Context Protocol (MCP) implementation featuring a custom book search server and a Streamlit-based chat client. This project demonstrates how to build and integrate MCP servers with both Claude Desktop and local LLMs using Ollama.

## 🎯 Overview

This project consists of two main components:

1. **MCP Server** (`mcp-server/`): A custom MCP server that provides book search capabilities using the Google Books API with intelligent caching
2. **MCP Client** (`mcp-client/`): A Streamlit web interface that connects to local LLMs via Ollama to interact with MCP servers

## 🌟 Features

### MCP Server
- 📚 Book search using Google Books API
- 💾 Smart caching system (up to 100 books)
- 🔌 MCP tools, resources, and prompts
- ⚡ Fast repeated queries with local cache

### MCP Client
- 💬 Interactive chat interface built with Streamlit
- 🤖 Integration with local LLMs via Ollama (Mistral by default)
- 🔗 Connects to MCP servers through Ollama MCP Bridge
- 🎨 Clean, user-friendly UI

## 📋 Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- [Ollama](https://ollama.ai/) installed and running
- Google Books API key
- Claude Desktop (optional, for testing with Claude)

## 🚀 Quick Start

### 1. Set Up the MCP Server

```bash
cd mcp-server

# Install dependencies
uv sync

# Create .env file with your Google Books API key
echo "API_KEY=your_google_books_api_key_here" > .env

# Test the server
uv run server.py
```

Get a Google Books API key:
- Visit [Google Cloud Console](https://console.cloud.google.com/)
- Create/select a project
- Enable the Books API
- Create an API Key credential

### 2. Set Up the MCP Client

```bash
cd mcp-client

# Install dependencies
uv sync

# Ensure Ollama is running
ollama pull mistral:latest  # or your preferred model

# Start the Ollama MCP Bridge
ollama-mcp-bridge

# In a new terminal, run the Streamlit app
streamlit run frontend.py
```

### 3. Configure MCP Servers

Edit `mcp-client/mcp-config.json` to configure which MCP servers to use:

```json
{
  "mcpServers": {
    "find-books": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-server",
        "run",
        "server.py"
      ]
    }
  }
}
```

## 📁 Project Structure

```
mcp_project/
├── mcp-server/              # MCP Server implementation
│   ├── server.py           # Main server code
│   ├── pyproject.toml      # Server dependencies
│   ├── .env               # API keys (not in git)
│   └── books_cache.txt    # Book cache storage
│
├── mcp-client/              # Streamlit chat client
│   ├── frontend.py         # Streamlit UI
│   ├── pyproject.toml      # Client dependencies
│   └── mcp-config.json     # MCP server configuration
│
├── .gitignore
└── README.md               # This file
```

## 💡 Usage Examples

Once both components are running, you can interact with the MCP server through the Streamlit interface:

**Search for books:**
```
Can you search for "The Great Gatsby"?
```

**Find multiple books:**
```
Tell me about "1984" and "Brave New World"
```

**Access latest book:**
```
What's the most recent book that was searched?
```

**Generate theme summaries:**
```
Can you summarize the themes from cached books?
```

## 🔧 Configuration

### Client Configuration (`mcp-client/pyproject.toml`)

```toml
[project]
model = "mistral:latest"  # Change to your preferred Ollama model
host = "0.0.0.0"
port = "8000"
```

### Server Configuration

Environment variables in `mcp-server/.env`:
```
API_KEY=your_google_books_api_key
```

## 🧪 Testing with Claude Desktop

The MCP server can also be used directly with Claude Desktop:

```bash
cd mcp-server
uv run mcp install server.py
```

Or manually configure in `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS).

## 🛠️ Development

### Running the Server Standalone
```bash
cd mcp-server
uv run server.py
```

### Running the Client Standalone
```bash
cd mcp-client
streamlit run frontend.py
```

### Cache Management
- Clear cache: Delete `mcp-server/books_cache.txt`
- Cache automatically maintains 100 most recent books
- Cache persists between server restarts

## 📚 MCP Components

### Tools
- `get_book(book: str)` - Search for books by title

### Resources
- `books://latest` - Access the most recently searched book

### Prompts
- `note_summary_prompt()` - Generate summaries of cached book themes

## 🐛 Troubleshooting

**Ollama MCP Bridge not connecting:**
- Ensure Ollama is running: `ollama list`
- Check if the bridge is running on port 8000
- Verify `mcp-config.json` paths are absolute

**Server not finding books:**
- Verify API key in `.env` file
- Check Google Books API quota/rate limits
- Test API key with a direct API call

**Streamlit app not loading:**
- Check if port 8501 is available
- Verify dependencies are installed: `uv sync`
- Check terminal for error messages

## 📖 Learn More

- [Model Context Protocol](https://modelcontextprotocol.io/) - Official MCP documentation
- [Ollama MCP Bridge](https://github.com/louloulin/ollama-mcp-bridge) - Bridge between Ollama and MCP
- [Google Books API](https://developers.google.com/books) - Books API documentation

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Note**: This is a mini project for learning MCP concepts and integration patterns.
