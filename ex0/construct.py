import sys
import os
import site


def is_venv() -> bool:
    """
    Checks if we are in a venv by comparing global and current path.
    Returns True/False
    """
    condition: bool = (sys.base_prefix != sys.prefix)
    return condition


def get_path_info() -> dict[str, str]:
    """
    Supplies path data as a dict to output message functions.
    """
    keys = ["Current Python",
            "Virtual environment",
            "Environment path",
            "Package installation path"]

    cur_python = sys.executable
    venv_name = os.path.basename(sys.prefix)
    env_path = sys.prefix
    package_install_path = site.getsitepackages()[0]

    values = [cur_python,
              venv_name,
              env_path,
              package_install_path]

    format_out = dict(zip(keys, values))
    return format_out


def env_message(path_data: dict[str, str]) -> str:
    """
    Creates output message for venv.
    """
    matrix_status = "MATRIX STATUS: Welcome to the construct"
    success_message = "SUCCESS: You're in an isolated environment!"
    cur_python = path_data["Current Python"]
    venv_name = path_data["Virtual environment"]
    env_path = path_data["Environment path"]
    inst_path = path_data["Package installation path"]

    raw_out = [
        "",
        matrix_status,
        "",
        f"Current Python: {cur_python}",
        f"Virtual Environment: {venv_name}",
        f"Environment Path: {env_path}",
        "",
        success_message,
        "Safe to install packages without affecting"
        "the global system."
        "",
        "Package installation path:",
        inst_path
    ]

    format_out = "\n".join(raw_out)
    return format_out


def global_message(path_data: dict[str, str]) -> str:
    """
    Creates warning message for global environment.
    """
    ...


if __name__ == "__main__":
    ...
