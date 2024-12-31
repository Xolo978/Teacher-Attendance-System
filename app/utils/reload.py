import sys
from pathlib import Path
from kivy.lang import Builder
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from typing import List

class HotReloader(FileSystemEventHandler):
    """
    A class to handle hot reloading of Python and KV files in a Kivy application.
    Attributes:
        app: The Kivy application instance.
    Methods:
        on_modified(event: FileSystemEvent) -> None:
            Handles the event when a file is modified. Reloads the file if it is a Python or KV file.
        _reload_py_file(path: str) -> None:
            Reloads a modified Python file and rebuilds the application.
        _reload_kv_file(path: str) -> None:
            Reloads a modified KV file and rebuilds the application.
    """
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app
        self._kv_file_mtimes = {}

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.src_path.endswith('.py'):
            print(f"Python file changed: {event.src_path}")
            self._reload_py_file(event.src_path)
        elif event.src_path.endswith('.kv'):
            print(f"KV file changed: {event.src_path}")
            self._reload_kv_file(event.src_path)

    def _reload_py_file(self, path: str) -> None:
        module_path = Path(path).resolve().relative_to(Path.cwd())
        module_name = str(module_path).replace('/', '.').replace('\\', '.')[:-3]
        
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        try:
            import importlib
            importlib.import_module(module_name)
            self.app.rebuild()
        except Exception as e:
            print(f"Error reloading {path}: {e}")

    def _reload_kv_file(self, path: str) -> None:
        try:
            current_mtime = Path(path).stat().st_mtime
            if self._kv_file_mtimes.get(path) == current_mtime:
                return
            self._kv_file_mtimes[path] = current_mtime
            
            Builder.unload_file(path)
            Builder.load_file(path)
            self.app.rebuild()
        except Exception as e:
            print(f"Error reloading {path}: {e}")

def start_hot_reload(app, directories: List[str]):
    event_handler = HotReloader(app)
    observer = Observer()
    
    for directory in directories:
        observer.schedule(event_handler, directory, recursive=True)
    
    observer.start()
    return observer