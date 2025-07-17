# LLM-Code

A simple CLI tool that lets you chat with multiple LLM providers (Claude, GPT, Gemini) while analyzing your codebase. Think of it as a Claude Code spoof with multi-provider support!

## ✨ Features

- **Multi-Provider Support**: Switch between Anthropic Claude, OpenAI GPT, and Google Gemini
- **Smart File Context**: Use `@filename` to include files in your conversations
- **Intelligent Autocomplete**: File suggestions with `@` that work across subdirectories
- **Rich CLI Interface**: Beautiful terminal UI with syntax highlighting and markdown support
- **Conversation History**: Maintains context across your chat session
- **Flexible File Handling**: Supports 30+ file types including code, config, and documentation files

## 🚀 Quick Start

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Tusharbecoding/LLM-Code
   cd LLM-Code
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API keys** in a `.env` file:

   ```env
   ANTHROPIC_API_KEY=your_claude_api_key
   OPENAI_API_KEY=your_openai_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

4. **Run the CLI:**
   ```bash
   python run.py
   # or
   python -m llm_code
   ```

## 📖 Usage

### Basic Commands

| Command            | Description                                          |
| ------------------ | ---------------------------------------------------- |
| `@filename`        | Include a file in your message context               |
| `/provider [name]` | Switch between providers (anthropic, openai, gemini) |
| `/clear`           | Clear conversation history                           |
| `/files`           | Show all available files in current directory        |
| `/help`            | Show help information                                |
| `/exit`            | Exit the application                                 |

### Examples

```bash
# Ask about a specific file
@main.py explain this code

# Include multiple files
@src/app.js @package.json how can I optimize this?

# Switch providers
/provider openai

# Get help
/help
```

### File Autocomplete

- Type `@` to see available files
- Use arrow keys to navigate
- Press Enter to select a file (won't submit the message)
- Press Enter again to submit your message

## 🔧 Configuration

### Environment Variables

Create a `.env` file in your project root:

```env
# Required API Keys
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key

# Optional: Custom Models
ANTHROPIC_MODEL=claude-3-5-sonnet-20240620
OPENAI_MODEL=gpt-4o-mini
GEMINI_MODEL=gemini-1.5-flash
```

### Supported File Types

The tool automatically recognizes and includes:

- **Code Files**: `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.go`, `.rs`, `.swift`, etc.
- **Config Files**: `.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.env`
- **Documentation**: `.md`, `.txt`
- **Web Files**: `.html`, `.css`, `.scss`
- **And many more...**

## 🏗️ Project Structure

```
LLM-Code/
├── llm_code/
│   ├── __main__.py          # CLI entry point
│   ├── cli.py              # Main CLI logic
│   ├── config.py           # Configuration management
│   ├── providers/          # LLM provider implementations
│   │   ├── base.py
│   │   ├── anthropic_provider.py
│   │   ├── openai_provider.py
│   │   └── gemini_provider.py
│   └── utils/
│       └── file_handler.py # File processing utilities
├── run.py                  # Alternative entry point
├── requirements.txt        # Dependencies
└── README.md
```

## 🎯 Use Cases

- **Code Review**: Ask LLMs to review your code files
- **Debugging**: Get help debugging issues across multiple files
- **Refactoring**: Get suggestions for code improvements
- **Documentation**: Generate documentation for your codebase
- **Learning**: Understand unfamiliar codebases with AI assistance

## 🔄 Running in Different Directories

You can run the CLI from any directory to analyze that project:

```bash
cd /path/to/your/project
python /path/to/LLM-Code/run.py
```

The tool will automatically detect and suggest files from the current directory.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request
