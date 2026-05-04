from django_dramatiq.management.commands.rundramatiq import Command as RunDramatiqCommand  # type: ignore


class Command(RunDramatiqCommand):
    def discover_tasks_modules(self) -> list[str]:
        tasks_modules = super().discover_tasks_modules()
        if tasks_modules:
            tasks_modules[0] = "backend.dramatiq_setup"
        else:
            tasks_modules = ["backend.dramatiq_setup"]
        return tasks_modules  # type: ignore

