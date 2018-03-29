# ImageFinder

## Description

This is a tool powered by Python and Selenium python to help users download images with a given keyword from the web.

## Usage

The script accepts 3 parameters:

- `--keyword`: mandatory. The keyword with which the user would like to search from the web
- `--dir`: optional, default to be the current working directory. The root directory to save the downloaded images,
note that the images will not be placed directly in the specified directory, but creating a folder named after
the specified keyword and place all the images into that folder
- `--limit`: optional, default to 10. Indicates the maximum number of images to be downloaded

A sample usage of the script:

`python /path/to/app.py --keyword="iron man" --dir=/tmp/marvel --limit=100`

