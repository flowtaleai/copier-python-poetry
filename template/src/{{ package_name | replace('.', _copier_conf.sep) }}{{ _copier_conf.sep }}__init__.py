{% if generate_docs == "pdoc" %}
"""
.. include:: ../../README.md
"""

{% endif %}
__version__ = "{{ version }}"
