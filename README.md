# BigGrab-Translator - Lazy OCR and Auto Translation Tool
So you want to translate stuff on your screen but don't want to type? Boom. This thing lets you press Ctrl+F1, grab a screenshot, extract the text, and get it translated automatically. Just click anywhere to dismiss it. Easy peasy.
*Byproduct of practicing Python, for personal use, might add more features later.
# How to Install
1.Install Python<br>2.Install these packages:<br>`pip install tkinter pyautogui pillow pytesseract keyboard googletrans concurrent.futures`<br>3.Set up [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)_<br>4.Change this line to your Tesseract path:<br>`pytesseract.pytesseract.tesseract_cmd = r'【Path to Tesseract-OCR executable】`<br>`cropped.save(r"【Path to save captured image】")`<br>
# How to Run
1.Run the script
`python screenshot_translator.py`
2.Press Ctrl+F1 to capture. Press ESC to exit. Click anywhere to close the translation popup.

# Features
Multi-threaded Magic: Translates multiple versions, picks the best one.<br>Supports English <> Chinese: Might add more later... if I feel like it.<br>Minimal UI: No buttons, no menus. Just select and go

# Libraries Used
tkinter: Makes the UI, keeps it old-school<br>
pyautogui: Takes screenshots<br>
Pillow: Handles images and cropping<br>
pytesseract: OCR magic, powered by Tesseract<br>
keyboard: Listens for Ctrl+F1<br>
googletrans: Free translation<br>
concurrent.futures: Makes translation faster with multi-threading<br>

# Things to Fix (Maybe)
Google Translate sometimes derps.
Might add DeepL support (if someone gives me an API key lol).
More languages? Maybe. Not today though
