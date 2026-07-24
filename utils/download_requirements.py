import adsk.core

import sys

def download_requirements():
    try:    
        import pip
    except:
        import ensurepip
        ensurepip.bootstrap()
        import pip
    pip.main(["install", "scipy"])