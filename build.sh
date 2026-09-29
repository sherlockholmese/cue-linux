#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$(readlink -f -- "$0")")"

if (( EUID == 0 )); then
    echo 'Run this script as your normal user, not with sudo.' >&2
    exit 1
fi
if ! command -v makepkg >/dev/null; then
    echo 'This builder requires Arch Linux (or an Arch-based distribution) and makepkg.' >&2
    exit 1
fi
for tool in 7z python unzip curl; do
    if ! command -v "$tool" >/dev/null; then
        echo "Missing $tool. Install prerequisites: sudo pacman -S --needed base-devel 7zip python unzip curl" >&2
        exit 1
    fi
done

export SRCDEST="$PWD/.cache" BUILDDIR="$PWD/.build" PKGDEST="$PWD/dist"
mkdir -p "$SRCDEST" "$BUILDDIR" "$PKGDEST"
# No -s or -i: building must not install packages or invoke sudo.
makepkg --force --cleanbuild "$@"
printf '\nPackage output: %s\n' "$PKGDEST"
makepkg --packagelist
