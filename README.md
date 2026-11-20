# Battle Cats DB

An experimental portfolio and learning project about collecting and organizing
**The Battle Cats** game data. The goal is to build a database that can power a
website and a public, read-only API for information such as cats, talents, and
other game details. I would like the website to offer an experience similar to
[MyGamatoto](https://mygamatoto.com/).

## For readers

This repository is mainly here to introduce the project and show how it is
being built. You do not need to install anything, connect a phone, provide APKs,
or run the extraction workflow to read about the project. Feel free to browse,
download, or fork the repository, under the MIT license.

The extraction tools are part of my behind-the-scenes data collection process;
they are not the product I expect other people to use. The longer-term plan is
for people to explore the processed data through the website or API.

## Project status

The project is experimental and is being developed as a portfolio piece and
personal learning exercise.

### Available now

- [x] Collect APKs from one authorized Android device with the English game
      installed.
- [x] Detect the installed game's version and merge its APK splits.
- [x] Extract the merged APK and decode its `.list` and `.pack` assets.
- [x] Save extracted and decoded files in version-specific folders for the
      English game.

These features are experimental and describe the maintainer's data-collection
workflow, not something readers need to run.

### Not available yet

- [ ] Support for other regional game versions.
- [ ] A database and automated data-ingestion pipeline.
- [ ] A website for browsing or searching game data.
- [ ] A public, read-only API.
- [ ] Verified coverage of all game data, including assets the game downloads
      separately.

## How the project is intended to work

This is the project's path from my own data collection work to the planned
reader-facing tools. The arrows show the order; readers do not need to perform
these steps.

**English game on my device**  
↓  
**Collect and merge its APKs** — available, experimental  
↓  
**Extract and decode the game assets** — available, experimental  
↓  
**Save the English data in version-specific folders** — available, experimental  
↓  
**Load the data into a database** — planned  
↓  
**Browse it on a website or query the read-only API** — planned

## Repository contents

- `src/extraction/` — code for extracting APK contents.
- `src/decoding/` — code for decoding game asset packs.
- `run.sh` — the maintainer's current collection workflow.
- `lib/` — supporting project tools.
- `apks/` and `game_data/` — local project data organized by region and version.

## Future project links

- Website: coming soon
- API documentation: coming soon
- Related projects: coming soon

## Credits and attribution

The approach to exploring and organizing Battle Cats data is heavily inspired
by [fieryhenry's Battle Cats Data](https://git.battlecatsmodding.org/fieryhenry/BCData).
Please see that project for its own credits and attribution.

Most of this project's implementation and content are developed by me as part
of the learning process. AI tools have assisted me periodically with research
and implementation, including work involving PyCryptodome, among other things (like this README, lol).

**The Battle Cats** is the property of its respective rights holders. This is
an unofficial fan project and is not affiliated with or endorsed by PONOS.
