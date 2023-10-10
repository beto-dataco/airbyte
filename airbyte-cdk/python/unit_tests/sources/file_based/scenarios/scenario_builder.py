#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, List, Mapping, Optional, Tuple, Type

from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.file_based.availability_strategy.abstract_file_based_availability_strategy import (
    AbstractFileBasedAvailabilityStrategy,
)
from airbyte_cdk.sources.file_based.discovery_policy import AbstractDiscoveryPolicy, DefaultDiscoveryPolicy
from airbyte_cdk.sources.file_based.file_based_source import default_parsers
from airbyte_cdk.sources.file_based.file_based_stream_reader import AbstractFileBasedStreamReader
from airbyte_cdk.sources.file_based.file_types.file_type_parser import FileTypeParser
from airbyte_cdk.sources.file_based.schema_validation_policies import AbstractSchemaValidationPolicy
from airbyte_cdk.sources.file_based.stream.cursor import AbstractFileBasedCursor
from unit_tests.sources.file_based.in_memory_files_source import InMemoryFilesSource


@dataclass
class IncrementalScenarioConfig:
    input_state: List[Mapping[str, Any]] = field(default_factory=list)
    expected_output_state: Optional[Mapping[str, Any]] = None


class TestScenario:
    def __init__(
        self,
        name: str,
        config: Mapping[str, Any],
        source: AbstractSource,
        expected_spec: Optional[Mapping[str, Any]],
        expected_check_status: Optional[str],
        expected_catalog: Optional[Mapping[str, Any]],
        expected_logs: Optional[Mapping[str, List[Mapping[str, Any]]]],
        expected_records: List[Mapping[str, Any]],
        expected_check_error: Tuple[Optional[Type[Exception]], Optional[str]],
        expected_discover_error: Tuple[Optional[Type[Exception]], Optional[str]],
        expected_read_error: Tuple[Optional[Type[Exception]], Optional[str]],
        incremental_scenario_config: Optional[IncrementalScenarioConfig],
    ):
        self.name = name
        self.config = config
        self.source = source
        self.expected_spec = expected_spec
        self.expected_check_status = expected_check_status
        self.expected_catalog = expected_catalog
        self.expected_logs = expected_logs
        self.expected_records = expected_records
        self.expected_check_error = expected_check_error
        self.expected_discover_error = expected_discover_error
        self.expected_read_error = expected_read_error
        self.incremental_scenario_config = incremental_scenario_config
        self.validate()

    def validate(self) -> None:
        assert self.name
        if not self.expected_catalog:
            return
        if self.expected_read_error or self.expected_check_error:
            return
        # Only verify the streams if no errors are expected
        streams = set([s.name for s in self.source.streams(self.config)])
        expected_streams = {s["name"] for s in self.expected_catalog["streams"]}
        assert expected_streams <= streams

    def configured_catalog(self, sync_mode: SyncMode) -> Optional[Mapping[str, Any]]:
        if not self.expected_catalog:
            return None
        catalog: Mapping[str, Any] = {"streams": []}
        for stream in self.expected_catalog["streams"]:
            catalog["streams"].append(
                {
                    "stream": stream,
                    "sync_mode": sync_mode.value,
                    "destination_sync_mode": "append",
                }
            )

        return catalog

    def input_state(self) -> List[Mapping[str, Any]]:
        if self.incremental_scenario_config:
            return self.incremental_scenario_config.input_state
        else:
            return []


class FileBasedSourceBuilder:
    def __init__(self) -> None:
        self._files: Mapping[str, Any] = {}
        self._file_type: Optional[str] = None
        self._availability_strategy: Optional[AbstractFileBasedAvailabilityStrategy] = None
        self._discovery_policy: AbstractDiscoveryPolicy = DefaultDiscoveryPolicy()
        self._validation_policies: Optional[Mapping[str, AbstractSchemaValidationPolicy]] = None
        self._parsers = default_parsers
        self._stream_reader: Optional[AbstractFileBasedStreamReader] = None
        self._file_write_options: Mapping[str, Any] = {}
        self._cursor_cls: Optional[Type[AbstractFileBasedCursor]] = None

    def build(self, configured_catalog) -> AbstractSource:
        if self._file_type is None:
            raise ValueError("file_type is not set")
        return InMemoryFilesSource(
            self._files,
            self._file_type,
            self._availability_strategy,
            self._discovery_policy,
            self._validation_policies,
            self._parsers,
            self._stream_reader,
            configured_catalog,
            self._file_write_options,
            self._cursor_cls,
        )

    def set_files(self, files: Mapping[str, Any]) -> "FileBasedSourceBuilder":
        self._files = files
        return self

    def set_file_type(self, file_type: str) -> "FileBasedSourceBuilder":
        self._file_type = file_type
        return self

    def set_parsers(self, parsers: Mapping[Type[Any], FileTypeParser]) -> "FileBasedSourceBuilder":
        self._parsers = parsers
        return self

    def set_availability_strategy(self, availability_strategy: AbstractFileBasedAvailabilityStrategy) -> "FileBasedSourceBuilder":
        self._availability_strategy = availability_strategy
        return self

    def set_discovery_policy(self, discovery_policy: AbstractDiscoveryPolicy) -> "FileBasedSourceBuilder":
        self._discovery_policy = discovery_policy
        return self

    def set_validation_policies(self, validation_policies: Mapping[str, AbstractSchemaValidationPolicy]) -> "FileBasedSourceBuilder":
        self._validation_policies = validation_policies
        return self

    def set_stream_reader(self, stream_reader: AbstractFileBasedStreamReader) -> "FileBasedSourceBuilder":
        self._stream_reader = stream_reader
        return self

    def set_cursor_cls(self, cursor_cls: AbstractFileBasedCursor) -> "FileBasedSourceBuilder":
        self._cursor_cls = cursor_cls
        return self

    def set_file_write_options(self, file_write_options: Mapping[str, Any]) -> "FileBasedSourceBuilder":
        self._file_write_options = file_write_options
        return self

    def copy(self) -> "FileBasedSourceBuilder":
        return deepcopy(self)


