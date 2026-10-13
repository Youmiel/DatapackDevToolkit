# DatapackDevToolkit

> A build framework for Minecraft datapacks that ship the same JSON resources across many game versions from one source tree.

## Scope

The framework fits datapacks that ship the same JSON resources for several game versions and need the differences between versions to stay small and explicit.

- resources are defined once as compact Python patch scripts plus a minimal set of source files, so the generated JSON is never committed.
- it is not tied to a single resource type: worldgen configuration, loot tables, recipes and other datapack JSON are handled the same way.

## How it works

- there is one source directory per version, named after that version and listed in `build_settings.py`.
- inside a version directory every `.py` file is a patch, and every other file is a static resource that is copied into the build as-is.
- a patch declares `TYPE`, `reference_file` and `process_single` / `process_multi`. `reference_file` selects the JSON sources to read, `process_single` / `process_multi` return the modified content.
- sources may come from `common/`, from static files of the current version, or from the build output of an already-built older version.
- versions are built in the order they are declared in `build_settings.py`, so references only ever point backwards.

## Layout

- `build.py` — `run()` builds every configured version and packs it.
- `clean.py` — removes `__pycache__` folders.
- `json_diff.py` — minimal helper that reports differing paths between two JSON files.
- `builder/` — the framework modules used by the entry points.
- `template/build_settings.py` — configuration template; the copy a project uses lives in the project root.
- `template/json_patcher.py` — documents the patch interface.

## Patcher files

A patcher is a Python module placed anywhere in a version directory; its interface is documented in `template/json_patcher.py`.

- the file name is the target file name, with `.` written as `___`, for example `pack___mcmeta.py` generates `pack.mcmeta`.
- a reference may only read the build output of an older version (`MC_*` constants in `build_settings.py`), static files of the current version (`MC_0`) or `common/` (`COMMON`). Versions are built in the order they are declared in `build_settings.py`.

## Requirements

Python 3 and `chardet` (`pip install -r requirements.txt`).

## Contributing

Contributions are welcome. The build framework is a small Python program with a single third-party dependency (`chardet`), so any Python 3 runtime can run it.
