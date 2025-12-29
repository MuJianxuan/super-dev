"""
Super Dev - Shared Utilities
Provides unified logging, styling, and common helpers.
"""

from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from rich.progress import Progress, SpinnerColumn, TextColumn
import sys
import contextlib

# Custom theme for "Hacker/Professional" look
theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "h1": "bold magenta underline",
    "highlight": "bold white on blue",
})

console = Console(theme=theme)

def print_header(title: str, subtitle: str = ""):
    """Print a stylized header."""
    console.print()
    console.print(Panel(
        f"[bold white]{subtitle}[/bold white]",
        title=f"[h1]Super Dev :: {title}[/h1]",
        border_style="blue",
        padding=(1, 2)
    ))
    console.print()

def print_step(step_name: str):
    """Print a major step execution."""
    console.print(f"[bold cyan]➜ Executing:[/bold cyan] {step_name}...")

def print_success(message: str):
    """Print a success message."""
    console.print(f"[success]✔ {message}[/success]")

def print_error(message: str):
    """Print an error message."""
    console.print(f"[error]✖ {message}[/error]")

@contextlib.contextmanager
def spinner(description: str):
    """Context manager for a loading spinner."""
    with Progress(
        SpinnerColumn("dots", style="magenta"),
        TextColumn("[bold white]{task.description}[/bold white]"),
        transient=True,
    ) as progress:
        progress.add_task(description, total=None)
        yield
