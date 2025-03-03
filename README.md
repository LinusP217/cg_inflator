# Canvas Grade Inflator
## Introduction

```bash
-----------------------------------------------------------------
   ____                             ____               _
  / ___|__ _ _ ____   ____ _ ___   / ___|_ __ __ _  __| | ___
 | |   / _` | '_ \ \ / / _` / __| | |  _| '__/ _` |/ _` |/ _ \
 | |__| (_| | | | \ V / (_| \__ \ | |_| | | | (_| | (_| |  __/
  \____\__,_|_| |_|\_/ \__,_|___/  \____|_|  \__,_|\__,_|\___|
            |_ _|_ __  / _| | __ _| |_ ___  _ __
             | || '_ \| |_| |/ _` | __/ _ \| '__|
             | || | | |  _| | (_| | || (_) | |
            |___|_| |_|_| |_|\__,_|\__\___/|_|

-----------------------------------------------------------------
A python script 🐍 for instructors wanting to add (or subtract)
points to student grades on Canvas, a capability not available
on the web interface 😠💻.

Ex: +2 grade increment

Student | Old Grade -> New Grade
--------------------------------
John    |      1     |     3
Sarah   |      7     |     9
Andrew  |    None    |   None
Emily   |      0     |     2
```

## Usage

The script runs as a cli program that prompts the user for information. To get going, simply type

```bash
python cg_inflator.py
```
The script will ask for your institutional Canvas url and api key, so have those ready to go.

## Installation

```bash
wget cg_inflator.py
```
Best to run it in a clean conda environment ([instructions]()).

