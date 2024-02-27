import pytest
from prompt_toolkit.validation import ValidationError


@pytest.mark.parametrize(
    "distribution_name",
    ["validpackagename", "valid_package_name", "valid-package-name"],
)
def test_validate_distribtuion_name_valid(tmp_path, copier, distribution_name):
    custom_answers = {"distribution_name": distribution_name}
    project = copier.copy(tmp_path, **custom_answers)
    project.run("pytest")


@pytest.mark.parametrize(
    "distribution_name",
    ["", "-test", "test-", "distribution name"],
)
def test_validate_distribtuion_name_invalid(tmp_path, copier, distribution_name):
    custom_answers = {"distribution_name": distribution_name}
    with pytest.raises(ValidationError):
        copier.copy(tmp_path, **custom_answers)


@pytest.mark.parametrize("package_name", ["validpackagename", "valid_package_name"])
def test_validate_package_name_valid(tmp_path, copier, package_name):
    custom_answers = {"package_name": package_name, "distribution_name": "test-name"}
    project = copier.copy(tmp_path, **custom_answers)
    project.run("pytest")


@pytest.mark.parametrize(
    "package_name",
    [
        "invalid-package-name",
        "2invalidpackagename",
        "invalidPackageName",
        "_invalidpackagename",
        "",
    ],
)
def test_validate_package_name_invalid(tmp_path, copier, package_name):
    custom_answers = {"package_name": package_name, "distribution_name": "test-name"}
    with pytest.raises(ValidationError):
        copier.copy(tmp_path, **custom_answers)


@pytest.mark.parametrize("email", ["", "test@test.com"])
def test_validate_email_valid(tmp_path, copier, email):
    custom_answers = {"author_email": email, "distribution_name": "test-name"}
    project = copier.copy(tmp_path, **custom_answers)
    project.run("pytest")


def test_validate_email_invalid(tmp_path, copier):
    custom_answers = {"author_email": "userexample.com"}
    with pytest.raises(ValidationError):
        copier.copy(tmp_path, **custom_answers)


@pytest.mark.parametrize("version", ["0.1.0", "1.2.3", "10.20.30"])
def test_validate_version_valid(tmp_path, copier, version):
    custom_answers = {"version": version, "distribution_name": "test-name"}
    project = copier.copy(tmp_path, **custom_answers)
    project.run("pytest")


@pytest.mark.parametrize("version", ["invalid_version", "1.2.3.4.5.6.a"])
def test_validate_version_invalid(tmp_path, copier, version):
    custom_answers = {"version": version, "distribution_name": "test-name"}
    with pytest.raises(ValidationError):
        copier.copy(tmp_path, **custom_answers)
