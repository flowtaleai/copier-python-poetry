{% if generate_docs == "pdoc" %}
"""
.. include:: ../../README.md
   :end-before: Versioning
{% if generate_example_code %}

.. include:: ../../docs/user_guide.md
{% endif %}
"""

{% endif %}
__version__ = "{{ version }}"
