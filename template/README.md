# {{ project_name if project_name else distribution_name }}

{{ project_short_description }}

{% if generate_docs != 'none' %}
The project documentation is available at [docs/](docs/).
{% endif %}

## Installation

> Write installation instructions here or remove this section.

## Usage

{% if package_type == 'cli' %}
```
{{ package_name.split('.')[-1] }} --help
```
{% endif %}

{% if license != "LicenseRef-Proprietary" %}
## License

This project is licensed under the terms of the [{{ license }}](LICENSE).
{% endif %}
