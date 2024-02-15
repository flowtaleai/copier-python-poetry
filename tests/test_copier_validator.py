import re


# Function to validate project_name
def validate_project_name(project_name):
    return len(project_name.strip()) > 0


# Function to validate package_name
def validate_package_name(package_name):
    return bool(re.match(r"^[a-z][a-z0-9-]*$", package_name))


# Function to validate email
def validate_email(email):
    if len(email) == 0 or "@" in email:
        return True
    else:
        return False


# Function to validate version
def validate_version(version):
    if re.match(r"^\d+(\.\d+)*$", version):
        return True
    else:
        return False


# Tests for validate_project_name
def test_validate_project_name():
    assert validate_project_name("Python Boilerplate")
    assert not validate_project_name(" ")
    assert not validate_project_name("")


# Tests for validate_package_name
def test_validate_package_name():
    assert validate_package_name("validpackagename")
    assert validate_package_name("valid-package-name")
    assert not validate_package_name("2invalidpackagename")
    assert not validate_package_name("invalidPackageName")
    assert not validate_package_name("invalid_package_name")
    assert not validate_package_name("-invalidpackagename")
    assert not validate_package_name("")


# Tests for validate_email
def test_validate_email():
    assert validate_email("")
    assert validate_email("user@example.com")
    assert not validate_email("userexample.com")


# Tests for validate_version
def test_validate_version():
    assert validate_version("0.1.0")
    assert validate_version("1.2.3")
    assert validate_version("10.20.30")
    assert not validate_version("invalid_version")
    assert not validate_version("1.2.3.4.5.6.a")
