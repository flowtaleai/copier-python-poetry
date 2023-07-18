{%- if cookiecutter.testing_framework == "unittest" -%}
import unittest

{% endif -%}
from {{cookiecutter.project_slug}}.{{cookiecutter.project_slug}} import a_function


{% if cookiecutter.testing_framework == "pytest" -%}
def test_a_function():
    """Sample test."""
    assert a_function() == "Hello World!"
{%- elif cookiecutter.testing_framework == "unittest" -%}
class TestAFunction(unittest.TestCase):
    def setUp(self):
        pass

    def test_a_function(self):
        result = a_function()

        self.assertEqual("Hello World!", result)

    def tearDown(self):
        pass
{%- endif %}
