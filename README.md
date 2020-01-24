# cluster-dataset
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

annoy to copy data from your computer to a lot of computing engines when you are doing data science? try cluster-dataset

## Plan
Support rclone (for cross platform compatibitliy) and rsync (for previous linux cluster)

### Feature to implement
- [ ] automatic sync between local and node
- [ ] avoid `rm` and `ls` thing for cross-platform compatibilty
- [ ] automatic look up between node
- [ ] raise error when conflict
- [ ] under the hood. (Few or none of code  to edit to support
- [ ] unit testing support

## PreRequirement

### Windows

- Download [Rclone](https://rclone.org/downloads/) Windows prebuilt
- Extract prebuilt files on your computer. I recommend to extract files at `%APPDATA%/rclone` to avoid permission problems.
- add rclone to `PATH` in environment variable. It's will make this library see rclone