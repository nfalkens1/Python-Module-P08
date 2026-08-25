import importlib.util
import importlib.metadata
import sys


DEPENDENCIES: dict[str, tuple[str, str]] = {
    "pandas": ("pandas", "Data manipulation ready"),
    "numpy": ("numpy", "Numerical computation ready"),
    "matplotlib": ("matplotlib", "Visualization ready"),
}


def check_dependencies() -> list[str]:
    """
    Prints the install status of every required package.
    """
    list_out: list[str] = []
    for import_name, (dist_name, ok_status) in DEPENDENCIES.items():
        if importlib.util.find_spec(import_name) is None:
            print(f"[MISSING] {import_name}")
            list_out.append(import_name)
        else:
            version = importlib.metadata.version(dist_name)
            print(f"[OK] {import_name} ({version}) - {ok_status}")
    return list_out


def analyze_data() -> dict[str, int]:
    """
    Uses different imported modules:
     - numpy: for creating the data (1000 random int between 1-1000)
     - pandas: to manipulate the data and sort it inside categories
     - matplotlib: to create the .png visualization
    """
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    raw_data = np.random.default_rng(111).integers(0, 1000, size=1000)
    data_frame = pd.DataFrame({"numbers": raw_data})
    labels = ["0-199", "200-399", "400-599", "600-799", "800-999"]
    data_frame["Range"] = pd.cut(data_frame["numbers"],
                                 bins=[0, 200, 400, 600, 800, 1000],
                                 labels=labels, right=False)
    final_data = data_frame.groupby("Range")["numbers"].count()
    format_out = {str(k): int(v) for k, v in final_data.to_dict().items()}
    fig, ax = plt.subplots()
    ax.bar(list(format_out.keys()), list(format_out.values()))
    ax.set_title("Visualized Data")
    ax.set_xlabel("Value range")
    ax.set_ylabel("Count")
    fig.savefig("matrix_analysis.png")
    plt.close(fig)
    return format_out


def show_dif() -> None:
    """
    Shows the difference between Pip and Poetry by:
     - comparing sys paths
     - showing dependencies of each required package
     - showing declared vs total installs
    """
    header = "\nDifferences between Pip and Poetry:\n"
    cur_path = sys.prefix
    cur_python = sys.executable
    print(header)
    print(f"Current path: {cur_path}")
    print(f"Current python: {cur_python}")
    print()
    for name in DEPENDENCIES.keys():
        print(f"{name} installed version: {importlib.metadata.version(name)}")
        requirements = importlib.metadata.requires(name) or []
        print(f"{name} required dependencies:")
        for requirement in requirements:
            if " extra == " not in requirement:
                print(f"  {requirement}")
        if not requirements:
            print("  No required dependency")
        print()
    installs_declared = len(DEPENDENCIES.keys())
    total_installs = len(list(importlib.metadata.distributions()))
    print(f"Declared installs: {installs_declared}")
    print(" vs.")
    print(f"Total installs: {total_installs}")


if __name__ == "__main__":
    header = "\nLOADING STATUS: Loading programs...\n"
    print(header)
    pip_instructions = "\n".join([
        " install with pip:",
        " $> pip install -r requirements.txt",
        " $> python3 loading.py"
    ])
    poetry_instructions = "\n".join([
        " install with poetry",
        " $> poetry install",
        " $> poetry run python loading.py"
    ])
    missing_dependencies = check_dependencies()
    if not missing_dependencies:
        print()
        print("Analyzing Matrix data...")
        data = analyze_data()
        data_points = sum(data.values())
        print(f"Processing {data_points} data points...")
        print("Generating visualization...")
        print()
        print("Analysis complete!")
        print("Results saved to: matrix_analysis.png")
        show_dif()
    else:
        missing_count = len(missing_dependencies)
        print()
        print(f"Missing {missing_count} dependencies:")
        for package in missing_dependencies:
            print(package)
        print()
        print("How to install:")
        print(pip_instructions)
        print("or")
        print(poetry_instructions)
