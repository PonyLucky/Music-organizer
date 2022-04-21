# Music-organizer
Organize music (into folders) from metadata.

## Why?
I'm openning this repo to people who like to cleany organize their music. Also for those who already did the job but have (like me) a device where this organization bother you.

Example:
- You have all your music in one folder -> you want it into artists.
- You have folder per artist but want also per album.
- You have everything good -> one of your device is unable to correctly display music as you want. Then you need the `artist/album` orga to become `artist`.

## How?
This repo is a simple python script that will help you to organize your music.

Modes:
- `--artist`: will create a folder per artist.
- `--album`: will create a folder per artist/album.
- `--all`: will move all files into a single folder (root).

## Disclaimer
For this script to work, you need to have a music file (like `.mp3` or `.flac`) with the following metadata tags:
- `artist`
- `album`
