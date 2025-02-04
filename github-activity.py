import sys

import requests
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

from model import CreateEventPayload, Event, PushEventPayload, WatchEventPayload

console = Console()


def display(event_data: dict):
    event_type = event_data["type"]
    created_at = event_data["created_at"]

    content = Text()

    header = Text()
    header.append("📅 Date: ", style="bold cyan")
    header.append(created_at, style="italic dim")

    if event_type == "PushEvent":
        event = Event[PushEventPayload].model_validate(event_data)
        content = Text.from_markup(
            f"🙋 User [bold magenta]{event.actor.login}[/] "
            f"pushed [bold green]{len(event.payload.commits)} commits[/]\n"
            f"📦 To repository: [bold yellow]{event.repo.name}[/]"
        )

    elif event_type == "WatchEvent":
        event = Event[WatchEventPayload].model_validate(event_data)
        content = Text.from_markup(
            f"👀 User [bold magenta]{event.actor.login}[/] "
            f"started watching\n"
            f"🏷️ Repository: [bold yellow]{event.repo.name}[/]"
        )

    elif event_type == "CreateEvent":
        event = Event[CreateEventPayload].model_validate(event_data)
        content = Text.from_markup(
            f"🛠️ User [bold magenta]{event.actor.login}[/] "
            f"created repository\n"
            f"🎉 [bold yellow]{event.repo.name}[/]"
        )

    else:
        content = Text.from_markup(
            f"😅 [bold yellow]Unsupported event type![/]\nType: [italic]{event_type}[/]"
        )

    panel = Panel(
        content,
        title=header,
        style=Style(
            color="blue"
            if event_type == "PushEvent"
            else "green"
            if event_type == "WatchEvent"
            else "magenta"
            if event_type == "CreateEvent"
            else "yellow"
        ),
        subtitle="⚡ GitHub Event",
        subtitle_align="right",
    )

    console.print(panel)


def fetch_user_activity(username: str):
    url = f"https://api.github.com/users/{username}/events"
    res = requests.get(url=url)
    if res.status_code == 200:
        events: list[dict] = res.json()
        for event in events:
            display(event_data=event)
        rprint("Done!")
    else:
        rprint(f"Error fetching for {username}: {res.status_code}")


def main():
    if len(sys.argv) > 1:
        fetch_user_activity(sys.argv[1])


if __name__ == "__main__":
    main()
