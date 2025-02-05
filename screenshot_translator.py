import tkinter as tk
import tkinter.font as tkFont
import pyautogui
from PIL import Image, ImageTk
import pytesseract
import keyboard
import threading
import concurrent.futures
import time
from googletrans import Translator

# Configure tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'【Path to Tesseract-OCR executable】'

# Dummy NLP model for text classification
def classify_text_context(text):
    """Classify the context of the text. Academic? Casual? Forum? Who knows..."""
    if any(word in text.lower() for word in ['cell', 'protein', 'dna', 'research']):
        return "academic"
    elif any(word in text.lower() for word in ['lol', 'omg', 'wtf']):
        return "forum"
    else:
        return "general"

# Translation worker using Google Translate API
def translate_worker(text, target_lang, context, variant):
    """Just a quick translation... I hope it works..."""
    time.sleep(0.5)  # Faster delay for simulation
    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    return translated.text

def run_matntranslate_multithread(text, target_lang, context):
    """Multi-thread translation with speed! Let's gooo!"""
    variants = ["Version 1", "Version 2", "Version 3"]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_variant = {
            executor.submit(translate_worker, text, target_lang, context, variant): variant
            for variant in variants
        }
        for future in concurrent.futures.as_completed(future_to_variant):
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                results.append(f"Error with {future_to_variant[future]}: {exc}")
    return results

# Evaluate translations, picking the best one based on the text length
def evaluate_translations(original_text, translations):
    """Choose the best translation... I'm sure it'll be fine..."""
    best = max(translations, key=lambda t: len(t))
    return best

# Main translation flow: context -> multi-thread -> evaluation
def advanced_translate(text, translation_direction):
    """We got this... Let's translate!"""
    context = classify_text_context(text)
    print(f"Context: {context}")

    target_lang = "zh-cn" if translation_direction == "en_to_zh" else "en"

    translations = run_matntranslate_multithread(text, target_lang, context)
    print(f"Translation results: {translations}")

    best_translation = evaluate_translations(text, translations)
    return best_translation

class ScreenCaptureApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.config(bg="black")

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.screenshot = pyautogui.screenshot()
        self.tk_screenshot = ImageTk.PhotoImage(self.screenshot)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_screenshot)

        self.root.bind("<Escape>", self.exit_capture)

        self.translation_direction = tk.StringVar(value="en_to_zh")
        self.create_translation_options()

        self.root.mainloop()

    def create_translation_options(self):
        """Add translation direction options at the top."""
        frame = tk.Frame(self.root, bg="black")
        frame.pack(side=tk.TOP, fill=tk.X)

        en_to_zh_radio = tk.Radiobutton(frame, text="English to Chinese", variable=self.translation_direction,
                                        value="en_to_zh", bg="black", fg="white")
        en_to_zh_radio.pack(side=tk.LEFT, padx=5, pady=5)

        zh_to_en_radio = tk.Radiobutton(frame, text="Chinese to English", variable=self.translation_direction,
                                        value="zh_to_en", bg="black", fg="white")
        zh_to_en_radio.pack(side=tk.LEFT, padx=5, pady=5)

    def on_press(self, event):
        """Start selecting area when mouse pressed."""
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
                                                 outline="red", width=2)

    def on_drag(self, event):
        """Drag to update selection area."""
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        """Release mouse to start OCR and translation."""
        self.capture_area(self.start_x, self.start_y, event.x, event.y)

    def capture_area(self, x1, y1, x2, y2):
        """Capture area, OCR, translate, and show result."""
        left, top, right, bottom = min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
        cropped = self.screenshot.crop((left, top, right, bottom))
        cropped.save(r"【Path to save captured image】")
        print("Captured as selected_area.png")

        text = pytesseract.image_to_string(cropped)
        text = text.replace('\n', ' ')  # Remove newline chars
        print(f"Recognized text: {text}")

        best_translation = advanced_translate(text, self.translation_direction.get())
        print(f"Best translation: {best_translation}")

        self.show_translation(best_translation, x2, y2)

    def show_translation(self, text, x, y):
        """Show translation at the mouse release position."""
        popup = tk.Toplevel(self.root)
        popup.wm_overrideredirect(True)

        font_size = 12 if len(text) <= 1500 else 10
        font_setting = ("Source Han Sans", font_size, "bold")
        myfont = tkFont.Font(family="Source Han Sans", size=font_size, weight="bold")

        text_width = myfont.measure(text)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        max_width = int(screen_width * 0.4)
        max_height = int(screen_height * 0.5)

        ideal_width = min(text_width + 20, max_width)
        ideal_height = min(int(myfont.metrics("linespace") * (len(text) / 50 + 1)), max_height)

        if len(text) > 1500:
            ideal_height = int(ideal_width * (16 / 9))
            if ideal_height > max_height:
                ideal_height = max_height
                ideal_width = int(ideal_height * (9 / 16))

        text_widget = tk.Text(
            popup, wrap=tk.WORD, font=font_setting,
            bg="#f8f0e3", fg="#2b2aaa", relief=tk.FLAT
        )
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)

        scrollbar = tk.Scrollbar(popup, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        if x + ideal_width > screen_width:
            x = screen_width - ideal_width - 10
        if y + ideal_height > screen_height:
            y = screen_height - ideal_height - 50

        popup.geometry(f"{ideal_width}x{ideal_height}+{x}+{y}")
        popup.bind("<Button-1>", lambda e: self.exit_translation_mode(popup))
        self.root.bind("<Button-1>", lambda e: self.exit_translation_mode(popup))

    def exit_translation_mode(self, popup):
        """Exit translation mode when clicked."""
        popup.destroy()
        self.root.destroy()

    def exit_capture(self, event):
        """Exit capture on pressing ESC."""
        self.root.destroy()

def start_app():
    """Start the app with hotkey."""
    global app_running
    if not app_running:
        app_running = True
        ScreenCaptureApp()
        app_running = False

if __name__ == "__main__":
    app_running = False
    threading.Thread(target=lambda: keyboard.add_hotkey('ctrl+f1', start_app)).start()
    print("Press Ctrl+F1 to start the screenshot translation tool, and it will keep showing the result until you click.")
    keyboard.wait('esc')
