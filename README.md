# Perspective Taking/Spatial Orientation Test (Hebrew Version)

Hebrew electronic version of the "Perspective Taking/Spatial Orientation Test" by Hegarty, Kozhevnikov and Waller (also referred to as "Object Perspective/Spatial Orientation Test"). This version was recreated from the original fork after an updated Java version was released in 2019.

This implementation avoids the need for measuring the participants' response angles by hand and for computing the delta angle to the correct solution. The following document hosted by the Spatial Intelligence and Learning Center served as a reference for the implementation: https://www.silc.northwestern.edu/object-perspective-spatial-orientation-test/ (accessed 10 Nov 2019).

The test is based on the two main papers:

 * Hegarty, M., & Waller, D. (2004). A dissociation between mental rotation and perspective-taking spatial abilities. Intelligence, 32, 175-191.

 * Kozhevnikov, M., & Hegarty, M. (2001). A dissociation between object-manipulation and perspective-taking spatial abilities. Memory & Cognition, 29, 745-756.

## Hebrew Version Features

This version includes:
- Complete Hebrew translation of all test instructions and interface elements
- Gender-specific Hebrew text versions (male and female participants)
- Right-to-left (RTL) text rendering using the python-bidi library
- Hebrew task text stored in `all_hebrew_task_text.csv`
- Screenshots and documentation for both male and female Hebrew versions
- Maintained compatibility with the original test methodology and scoring

## Test Structure

- **4 example tasks** for practice and familiarization
- **12 actual test trials** for scoring
- **5-minute time limit** for completion
- Interactive GUI with mouse-based angle selection
- Real-time visual feedback during practice trials

## Dependencies
 * Matplotlib
 * NumPy
 * python-bidi - for proper Hebrew right-to-left text rendering
 * Tkinter - for dialog boxes and user input (usually included with Python)

Install all dependencies using:
```bash
pip install -r requirements.txt
```

## Required Data Files

The test requires the following image files to be present in the `Data/` directory:
- `2019v_object_array.png` - Main object array display
- `heb_screenshot_.png` - Hebrew instruction screenshot

## Usage Instructions

1. Run the test: `python3 perspective_taking_test_friedman_2019_version.py`

2. **Input participant information:**
   - Enter participant ID (determines output file names)
   - Enter gender (M/F) to select appropriate Hebrew text version

3. **Configure display settings (optional):**
   - Enter DPI and font sizes, or press Enter for defaults
   - Default: DPI=100, instruction font=15, test font=13
   - Example input: `100 15 13`

4. **Test flow:**
   - Hebrew instructions are displayed with RTL formatting
   - Practice with 4 example tasks (correct answers shown in red)
   - Complete 12 timed test trials
   - Use mouse to set response angle on the circular interface
   - Press spacebar to confirm each answer and proceed

## Output Files

The test generates two output files per participant:

1. **Text file**: `results-[ID].txt`
   - Task number, correct angle, logged angle, absolute error
   - Average errors for all tasks and test-only tasks

2. **CSV file**: `results-[ID]-[timestamp].csv` 
   - Same data as text file plus elapsed time per task
   - Timestamped filename prevents overwrites
   - Headers: task_id, correct_angle, logged_angle, error, Time elapsed (s)

## Scoring

- **Primary measure**: Absolute angular error in degrees
- **Final scores**: 
  - Overall average error (all 16 tasks)
  - Test-only average error (12 test trials, excluding examples)
- **Time constraint**: Test automatically terminates after 5 minutes

## Screenshots

### Main Test Interface
![Hebrew Test Interface](Data/heb_screenshot_.png)

### First Instruction Window
![First Instruction Window](Data/example_image_first_window.png)

### Object Array Display
![Object Array](Data/2019v_object_array.png)

### Example Task
![Example Task](Data/Esample0.png)
