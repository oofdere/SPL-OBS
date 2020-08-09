# SPL-OBS
Plug-in for linking the Now Playing information in **StationPlaylist Studio** to **OBS Studio** ~~and **Twitch**~~ *(Soon™)*

- [SPL-OBS](#spl-obs)
  - [Documentation (*Coming Soon™*)](#documentation-coming-soon)
  - [Requirements](#requirements)
  - [Roadmap](#roadmap)
  - [iFAQ (inFrequently Asked Questions)](#ifaq-infrequently-asked-questions)
    - [Is this stable?](#is-this-stable)
    - [What is the default websockets login?](#what-is-the-default-websockets-login)
    - [Is this cross-platform?](#is-this-cross-platform)
    - [What license is this?](#what-license-is-this)
    - [Should I let you know if I'm using this or build off of it?](#should-i-let-you-know-if-im-using-this-or-build-off-of-it)

## Documentation (*Coming Soon™*)
Essentially, under `Now Playing` in the StationPlaylist options, you use `spls-template.yml` as your primary input template and output it to `input.yml` in the same folder.

Same thing for the countdown, but you use the secondary output, make the template `%S`, and output to `duration.txt`.


## Requirements
 - OBS Studio with [websockets plugin](https://github.com/Palakis/obs-websocket)
   - 
 - Python >= 3.8 (3.8.5 from the Microsoft Store was used for development)
   - watchdog
   - pyyaml
   - obs-websocket-py
 - Windows 10
 - StationPlaylist Studio (the demo works as well)
 - Music or other audio files with proper metadata

## Roadmap
- [X] Create YAML Template for StationPlaylist
- [x] Communicate with OBS via websockets
- [x] Make countdown synced to the system clock
- [x] Reduce I/O accesses
- [x] Add Unicode Support
- [ ] Implement scene switching in OBS
- [ ] Implement asyncio
- [ ] Implement dynamic Twitch titler
- [ ] Improve multithreading/general performance
- [ ] Add a GUI
- [ ] Add a way to configure the settings that isn't "go into the code and find the thing to change"

Suggest features by opening an issue.

## iFAQ (inFrequently Asked Questions)
### Is this stable?
Probably. It works on my machine.

### What is the default websockets login?
 - Host: `localhost`
 - Port: `4444`
 - Password: `spl-obs`

This can (and probably should) be changed by modifying the `OBS Websocket Settings` section on `script.py` and `countdown.py`.

This cannot yet be changed for the binary (exe) distribution.

### Is this cross-platform?
~~Technically it should be but StationPlaylist only runs on Windows so no other testing has been done.~~ Requires GDI+ text sources. Easy fix, but not cross-platform out of the box.

### What license is this?
Will figure out at some point, will be free as in freedom, for now is free as in free beer except the source is also available.

### Should I let you know if I'm using this or build off of it?
Please do! You are, of course, under no obligation to do so, but I'd be interested in seeing what's done with this, of course.
