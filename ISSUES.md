# ISSUES / Task Checklist

This document tracks maintainability, quality, and performance tasks for this **macOS-only** Mechanical-Keyboard-Sim project (based on the current `soundy.py`). Use this as a working checklist.

> Scope note: This project is intentionally **macOS-only** and relies on the system audio player (`afplay`). Tasks below aim to make that explicit, robust, and easier to maintain.

---

## Correctness (bugs / logic)

- [ ] **Fix logically incorrect `cmd` conditional** in `soundy.py`:
  - Current pattern (bug):
    - `elif key_pressed == "cmd" or "cmd_l" or "cmd_r":`
  - Required fix:
    - `elif key_pressed in ("cmd", "cmd_l", "cmd_r"):`
  - Add a small comment explaining why the old expression is always truthy.

- [ ] Normalize key-name handling consistently (e.g., lowercase everything once) and document expected key strings (`pynput` vs other libraries).

- [ ] Ensure modifier keys (cmd/ctrl/alt/shift) do not accidentally trigger sound playback unless explicitly intended.

---

## Platform + dependency validation (macOS-only hardening)

- [ ] Add an explicit platform guard at startup:
  - Check `sys.platform == "darwin"`.
  - If not macOS, print a clear message and exit with non-zero status.

- [ ] Check `afplay` existence before starting the listener:
  - Use `shutil.which("afplay")`.
  - If missing, show actionable guidance (e.g., “afplay should exist on macOS; check PATH / system integrity”).

- [ ] Validate sound file configuration at startup:
  - Confirm the sound directory exists.
  - Confirm all required sound files exist (and are readable).
  - Fail fast with a helpful error listing missing files.
  - Optional: validate file extensions / accepted formats (e.g., `.wav`, `.aiff`, `.mp3`) as used.

- [ ] Add a single “startup summary” log line listing:
  - platform, resolved sound directory, number of sound files found, whether `afplay` was located.

---

## Code structure / maintainability

- [ ] Keep the **main guard** (`if __name__ == "__main__":`) in place (already fixed) and ensure all side effects (listener start, initialization) happen only under it.

- [ ] Refactor `soundy.py` into small, testable units:
  - e.g., `resolve_sound_dir()`, `validate_environment()`, `load_sound_map()`, `play_sound_for_key()`, `on_press()`.

- [ ] Replace global state with a small config object/dataclass where appropriate (sound paths, cooldowns, toggles).

- [ ] Remove/replace misleading comment(s) about threads:
  - If the code uses `subprocess` with `afplay`, clarify what is and isn’t threaded.
  - If there is no explicit threading, don’t imply there is.

- [ ] Add type hints to public functions (and to key handler signatures) and run a type checker optionally (`mypy`).

---

## Observability (logging / diagnostics)

- [ ] Replace `print()` statements with the `logging` module:
  - Provide log levels (INFO for startup, DEBUG for key events if enabled, WARNING/ERROR for failures).
  - Add a `--verbose` mode (or env var) to enable debug logs.

- [ ] Log errors from failed `afplay` invocations (non-zero return code) with enough context (key name, chosen file).

---

## Performance / responsiveness

- [ ] Avoid spawning excessive `afplay` processes for key repeats (especially when key is held):
  - Implement debouncing/cooldown per key (optional but recommended).
  - Consider a small global rate limit (e.g., max N sounds/sec) to prevent audio overwhelm.

- [ ] Optional: pool/serialize playback to prevent overlapping process storms.
  - Keep it simple—this is a sim, not a DAW—but ensure it remains responsive.

- [ ] Ensure the key listener callback stays fast:
  - Offload slow work (path resolution, heavy logging, validation) outside the callback.

---

## Reliability / UX

- [ ] Provide clear CLI help / usage:
  - `--sounds DIR`, `--volume` (if supported via `afplay` flags), `--list-sounds`, `--dry-run`.

- [ ] Graceful shutdown and cleanup:
  - Ensure listener stops cleanly on Ctrl+C.
  - If tracking subprocesses, optionally terminate outstanding `afplay` processes on exit.

---

## Testing / QA

- [ ] Add lightweight unit tests for non-I/O logic:
  - platform guard logic
  - sound directory resolution
  - sound file existence checks
  - key normalization and mapping logic

- [ ] Add a simple manual test checklist in docs:
  - launch, press common keys, hold key behavior, modifier key behavior, missing sound dir behavior.

---

## Documentation

- [ ] Update `README.md` to explicitly state:
  - macOS-only requirement (`sys.platform == "darwin"`)
  - dependency on `afplay`
  - how to add/replace sound files
  - troubleshooting (no sound, missing afplay, permissions, accessibility permissions if needed for key listening)

- [ ] Document the sound file naming/mapping rules (how keys map to filenames).

---

## Nice-to-haves (optional)

- [ ] Provide a configuration file option (TOML/YAML/JSON) for key->sound mappings.

- [ ] Add a “randomize sounds” mode or multiple samples per key to reduce repetition.

- [ ] Add CI linting (ruff/flake8), formatting (black), and basic tests on macOS runners.
