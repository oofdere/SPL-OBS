---
layout: default
title: iFAQ
nav_exclude: false
---

## (inFrequently Asked Questions)
### Should I run this as administrator?
**NO.** Please don't. It shouldn't need to run as admin and it should never ask to.

### YOU BROKE MY COMPUTER!!!!!!!!!!!!11!!1!
From [the license](https://github.com/oofdere/SPL-OBS/blob/master/LICENSE):
```
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### Is this stable?
It works on my machine.

### What is the default websockets login?
 - Host: `localhost`
 - Port: `4444`
 - Password: `spl-obs`
This can **(and probably should) be changed** by modifying the updater and countdown's configuration files.

### Is this cross-platform?
No, partly because StationPlaylist Studio only runs on Windows so no other testing has been done.
 - Requires GDI+ text sources. Easy fix, but not cross-platform out of the box.
 - Binary (.exe) obviously is not.

### Why are the updater and countdown seperate?
Development is easier this way, and the countdown is the only "real-time"/time-sensitive component. Originally it was one script but it was unwieldy and the countdown was always off.

Also, I plan to split off the countdown into its own package at some point.

### What license is this?
[BSD 3-Clause](https://github.com/oofdere/SPL-OBS/blob/master/LICENSE). [Dependencies](https://github.com/oofdere/SPL-OBS/network/dependencies) may have different licenses, and all licenses must be taken into consideration. See the [LICENSES file](https://github.com/oofdere/SPL-OBS/blob/master/LICENSES).

### Should I let you know if I'm using this or build off of it?
Please do! You are, of course, under no obligation to do so, but I'd be interested in seeing what's done with this, of course.
