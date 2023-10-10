# {{ project_name }}

{{ project_short_description }}

## Install

### Dependencies

- python
- poetry [pip]
- make (optional)
- pytest (optional, installed by poetry but it's more convenient to have it installed on the system) [pip]
- pre-commit (optional, installed by poetry but it's more convenient to have it installed on the system) [pip]

### Development Environment Configuration

- Configure the project (poetry, pre-commit):
  ```bash
  make setup
  ```
- Open VSCode and install the suggested extensions

## Contributing

This project is tagged with versions according to [SemVer](https://semver.org/). To bump the project version:

```bash
make bump
```