class TestScenarioBuilder:
    def __init__(self) -> None:
        self._name = ""
        self._config: Mapping[str, Any] = {}
        self._expected_spec: Optional[Mapping[str, Any]] = None
        self._expected_check_status: Optional[str] = None
        self._expected_catalog: Mapping[str, Any] = {}
        self._expected_logs: Optional[Mapping[str, Any]] = None
        self._expected_records: List[Mapping[str, Any]] = []
        self._expected_check_error: Tuple[Optional[Type[Exception]], Optional[str]] = None, None
        self._expected_discover_error: Tuple[Optional[Type[Exception]], Optional[str]] = None, None
        self._expected_read_error: Tuple[Optional[Type[Exception]], Optional[str]] = None, None
        self._incremental_scenario_config: Optional[IncrementalScenarioConfig] = None
        self.source_builder = None

    def set_name(self, name: str) -> "TestScenarioBuilder":
        self._name = name
        return self

    def set_config(self, config: Mapping[str, Any]) -> "TestScenarioBuilder":
        self._config = config
        return self

    def set_expected_spec(self, expected_spec: Mapping[str, Any]) -> "TestScenarioBuilder":
        self._expected_spec = expected_spec
        return self

    def set_expected_check_status(self, expected_check_status: str) -> "TestScenarioBuilder":
        self._expected_check_status = expected_check_status
        return self

    def set_expected_catalog(self, expected_catalog: Mapping[str, Any]) -> "TestScenarioBuilder":
        self._expected_catalog = expected_catalog
        return self

    def set_expected_logs(self, expected_logs: Mapping[str, List[Mapping[str, Any]]]) -> "TestScenarioBuilder":
        self._expected_logs = expected_logs
        return self

    def set_expected_records(self, expected_records: List[Mapping[str, Any]]) -> "TestScenarioBuilder":
        self._expected_records = expected_records
        return self

    def set_incremental_scenario_config(self, incremental_scenario_config: IncrementalScenarioConfig) -> "TestScenarioBuilder":
        self._incremental_scenario_config = incremental_scenario_config
        return self

    def set_expected_check_error(self, error: Optional[Type[Exception]], message: str) -> "TestScenarioBuilder":
        self._expected_check_error = error, message
        return self

    def set_expected_discover_error(self, error: Type[Exception], message: str) -> "TestScenarioBuilder":
        self._expected_discover_error = error, message
        return self

    def set_expected_read_error(self, error: Type[Exception], message: str) -> "TestScenarioBuilder":
        self._expected_read_error = error, message
        return self

    def set_source_builder(self, source_builder):
        self.source_builder = source_builder
        return self

    def copy(self) -> "TestScenarioBuilder":
        return deepcopy(self)

    def build(self) -> TestScenario:
        if self.source_builder is None:
            raise ValueError("source_builder is not set")
        source = self.source_builder.build(
            self._configured_catalog(SyncMode.incremental if self._incremental_scenario_config else SyncMode.full_refresh)
        )
        return TestScenario(
            self._name,
            self._config,
            source,
            self._expected_spec,
            self._expected_check_status,
            self._expected_catalog,
            self._expected_logs,
            self._expected_records,
            self._expected_check_error,
            self._expected_discover_error,
            self._expected_read_error,
            self._incremental_scenario_config,
        )

    def _configured_catalog(self, sync_mode: SyncMode) -> Optional[Mapping[str, Any]]:
        if not self._expected_catalog:
            return None
        catalog: Mapping[str, Any] = {"streams": []}
        for stream in self._expected_catalog["streams"]:
            catalog["streams"].append(
                {
                    "stream": stream,
                    "sync_mode": sync_mode.value,
                    "destination_sync_mode": "append",
                }
            )

        return catalog
