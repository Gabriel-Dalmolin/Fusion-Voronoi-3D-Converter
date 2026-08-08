import os
import subprocess
import sys
import adsk.core


def download_requirements():
    app = adsk.core.Application.get()

    fusion_python = os.path.join(
        sys.path[0],
        "Python",
        "python.exe"
    )

    app.log(f"Fusion Python: {fusion_python}")

    # Check SciPy first.
    try:
        import scipy
        app.log("SciPy already installed.")
        return True
    except ImportError:
        app.log("SciPy not installed.")

    # Check whether pip exists.
    result = subprocess.run(
        [
            fusion_python,
            "-m",
            "pip",
            "--version"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        app.log("pip is not installed. Running ensurepip...")

        result = subprocess.run(
            [
                fusion_python,
                "-m",
                "ensurepip",
                "--upgrade"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        app.log(f"ensurepip exit code: {result.returncode}")
        app.log(f"ensurepip stdout: {result.stdout}")
        app.log(f"ensurepip stderr: {result.stderr}")

        if result.returncode != 0:
            app.log("Failed to install pip.")
            return False

    # Now install SciPy.
    result = subprocess.run(
        [
            fusion_python,
            "-m",
            "pip",
            "install",
            "scipy"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    app.log(f"pip install exit code: {result.returncode}")
    app.log(f"pip install stdout: {result.stdout}")
    app.log(f"pip install stderr: {result.stderr}")

    if result.returncode != 0:
        app.log("Failed to install SciPy.")
        return False

    app.log("SciPy installed successfully.")
    return True