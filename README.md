# bd-stubs

Type stubs for [Ballsdex](https://github.com/Ballsdex-Team/BallsDex).

`bd-stubs` provides type information for Ballsdex, making it easier to develop packages with type checkers such as Pyright.

## Installation

> [!TIP]
> Installing `bd-stubs` with the `all` extra is recommended. This also installs the dependencies required for complete type information, including types from packages such as `discord.py`.

Using [uv](https://docs.astral.sh/uv/):

```bash
uv add "bd-stubs[all] @ git+https://github.com/Caylies/bd-stubs@0.1.2"
```

## Typing Status

| Module                           | Status  |
| -------------------------------- | :-----: |
| `ballsdex`                       | ⏳     |
| `ballsdex/core`                  | ⏳     |
| `ballsdex/core/image_generator`  | ❌     |
| `ballsdex/core/utils`            | ⏳✅   |
| `ballsdex/packages`              | ⏳     |
| `ballsdex/packages/admin`        | ❌     |
| `ballsdex/packages/balls`        | ❌     |
| `ballsdex/packages/countryballs` | ✅     |
| `ballsdex/packages/guildconfig`  | ❌     |
| `ballsdex/packages/info`         | ❌     |
| `ballsdex/packages/money`        | ❌     |
| `ballsdex/packages/players`      | ❌     |
| `ballsdex/packages/trade`        | ❌     |
| `bd_models`                      | ✅     |
| `settings`                       | ✅     |
| `users`                          | ⏳✅   |

### Status Legend

* ✅ Fully typed
* ⏳ Partially typed / in progress
* ❌ Not typed
* ⏳✅ Partially typed with completed portions
