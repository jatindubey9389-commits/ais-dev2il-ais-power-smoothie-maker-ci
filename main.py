from pathlib import Path
import time
import pyjokes
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

def get_ingredients(recipe_file: Path) -> list[str]:
    if not recipe_file.exists():
        return []
    with open(recipe_file, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def make_smoothie(recipe_file: Path, console: Console = Console()):
    ingredients = get_ingredients(recipe_file)
    if not ingredients:
        console.print(f"[bold red]No ingredients found in {recipe_file.name}![/bold red]")
        return ingredients

    console.print(f"[bold green]Starting to make: {recipe_file.stem.replace('_', ' ').title()}[/bold green]")
    joke = pyjokes.get_joke()
    console.print(f"[bold cyan]Let met enlighten you with a joke while you wait: {joke}[/bold cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:

        # Adding ingredients
        for ingredient in ingredients:
            task = progress.add_task(f"Adding {ingredient}...", total=None)
            time.sleep(0.5)  # Simulate time to add ingredient
            progress.remove_task(task)
            console.print(f"  [green]✓[/green] Added {ingredient}")

        # Blending
        blend_task = progress.add_task("[bold magenta]Blending everything together...[/bold magenta]", total=None)
        time.sleep(2)
        progress.remove_task(blend_task)

    console.print(f"[bold yellow]✨ Smoothie '{recipe_file.stem.replace('_', ' ').title()}' is ready! Enjoy! ✨[/bold yellow]")


def main():
    base_dir = Path(__file__).parent
    smoothies_dir = base_dir / "smoothies"

    # Just grab the first txt file we find
    recipe_files = list(smoothies_dir.glob("*.txt"))

    if not recipe_files:
        print("No smoothie recipes found in 'smoothies/' folder!")
        return

    # Let's make the smoothie
    make_smoothie(recipe_files[0])

if __name__ == "__main__":
    main()
