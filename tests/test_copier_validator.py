import pytest
from prompt_toolkit.validation import ValidationError


# Tests for validate_project_name
def test_validate_project_name(tmp_path, copier):
    test_project_names = ["Test project", " ", ""]
    test_valid_respons = [True, False, False]
    for (name, valid) in zip(test_project_names, test_valid_respons, strict=True):
        custom_answers = {"project_name": name}
        if valid:
            project = copier.copy(tmp_path, **custom_answers)
            project.run("pytest")
        else:
            with pytest.raises(ValidationError):
                copier.copy(tmp_path, **custom_answers)


def test_validate_package_name(tmp_path, copier):
    test_package_names = [
        "validpackagename",
        "valid_package_name",
        "invalid-package-name",
        "2invalidpackagename",
        "invalidPackageName",
        "_invalidpackagename",
        "",
    ]
    test_valid_responses = [True, True, False, False, False, False, False]
    for (name, valid) in zip(test_package_names, test_valid_responses, strict=True):
        custom_answers = {"project_name": "test", "package_name": name}
        print(name, valid)
        if valid:
            project = copier.copy(tmp_path, **custom_answers)
            project.run("pytest")
        else:
            with pytest.raises(ValidationError):
                copier.copy(tmp_path, **custom_answers)


# Tests for validate_email
def test_validate_email(tmp_path, copier):
    test_emails = ["userexample.com"]
    test_valid_responses = [False]
    for (email, valid) in zip(test_emails, test_valid_responses, strict=True):
        custom_answers = {"author_email": email}
        print(email, valid)
        if valid:
            project = copier.copy(tmp_path, **custom_answers)
            project.run("pytest")
        else:
            with pytest.raises(ValidationError):
                copier.copy(tmp_path, **custom_answers)


# Tests for validate_version
def test_validate_version(tmp_path, copier):
    test_versions = ["0.1.0", "1.2.3", "10.20.30", "invalid_version", "1.2.3.4.5.6.a"]
    test_valid_responses = [True, True, True, False, False]
    for (version, valid) in zip(test_versions, test_valid_responses, strict=True):
        custom_answers = {"version": version}
        print(version, valid)
        if valid:
            project = copier.copy(tmp_path, **custom_answers)
            project.run("pytest")
        else:
            with pytest.raises(ValidationError):
                copier.copy(tmp_path, **custom_answers)
