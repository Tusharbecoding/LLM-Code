import click
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from typing import Optional, List, Dict
import os
from pathlib import Path
from prompt_toolkit.key_binding import KeyBindings


from .config import Config
from .providers import get_provider
from .utils import FileHandler

console = Console()

class FileCompleter(Completer):
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self._file_list = self.file_handler.list_supported_files()

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        if '@' not in text_before_cursor:
            return
        last_at = text_before_cursor.rfind('@')
        if last_at == -1:
            return
        partial = text_before_cursor[last_at + 1:].strip().lower()
        for file_path in self._file_list:
            if partial in file_path.lower():
                yield Completion(file_path, start_position=-len(partial), display=file_path)

class LLMChat: 
    def __init__(self):
        self.config = Config()
        self.file_handler = FileHandler()
        self.current_provider = self.config.default_provider
        self.provider = None
        self.conversation_history: List[Dict[str, str]] = []

        self._init_provider(self.current_provider)

    def _init_provider(self, provider_name: str) -> bool:
        if not self.config.validate_provider(provider_name):
            console.print(f"[red]Error: {provider_name} is not configured properly. Check your API key.[/red]")
            return False
        
        provider_config = self.config.get_provider_config(provider_name)
        try:
            self.provider = get_provider(provider_name, provider_config.api_key, provider_config.model)
            self.current_provider = provider_name
            return True
        except Exception as e:
            console.print(f"[red]Error initializing {provider_name}: {str(e)}[/red]")
            return False

    def switch_provider(self, provider_name: str):
        if self._init_provider(provider_name):
            console.print(f"[green]Switched to {provider_name}[/green]")
            self.conversation_history = []

    def process_message(self, user_input: str) -> str:
        if not self.provider:
            console.print(f"[red]Error: No provider initialized. Please check your API keys.[/red]")
            return "Error: No provider available. Please configure your API keys."
            
        files, cleaned_message = self.file_handler.parse_file_references(user_input)
        context_parts = []

        if files:
            console.print(f"[blue]Loading files: {', '.join(files)}[/blue]")
            file_contents = self.file_handler.get_files_content(files)
            for content, filename in file_contents:
                if not content.startswith("Error:"):
                    context_parts.append(self.provider.format_context_message(content, filename))
                else:
                    console.print(f"[yellow]{content}[/yellow]")
                
        if context_parts:
            full_message = "Here are the files for context:\n\n" + "\n\n".join(context_parts) + f"\n\n{cleaned_message}"
        else:
            full_message = cleaned_message

        self.conversation_history.append({"role": "user", "content": full_message})

        console.print(f"[dim]Using {self.current_provider}...[/dim]")
        response = self.provider.generate(self.conversation_history)

        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    

    def show_help(self):
        """Show help information"""
        help_text = """
# LLM CLI Help

## Commands:
- **@filename** - Include a specific file in the context
- **/provider [name]** - Switch provider (anthropic, openai, gemini)
- **/clear** - Clear conversation history
- **/files** - Show all available files in current directory
- **/help** - Show this help message
- **/exit** or **Ctrl+C** - Exit the application

## Examples:
- `@main.py explain this code`
- `/provider openai`
- `@src/app.js @package.json how can I optimize this?`
        """
        console.print(Markdown(help_text))

    def list_files(self):
        """List available files in the current directory"""
        from pathlib import Path
        files = []
        
        for item in Path(".").rglob("*"):
            if item.is_file() and not any(part.startswith('.') for part in item.parts[:-1]):
                relative = item.relative_to(".")
                if item.suffix in self.file_handler.SUPPORTED_EXTENSIONS:
                    files.append(str(relative))
        
        if files:
            console.print("[blue]Available files:[/blue]")
            for f in sorted(files)[:50]:  # Limit to 50 files
                console.print(f"  - {f}")
            if len(files) > 50:
                console.print(f"  ... and {len(files) - 50} more files")
        else:
            console.print("[yellow]No supported files found in current directory[/yellow]")

@click.command()
@click.option('--provider', '-p', type=click.Choice(['anthropic', 'openai', 'gemini']), 
              help='LLM provider to use')


def main(provider: Optional[str] = None):
    """Multi-provider LLM CLI tool"""
    console.print(Panel.fit(
        "[bold blue]LLM CODE[/bold blue]\n"
        "Chat with multiple LLM providers\n"
        "Type /help for commands",
        border_style="blue"
    ))
    
    chat = LLMChat()
    
    # Switch provider if specified
    if provider:
        chat.switch_provider(provider)
    
    console.print(f"[green]Using {chat.current_provider} provider[/green]")
    console.print("[dim]Type your message or /help for commands[/dim]\n")
    
    # Create custom file completer
    file_completer = FileCompleter(chat.file_handler)

    # Custom key bindings for prompt_toolkit
    kb = KeyBindings()

    @kb.add('enter')
    def _(event):
        buff = event.app.current_buffer
        if buff.complete_state:
            # Accept the current completion, do NOT submit
            completion = buff.complete_state.current_completion
            if completion:
                buff.apply_completion(completion)
            return
        else:
            buff.validate_and_handle()

    while True:
        try:
            user_input = prompt(
                "You: ",
                completer=file_completer,
                key_bindings=kb,
                complete_in_thread=True,
                complete_while_typing=True
            )
            
            if not user_input.strip():
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                command_parts = user_input.split()
                command = command_parts[0].lower()
                
                if command == "/exit":
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                elif command == "/help":
                    chat.show_help()
                elif command == "/clear":
                    chat.conversation_history = []
                    console.print("[green]Conversation history cleared[/green]")
                elif command == "/files":
                    chat.list_files()
                elif command == "/provider":
                    if len(command_parts) > 1:
                        chat.switch_provider(command_parts[1])
                    else:
                        console.print(f"[blue]Current provider: {chat.current_provider}[/blue]")
                        console.print("Available providers: anthropic, openai, gemini")
                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                continue
            
            # Process message
            response = chat.process_message(user_input)
            
            # Display response
            console.print("\n[bold]Assistant:[/bold]")
            console.print(Markdown(response))
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    main()