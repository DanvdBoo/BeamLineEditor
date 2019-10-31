# BeamLineEditor
Simple Line Editor for BeamNG.drive

Feedback is always welcome, more features to come.

#### Current known bugs in current version:


#### List of features I would like to add (ordered by priority):
- [ ] Toggleable line
- [x] Option to apply current speedup values
- [x] Show z value
- [x] Show velocity or t-value
- [x] Move nodes with the mouse
- [x] Custom logo
- [ ] A proper help page
- [ ] Add additional points to the end of the line
- [ ] Repeat part of line (laps)
- [ ] Select finish line (Add lap-counter on Beam ??)
- [x] Remove nodes

### v0.3
#### Things added:
- Gradients for speed, time and height.
- Move nodes with the mouse.
- Remove nodes from the line.
- Apply partially speeding up the line.

#### Fixes
- Fixed issue where opening a new line wouldn't destroy old data.

#### List of Known bugs

### v0.2
Added the functionallity to move individual nodes. 
Speedup parts of the line.

#### Known bugs
- Line moves while it shouldn't. (fixed in v0.2.1)
- Not automatically add .track.json to file names. (fixed in v0.2.1)

### v0.1.1
Added a more pleasant GUI, including a graph showing all the points of the selected line

### v0.1
* Select input and output file<sup>1</sup>
* Change the speed based on a percentage<sup>2</sup>

1 - If you want a file in the same directory, but don't want to browse again switch the "Set input to output" checkbox on and off. This will set the file path of the input to the output, you can then edit output filename.  
2 - Use negative percentages to slowdown the line
