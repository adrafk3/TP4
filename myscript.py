import os
import sys
import subprocess

def run(cmd):
    print(f"+ {cmd}", flush=True)
    result = subprocess.call(cmd, shell=True)
    if result != 0:
        print(f"⚠️ Command failed with code {result}: {cmd}", flush=True)
    return result

def main():
    bad = os.environ.get("BAD_HASH")
    good = os.environ.get("GOOD_HASH")

    if not bad or not good:
        print("❌ Erreur : les variables BAD_HASH et GOOD_HASH ne sont pas définies.")
        sys.exit(2)

    print(f"==> Lancement du bisect entre :\n BAD = {bad}\n GOOD = {good}\n", flush=True)

    run("git reset --hard")
    run("git clean -xfd")

    try:
        run("git bisect reset")
        run(f"git bisect start {bad} {good}")
        result = run("git bisect run python manage.py test")
    finally:
        run("git bisect reset")

    if result == 0:
        print("\n✅ Bisect terminé sans erreur.")
    else:
        print("\n❌ Bisect terminé avec erreurs.")
    sys.exit(result)

if __name__ == "__main__":
    main()
