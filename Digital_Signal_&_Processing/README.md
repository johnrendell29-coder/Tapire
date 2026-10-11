# CPE20 Laboratory Activities

**Student:** Carl Jayson Eli Bonaobra  
**Section:** CPE4A  
**Program:** Computer Engineering

## Project Overview

This project presents five laboratory activities covering discrete-time signal
processing and digital image analysis. The activities progress from representing
and transforming numerical sequences to counting objects, classifying Philippine
banknotes, and recognizing plate numbers. Python, NumPy, Matplotlib, OpenCV, and
Tesseract OCR provide the computational and visualization tools used in the project.

## Activity 1: Discrete-Time Signals and Basic Operations

**Notebook:** [act01.ipynb](Activity_01/act01.ipynb)

This activity introduces the representation and analysis of discrete-time signals
using sample values and their corresponding indices. It demonstrates time shifting,
time reversal, and signal energy calculation, showing how each operation affects
a finite sequence. Additional examples illustrate an arbitrary sequence, the unit
impulse, unit step, ramp, and a sampled cosine waveform.

NumPy manages the sequence values and indices, while Matplotlib stem plots display
the individual samples. Numerical results and labeled plots connect the mathematical
expressions to their computational representations.

## Activity 2: Interactive Sequence Operations Visualizer

**Application:** [act02-operational_sequence.py](Activity_02/act02-operational_sequence.py)

This activity provides a Tkinter desktop application for exploring discrete-time
sequence transformations. Users enter a sequence, its starting index, and a shift
amount to calculate time delay, time advance, time reversal, and signal energy.
The application also demonstrates two procedures for obtaining `y[n] = x[k - n]`:
shifting before reversal and reversing before shifting.

The interface presents numerical results alongside embedded Matplotlib stem plots.
Intermediate sequences illustrate the composite operations, and a reset control
restores the worked example. The activity reinforces the relationship between
sample indices, transformation order, and the resulting signal.

## Activity 3: Object Counting through Image Segmentation

**Notebook:** [act03-object_counting_bonaobra.ipynb](Activity_03/act03-object_counting_bonaobra.ipynb)  
**Input:** `Activity_03/images/coins.png`

This activity applies image segmentation to detect and count coins against a bright
background. The image is separated into red, green, and blue channels, and threshold
masks are combined to identify the background. Inverting the combined mask produces
the foreground regions used for object detection.

Flood filling closes gaps within the detected regions, and morphological opening
reduces small artifacts and weak connections. Connected-component analysis then
identifies candidate objects, with area and aspect-ratio filters retaining
substantial, approximately circular regions. The output includes intermediate
processing stages, numbered bounding boxes, and the calculated object count.

The activity focuses on object counting; coin denominations are not assigned from
their apparent size.

## Activity 4: Philippine Banknote Recognition by Color

**Notebook:** [act04-money_recognition_bonaobra.ipynb](Activity_04/act04-money_recognition_bonaobra.ipynb)  
**Input:** `Activity_04/images/bills.png`

This activity demonstrates color-based classification of Philippine banknotes.
The image is converted to the HSV color space, where predefined ranges identify
color evidence associated with the 20, 50, 100, 200, 500, and 1,000 peso
denominations. Foreground segmentation, contour detection, and morphological
opening isolate individual banknote regions.

Each detected banknote is evaluated using the color evidence within its interior.
Minimum support and separation criteria determine whether a denomination can be
assigned. Each region receives at most one classification, and ambiguous regions
remain unclassified and are excluded from the recognized subtotal.

The output displays color masks, classification scores, annotated banknotes, the
detected banknote count, and the total recognized value. This exercise demonstrates
visual classification and does not assess currency authenticity.

## Activity 5: Philippine Plate Number Recognition

**Notebook:** [act05-plate_recognition_bonaobra.ipynb](Activity_05/act05-plate_recognition_bonaobra.ipynb)  
**Inputs:** Six plate images in `Activity_05/images/`

This activity combines image preprocessing with optical character recognition to
extract text from frontal plate images. A central crop isolates the number band,
followed by grayscale conversion, Gaussian smoothing, and Otsu thresholding to
separate characters from the background.

Contour filters select tall character regions and reduce interference from plate
borders, mounting holes, QR codes, and small captions. The selected regions are
placed on a white background, resized, and padded before being passed to Tesseract
OCR. Single-character or single-line recognition is selected according to the
number of detected regions, and the returned text is restricted to uppercase
letters and digits.

For each image, the notebook displays the original plate, thresholded image,
selected character regions, and OCR result. Recognized text is generated from the
image content and should be checked against the original plate.

## Source Materials

The activities use the learning workflows from the supplied `CPE20.zip` reference
by Guian Jaundell R. Manalo. Activity 1 preserves the original exercise cells with
an added student identification cell, and Activity 2 preserves the reference
application. Activities 3–5 contain adapted implementations for the supplied images.

All eight input PNG files are retained unchanged from **CPE20 erinx version**:
`coins.png` for Activity 3, `bills.png` for Activity 4, and six plate images for
Activity 5. The supplied filenames, including `goverment.png` and `higher ups.png`,
are preserved.

## Setup and Execution

1. Open the **CPE20_Bonaobra** folder in VS Code.
2. Install Python 3.10 or newer and the VS Code Python and Jupyter extensions.
   Activity 2 also requires a Python installation with Tkinter support.
3. Create a virtual environment and install the project dependencies:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. Install **Tesseract OCR** with English language data for Activity 5:

   ```powershell
   winget install --id UB-Mannheim.TesseractOCR --exact
   ```

   Restart VS Code after installation. The notebook searches PATH and the standard
   Windows Program Files installation folder. For a custom installation, set
   `TESSERACT_CMD` to the executable path before opening VS Code. Tesseract is a
   separate application and is not installed by `pip`.
5. Open a notebook, select `.venv` as its Python kernel, and choose **Run All**.
   Activities 3–5 support execution from the project folder or their respective
   activity folders. Activity 5 also supports execution from the parent `CODES`
   workspace.
6. Launch the Activity 2 desktop application from the project terminal:

   ```powershell
   .\.venv\Scripts\python.exe Activity_02/act02-operational_sequence.py
   ```

Alternatively, start Jupyter from the project folder:

```powershell
.\.venv\Scripts\python.exe -m notebook
```

## Scope and Limitations

The image-processing thresholds are calibrated for the supplied images. Touching
coins may merge into a single region, while overlapping banknotes, lighting
conditions, and different currency series can affect segmentation and color
classification. Plate recognition assumes frontal images in which the plate fills
most of the frame; full vehicle scenes require an additional localization step.
OCR may confuse similar letters and digits, so visual verification remains necessary.

Execution results and validation details are documented in
[TEST_REPORT.md](TEST_REPORT.md).
