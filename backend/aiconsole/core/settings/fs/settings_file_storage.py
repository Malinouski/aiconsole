import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from aiconsole.consts import AICONSOLE_USER_CONFIG_DIR
from aiconsole.core.settings.fs.file_observer import FileObserver
from aiconsole.core.settings.fs.settings_file_format import (
    load_settings_file,
    save_settings_file,
)
from aiconsole.core.settings.settings_storage import SettingsStorage
from aiconsole.core.settings.utils.update_settings_data import update_settings_data
from aiconsole.utils.events import InternalEvent, internal_events
from aiconsole_toolkit.settings.partial_settings_data import PartialSettingsData
from aiconsole_toolkit.settings.settings_data import SettingsData

_log = logging.getLogger(__name__)


def _get_settings_from_path(file_path: Path | None) -> PartialSettingsData:
    if file_path:
        data = load_settings_file(file_path)
    else:
        data = PartialSettingsData()
    return data


@dataclass(frozen=True, slots=True)
class SettingsUpdatedEvent(InternalEvent):
    pass


class SettingsFileStorage(SettingsStorage):
    def __init__(
        self,
        project_path: Path | None,
    ):
        self.observer = FileObserver()
        self.change_project(project_path)

    @property
    def global_settings_file_path(self):
        return AICONSOLE_USER_CONFIG_DIR() / "settings.toml"

    @property
    def project_settings_file_path(self):
        return self._project_settings_file_path

    @property
    def global_settings(self):
        return _get_settings_from_path(self.global_settings_file_path)

    @property
    def project_settings(self):
        return _get_settings_from_path(self.project_settings_file_path)

    def change_project(self, project_path: Optional[Path] = None):
        self._project_settings_file_path = project_path / "settings.toml" if project_path else None
        self._start_observer()

    def save(self, settings_data: PartialSettingsData, to_global: bool):
        file_path = self.global_settings_file_path if to_global else self.project_settings_file_path
        if not file_path:
            raise ValueError("Cannot save settings, path not specified")

        detault_settings = SettingsData()
        data = update_settings_data(detault_settings, load_settings_file(file_path), settings_data)
        save_settings_file(file_path, data)

    async def _reload(self):
        await internal_events().emit(SettingsUpdatedEvent())

    def _start_observer(self):
        from aiconsole.core.settings.settings import settings

        file_paths = [self.global_settings_file_path]
        if self.project_settings_file_path:
            file_paths.append(self.project_settings_file_path)

        if self.observer:
            self.observer.start(file_paths=file_paths, on_changed=self._reload)