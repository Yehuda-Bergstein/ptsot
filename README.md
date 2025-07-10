# Perspective Taking/Spatial Orientation Test (Hebrew Version)

This project is a digital adaptation of the updated version of the [Spatial Orientation Test](https://hegarty-lab.psych.ucsb.edu/node/221) that was developed by [Friedman et al. (2019)](https://doi.org/10.3758/s13428-019-01277-3) in 2019.
This fork is based on a python project developed for the original version of the test (https://github.com/TimDomino/ptsot), but adds new features based on the Java version described by Friedman et al.(2019).
All the changes made from the original [repo](https://github.com/TimDomino/ptsot) are summarised below:

| Area         | Added feature                                       | Implementation notes                             |
| ------------ | --------------------------------------------------- | ------------------------------------------------ |
| Localization | Hebrew (M/F) + RTL support                          | `LIST_OF_TEXTS_*`, `RTL_text`, `linebreak_text`  |
| Practice     | 4 guided practice items with flashing guides        | `TASK_ITEMS`, `example_line_*` in `on_key_press` |
| Instructions | 3 instruction windows + end-of-task pop-up          | `create_*_instruction_window`, `CustomDialog`    |
| Layout       | Side-by-side object array ↔ answer circle           | `create_test_window` Gridspec                    |
| UI scaling   | Optional setting of the DPI and window size on start| logic in `main`; `matplotlib.use('TkAgg')`       |
| Timing       | Hard 5-min timer with autosave                      | `update_time`; timeout in `on_close`             |
| Completion   | Large pop-up on finish or timeout                   | `show_popup_message`                             |
| Logging      | Trial-level CSV + summary stats                     | writes in `on_key_press` & `main`                |
| Prompts      | Start-up dialogs (ID, gender, DPI) + answer preview | input dialogs & preview code in `main`           |

## Hebrew Version Features

This version includes:
- Complete Hebrew translation of all test instructions and interface elements
- Gender-specific Hebrew text versions (male and female participants)
- Right-to-left (RTL) text rendering using the python-bidi library
- Hebrew task text stored in `all_hebrew_task_text.csv` (not needed to run the task)
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

## Executable Version

A standalone executable version is available in the `EXE_files/` directory as `perspective_taking_test_friedman_2019_version_1.0.exe`.

**Requirements for running the executable:**
- The `Data/` directory with required image files must be in the same folder as the executable
- All other dependencies are built into the executable
- No Python installation required on the target machine

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
