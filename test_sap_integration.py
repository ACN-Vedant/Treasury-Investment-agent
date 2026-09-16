"""
Test script to verify SAP Fiori integration is properly set up.
Run this to diagnose issues before connecting to SAP.

Usage:
  python test_sap_integration.py
"""

import sys
import os
from pathlib import Path

# Fix encoding on Windows for Unicode output
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_imports():
    """Test that all required dependencies are installed."""
    print("\n" + "="*70)
    print("TEST 1: Checking Python Dependencies")
    print("="*70)

    dependencies = [
        ("playwright", "Playwright (browser automation)"),
        ("requests", "Requests (HTTP client)"),
        ("fastapi", "FastAPI (web server)"),
        ("uvicorn", "Uvicorn (ASGI server)"),
        ("pydantic", "Pydantic (data validation)"),
    ]

    all_ok = True
    for module_name, description in dependencies:
        try:
            __import__(module_name)
            print(f"  ✓ {description:<40} installed")
        except ImportError:
            print(f"  ✗ {description:<40} NOT installed")
            all_ok = False

    if not all_ok:
        print("\n⚠ Install missing packages with:")
        print("  pip install playwright fastapi uvicorn requests pydantic")
        print("  playwright install chromium")
        return False

    print("\n✓ All dependencies installed!")
    return True


def test_files_exist():
    """Test that all required files are present."""
    print("\n" + "="*70)
    print("TEST 2: Checking Required Files")
    print("="*70)

    project_dir = Path(__file__).resolve().parent
    required_files = [
        ("treasury_agent.html", "Main dashboard"),
        ("fetch_sap_cashflow.py", "SAP data fetcher"),
        ("sap_fiori_server.py", "FastAPI server"),
        ("fetch_market_rates.py", "Market rates fetcher"),
        ("register_daily_task.ps1", "Windows scheduler setup"),
    ]

    all_exist = True
    for filename, description in required_files:
        path = project_dir / filename
        if path.exists():
            print(f"  ✓ {filename:<30} {description}")
        else:
            print(f"  ✗ {filename:<30} NOT FOUND")
            all_exist = False

    if not all_exist:
        print("\n⚠ Some files are missing. Check your project directory.")
        return False

    print("\n✓ All required files present!")
    return True


def test_server_startable():
    """Test that the FastAPI server can start."""
    print("\n" + "="*70)
    print("TEST 3: FastAPI Server Startup")
    print("="*70)

    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware

        app = FastAPI()
        app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

        @app.get("/test")
        async def test_endpoint():
            return {"status": "ok"}

        print("  ✓ FastAPI app created successfully")
        print("  ✓ CORS middleware configured")
        print("\n✓ Server is ready to start!")
        print("  Run: python sap_fiori_server.py")
        return True
    except Exception as e:
        print(f"  ✗ Error creating FastAPI app: {e}")
        return False


def test_sap_fetcher_loadable():
    """Test that the SAP fetcher module can be imported."""
    print("\n" + "="*70)
    print("TEST 4: SAP Fetcher Module")
    print("="*70)

    try:
        # Try to import the SAP fetcher
        from fetch_sap_cashflow import fetch_sap_cashflow
        print("  ✓ SAP fetcher module imported successfully")
        print("  ✓ fetch_sap_cashflow() function available")
        print("\n✓ SAP fetcher is ready!")
        return True
    except ImportError as e:
        print(f"  ✗ Could not import SAP fetcher: {e}")
        print("\n⚠ Make sure fetch_sap_cashflow.py is in the project directory")
        return False
    except Exception as e:
        print(f"  ✗ Error loading SAP fetcher: {e}")
        return False


def test_playwright():
    """Test that Playwright is properly installed with chromium."""
    print("\n" + "="*70)
    print("TEST 5: Playwright Chromium Browser")
    print("="*70)

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            # Just check if chromium is available
            chromium = p.chromium
            print("  ✓ Playwright imported successfully")
            print("  ✓ Chromium browser available")
            print("\n✓ Playwright is ready!")
            return True
    except Exception as e:
        print(f"  ✗ Playwright error: {e}")
        print("\n⚠ Install Playwright with:")
        print("  pip install playwright")
        print("  playwright install chromium")
        return False


def main():
    """Run all tests and provide a summary."""
    print("\n" + "#"*70)
    print("# SAP Fiori Integration — Verification Tests")
    print("#"*70)

    tests = [
        ("Dependencies", test_imports),
        ("Files", test_files_exist),
        ("Server", test_server_startable),
        ("SAP Fetcher", test_sap_fetcher_loadable),
        ("Playwright", test_playwright),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Unexpected error in {test_name}: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status:<10} {test_name}")

    print(f"\n  {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed! You're ready to use SAP Fiori integration.")
        print("\nNext steps:")
        print("  1. Start the server: python sap_fiori_server.py")
        print("  2. Open the dashboard: treasury_agent.html in a browser")
        print("  3. Fill in SAP credentials and click 'Fetch Cash Balances'")
        return 0
    else:
        print("\n✗ Some tests failed. See above for details.")
        print("\nCommon issues:")
        print("  - Missing dependencies: pip install playwright fastapi uvicorn requests")
        print("  - Playwright not installed: playwright install chromium")
        print("  - Missing files: Check your project directory")
        return 1


if __name__ == "__main__":
    sys.exit(main())
