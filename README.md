# Cue → Arch Linux

Unofficial repackager for **Cue**. Replaces the macOS ARM64 Electron
runtime with **Electron 43.6.0 for Linux**, preserving the original `app.asar`.
Produces a normal `.pkg.tar.zst` package for pacman. No Wine, emulation, Node.js,
or npm is needed to build or run it.

## Build

On Arch Linux or an Arch-based distribution:

```sh
sudo pacman -S --needed base-devel 7zip python unzip curl
./build.sh
```

Run the builder **without sudo**. It gets the current macOS ARM64 DMG URL from
Cue's public download settings API, downloads the DMG and Linux Electron
archive, and runs `makepkg`. The Electron archive has a pinned SHA-256 checksum.
It does not install the resulting package or automatically install missing
dependencies. If makepkg reports missing dependencies, install those with
pacman and rerun the builder.

On x86-64, the current output is `dist/cue-linux-1.0.3-1-x86_64.pkg.tar.zst`.
The version in the filename follows the URL returned by Cue's API.
The recipe also selects an ARM64 runtime on Arch Linux ARM (`aarch64`), but
that architecture has not been runtime-tested. It builds for the host
architecture, not the DMG's architecture.

```sh
sudo pacman -U dist/cue-linux-1.0.3-1-x86_64.pkg.tar.zst
cue
```

The package installs a launcher, application-menu entry, icon, and `cue://`
URL handler for browser sign-in callbacks. The bundled Chromium sandbox is
retained. Cue may register itself as the default `cue://` handler on launch.
Install the package before signing in: running the extracted executable alone
does not install the required `cue-desktop.desktop` callback handler.

Downloads are cached in `.cache/`; temporary package files are in `.build/`.
Allow roughly 2 GB of free space. Re-running reuses downloaded archives and
rebuilds the package. Delete `.build/` to recover build space, or `.cache/`
to discard downloaded archives. You can also use the PKGBUILD with makepkg
directly to build the fallback Cue 1.0.3 release. The Cue DMG and local
packaging files use `SKIP` checksums; the Electron archives remain pinned.

## Limitations

This is a runtime replacement, not a general macOS binary converter. This
specific app contains portable JavaScript/web assets and no native `.node`
modules. Future versions may need additional porting even if the download
and package build succeed.

Cue's existing updater disables itself on Linux. Rebuild the package to pick
up a newer Cue release; Electron security updates are not automatic.
The app remains proprietary and subject to the vendor's terms. This project
does not grant permission to redistribute it. Authentication and online
features depend on the vendor's services and Linux support is unofficial.
