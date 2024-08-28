import wx
import pygame
import pyttsx3
from gtts import gTTS
import speech_recognition as sr
import threading
import time
from googletrans import Translator
import os

class TextToSpeechGUI(wx.Frame):
    def __init__(self):
        super().__init__(None, title="VocalEase", size=(800, 600))
        pygame.init()
        pygame.mixer.init()
        self.engine = pyttsx3.init()
        self.translator = Translator()
        self.default_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.default_font_size = 10
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)
        self.text_to_speech_tab = wx.Panel(notebook)
        self.create_text_to_speech_tab(self.text_to_speech_tab)
        notebook.AddPage(self.text_to_speech_tab, "Text to Speech")
        self.speech_to_text_tab = wx.Panel(notebook)
        self.create_speech_to_text_tab(self.speech_to_text_tab)
        notebook.AddPage(self.speech_to_text_tab, "Speech to Text")
        self.translation_tab = wx.Panel(notebook)
        self.create_translation_tab(self.translation_tab)
        notebook.AddPage(self.translation_tab, "Translation")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_SIZE, self.on_resize)

    def create_text_to_speech_tab(self, tab):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.text_area = wx.TextCtrl(tab, style=wx.TE_MULTILINE)
        self.text_area.SetFont(self.default_font)
        vbox.Add(self.text_area, 1, wx.ALL | wx.EXPAND, 10)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.open_file_button = wx.Button(tab, label="Open File")
        self.open_file_button.Bind(wx.EVT_BUTTON, self.on_open_file)
        button_sizer.Add(self.open_file_button, 0, wx.ALL | wx.CENTER, 5)

        self.speak_button = wx.Button(tab, label="Speak")
        self.speak_button.Bind(wx.EVT_BUTTON, self.on_speak)
        button_sizer.Add(self.speak_button, 0, wx.ALL | wx.CENTER, 5)

        self.save_speech_button = wx.Button(tab, label="Save Speech")
        self.save_speech_button.Bind(wx.EVT_BUTTON, self.on_save_speech)
        button_sizer.Add(self.save_speech_button, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(button_sizer, 0, wx.ALL | wx.CENTER, 10)

        font_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.font_picker = wx.FontPickerCtrl(tab, font=self.default_font)
        self.font_picker.Bind(wx.EVT_FONTPICKER_CHANGED, self.on_font_change)
        font_sizer.Add(wx.StaticText(tab, label="Font:"), 0, wx.ALL | wx.CENTER, 5)
        font_sizer.Add(self.font_picker, 1, wx.ALL | wx.EXPAND, 5)

        self.font_size_spinner = wx.SpinCtrl(tab, value=str(self.default_font_size), min=8, max=72)
        self.font_size_spinner.Bind(wx.EVT_SPINCTRL, self.on_font_size_change)
        font_sizer.Add(wx.StaticText(tab, label="Font Size:"), 0, wx.ALL | wx.CENTER, 5)
        font_sizer.Add(self.font_size_spinner, 1, wx.ALL | wx.EXPAND, 5)

        vbox.Add(font_sizer, 0, wx.ALL | wx.EXPAND, 5)

        voice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.voice_choice = wx.RadioBox(tab, label="Select Voice", choices=["Female", "Male"])
        voice_sizer.Add(self.voice_choice, 1, wx.ALL | wx.CENTER, 5)

        self.volume_label = wx.StaticText(tab, label="Volume:")
        voice_sizer.Add(self.volume_label, 0, wx.ALL | wx.CENTER, 5)

        self.volume_slider = wx.Slider(tab, value=50, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL)
        voice_sizer.Add(self.volume_slider, 1, wx.ALL | wx.EXPAND, 5)

        self.rate_label = wx.StaticText(tab, label="Rate:")
        voice_sizer.Add(self.rate_label, 0, wx.ALL | wx.CENTER, 5)

        self.rate_slider = wx.Slider(tab, value=200, minValue=50, maxValue=300, style=wx.SL_HORIZONTAL)
        voice_sizer.Add(self.rate_slider, 1, wx.ALL | wx.EXPAND, 5)

        vbox.Add(voice_sizer, 0, wx.ALL | wx.EXPAND, 5)

        tab.SetSizer(vbox)

    def create_speech_to_text_tab(self, tab):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.speech_text_area = wx.TextCtrl(tab, style=wx.TE_MULTILINE)
        self.speech_text_area.SetFont(self.default_font)
        vbox.Add(self.speech_text_area, 1, wx.ALL | wx.EXPAND, 10)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.record_button = wx.Button(tab, label="Speak to Transcribe")
        self.record_button.Bind(wx.EVT_BUTTON, self.on_record)
        button_sizer.Add(self.record_button, 0, wx.ALL | wx.CENTER, 5)

        self.save_button = wx.Button(tab, label="Save to File")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save_text)
        button_sizer.Add(self.save_button, 0, wx.ALL | wx.CENTER, 5)

        self.transcribe_button = wx.Button(tab, label="Transcribe MP3")
        self.transcribe_button.Bind(wx.EVT_BUTTON, self.on_transcribe_mp3)
        button_sizer.Add(self.transcribe_button, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(button_sizer, 0, wx.ALL | wx.CENTER, 5)

        font_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.font_picker_stt = wx.FontPickerCtrl(tab, font=self.default_font)
        self.font_picker_stt.Bind(wx.EVT_FONTPICKER_CHANGED, self.on_font_change_stt)
        font_sizer.Add(wx.StaticText(tab, label="Font:"), 0, wx.ALL | wx.CENTER, 5)
        font_sizer.Add(self.font_picker_stt, 1, wx.ALL | wx.EXPAND, 5)

        self.font_size_spinner_stt = wx.SpinCtrl(tab, value=str(self.default_font_size), min=8, max=72)
        self.font_size_spinner_stt.Bind(wx.EVT_SPINCTRL, self.on_font_size_change_stt)
        font_sizer.Add(wx.StaticText(tab, label="Font Size:"), 0, wx.ALL | wx.CENTER, 5)
        font_sizer.Add(self.font_size_spinner_stt, 1, wx.ALL | wx.EXPAND, 5)

        vbox.Add(font_sizer, 0, wx.ALL | wx.EXPAND, 5)

        tab.SetSizer(vbox)

    def create_translation_tab(self, tab):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.translation_input_area = wx.TextCtrl(tab, style=wx.TE_MULTILINE)
        self.translation_input_area.SetFont(self.default_font)
        vbox.Add(self.translation_input_area, 1, wx.ALL | wx.EXPAND, 10)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.translate_button = wx.Button(tab, label="Translate")
        self.translate_button.Bind(wx.EVT_BUTTON, self.on_translate)
        button_sizer.Add(self.translate_button, 0, wx.ALL | wx.CENTER, 5)

        self.speak_translation_button = wx.Button(tab, label="Speak Translation")
        self.speak_translation_button.Bind(wx.EVT_BUTTON, self.on_speak_translation)
        button_sizer.Add(self.speak_translation_button, 0, wx.ALL | wx.CENTER, 5)

        self.open_file_translate_button = wx.Button(tab, label="Open File to Translate")
        self.open_file_translate_button.Bind(wx.EVT_BUTTON, self.on_open_file_to_translate)
        button_sizer.Add(self.open_file_translate_button, 0, wx.ALL | wx.CENTER, 5)

        self.speak_to_translation_button = wx.Button(tab, label="Speak to Translate")
        self.speak_to_translation_button.Bind(wx.EVT_BUTTON, self.on_speak_to_translate)
        button_sizer.Add(self.speak_to_translation_button, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(button_sizer, 0, wx.ALL | wx.CENTER, 10)

        language_choices = [
            "Afrikaans", "Albanian", "Arabic", "Armenian", "Azerbaijani",
            "Basque", "Belarusian", "Bengali", "Bosnian", "Bulgarian",
            "Catalan", "Chinese Simplified", "Chinese Traditional", "Croatian",
            "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish",
            "French", "Galician", "Georgian", "German", "Greek", "Gujarati",
            "Haitian Creole", "Hebrew", "Hindi", "Hungarian", "Icelandic",
            "Indonesian", "Irish", "Italian", "Japanese", "Kazakh", "Korean",
            "Kurdish (Kurmanji)", "Kyrgyz", "Latvian", "Lithuanian", "Luxembourgish",
            "Macedonian", "Malagasy", "Malay", "Maltese", "Maori", "Marathi",
            "Mongolian", "Nepali", "Norwegian", "Pashto", "Persian", "Polish",
            "Portuguese", "Romanian", "Russian", "Scottish Gaelic", "Serbian",
            "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Tajik",
            "Tamil", "Tatar", "Telugu", "Thai", "Turkish", "Ukrainian",
            "Urdu", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish",
            "Zulu"
        ]
        self.language_choice = wx.Choice(tab, choices=language_choices)
        self.language_choice.SetSelection(0)
        vbox.Add(self.language_choice, 0, wx.ALL | wx.EXPAND, 10)

        self.translation_output_area = wx.TextCtrl(tab, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.translation_output_area.SetFont(self.default_font)
        vbox.Add(self.translation_output_area, 1, wx.ALL | wx.EXPAND, 10)

        save_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.save_translation_button = wx.Button(tab, label="Save Translated Text")
        self.save_translation_button.Bind(wx.EVT_BUTTON, self.on_save_translation_text)
        save_button_sizer.Add(self.save_translation_button, 0, wx.ALL | wx.CENTER, 5)

        self.save_translation_audio_button = wx.Button(tab, label="Save Translation Speech")
        self.save_translation_audio_button.Bind(wx.EVT_BUTTON, self.on_save_translation_speech)
        save_button_sizer.Add(self.save_translation_audio_button, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(save_button_sizer, 0, wx.ALL | wx.CENTER, 10)

        font_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.font_picker_translation = wx.FontPickerCtrl(tab, font=self.default_font)
        self.font_picker_translation.Bind(wx.EVT_FONTPICKER_CHANGED, self.on_font_change_translation)
        font_sizer.Add(wx.StaticText(tab, label="Font:"), 0, wx.ALL | wx.CENTER, 5)
        font_sizer.Add(self.font_picker_translation, 1, wx.ALL | wx.EXPAND, 5)

        self.font_size_spinner_translation = wx.SpinCtrl(tab, value=str(self.default_font_size), min=8, max=72)
        self.font_size_spinner_translation.Bind(wx.EVT_SPINCTRL, self.on_font_size_change_translation)
        font_sizer.Add(wx.StaticText(tab, label="Font Size:"), 0, wx.ALL | wx.CENTER, 5)
        font_sizer.Add(self.font_size_spinner_translation, 1, wx.ALL | wx.EXPAND, 5)

        vbox.Add(font_sizer, 0, wx.ALL | wx.EXPAND, 5)

        tab.SetSizer(vbox)

    def on_resize(self, event):
        self.Layout()

    def on_open_file(self, event):
        with wx.FileDialog(self, "Open Text File", wildcard="Text files (*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r', encoding='utf-8') as file:
                    self.text_area.SetValue(file.read())
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

    def on_open_file_to_translate(self, event):
        with wx.FileDialog(self, "Open Text File to Translate", wildcard="Text files (*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r', encoding='utf-8') as file:
                    self.translation_input_area.SetValue(file.read())
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

    def on_speak(self, event):
        text = self.text_area.GetValue()
        if text.strip():
            volume = self.volume_slider.GetValue() / 100.0
            rate = self.rate_slider.GetValue()
            self.engine.setProperty('volume', volume)
            self.engine.setProperty('rate', rate)
            voices = self.engine.getProperty('voices')
            voice = self.voice_choice.GetStringSelection().lower()
            if voice == "male":
                self.engine.setProperty('voice', voices[0].id)
            else:
                self.engine.setProperty('voice', voices[1].id)
            self.engine.say(text)
            self.engine.runAndWait()

    def on_save_speech(self, event):
        text = self.text_area.GetValue()
        if text.strip():
            with wx.FileDialog(self, "Save Speech", wildcard="Audio files (*.mp3)|*.mp3",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return
                pathname = fileDialog.GetPath()
                self.engine.save_to_file(text, pathname)
                self.engine.runAndWait()

    def on_speak_to_translate(self, event):
        threading.Thread(target=self.record_and_transcribe2).start()

    def on_record(self, event):
        if not self.check_microphone():
            wx.LogError("Microphone not available.")
            return
        threading.Thread(target=self.record_and_transcribe).start()

    def on_save_text(self, event):
        text = self.speech_text_area.GetValue()
        with wx.FileDialog(self, "Save Text", wildcard="Text files (*.txt)|*.txt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w', encoding='utf-8') as file:
                    file.write(text)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def on_save_translation_text(self, event):
        text = self.translation_output_area.GetValue()
        if not text.strip():
            wx.LogError("No translated text to save.")
            return
        with wx.FileDialog(self, "Save Translated Text", wildcard="Text files (*.txt)|*.txt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w', encoding='utf-8') as file:
                    file.write(text)
            except IOError:
                wx.LogError("Cannot save translated text in file '%s'." % pathname)

    def on_save_translation_speech(self, event):
        text = self.translation_output_area.GetValue()
        if not text.strip():
            wx.LogError("No translated speech to save.")
            return
        language = self.language_choice.GetStringSelection().lower()
        lang_code = {
            "afrikaans": "af", "albanian": "sq", "arabic": "ar", "armenian": "hy",
            "azerbaijani": "az", "basque": "eu", "belarusian": "be", "bengali": "bn",
            "bosnian": "bs", "bulgarian": "bg", "catalan": "ca", "chinese simplified": "zh-CN",
            "chinese traditional": "zh-TW", "croatian": "hr", "czech": "cs", "danish": "da",
            "dutch": "nl", "english": "en", "estonian": "et", "finnish": "fi", "french": "fr",
            "galician": "gl", "georgian": "ka", "german": "de", "greek": "el", "gujarati": "gu",
            "haitian creole": "ht", "hebrew": "iw", "hindi": "hi", "hungarian": "hu",
            "icelandic": "is", "indonesian": "id", "irish": "ga", "italian": "it",
            "japanese": "ja", "kazakh": "kk", "korean": "ko", "kurdish (kurmanji)": "ku",
            "kyrgyz": "ky", "latvian": "lv", "lithuanian": "lt", "luxembourgish": "lb",
            "macedonian": "mk", "malagasy": "mg", "malay": "ms", "maltese": "mt",
            "maori": "mi", "marathi": "mr", "mongolian": "mn", "nepali": "ne",
            "norwegian": "no", "pashto": "ps", "persian": "fa", "polish": "pl",
            "portuguese": "pt", "romanian": "ro", "russian": "ru", "scottish gaelic": "gd",
            "serbian": "sr", "slovak": "sk", "slovenian": "sl", "spanish": "es",
            "swahili": "sw", "swedish": "sv", "tajik": "tg", "tamil": "ta",
            "tatar": "tt", "telugu": "te", "thai": "th", "turkish": "tr",
            "ukrainian": "uk", "urdu": "ur", "uzbek": "uz", "vietnamese": "vi",
            "welsh": "cy", "xhosa": "xh", "yiddish": "yi", "zulu": "zu"
        }.get(language, "hi")
        tts = gTTS(text=text, lang=lang_code)
        with wx.FileDialog(self, "Save Translation Speech", wildcard="Audio files (*.mp3)|*.mp3",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            tts.save(pathname)

    def record_and_transcribe(self):
        text = self.get_text()
        if text:
            wx.CallAfter(self.speech_text_area.SetValue, text)
        else:
            wx.LogError("Failed to transcribe speech.")

    def record_and_transcribe2(self):
        text = self.get_text()
        if text:
            wx.CallAfter(self.translation_input_area.SetValue, text)
        else:
            wx.LogError("Failed to transcribe speech.")

    def get_audio(self):
        ear_robot = sr.Recognizer()
        with sr.Microphone() as source:
            print("Virtual Assistant: Listening...")
            audio = ear_robot.record(source, duration=4)
            try:
                print("Virtual Assistant: Recognizing...")
                text = ear_robot.recognize_google(audio, language="en-US")
                print("You:", text)
                return text
            except Exception as ex:
                print("Virtual Assistant: Error! Please try again.")
                return None

    def get_text(self):
        for i in range(3):
            text = self.get_audio()
            if text:
                return text.lower()
            elif i < 2:
                print("Virtual Assistant: I couldn't hear you clearly. Please try again.")
                time.sleep(3)
        return None

    def on_translate(self, event):
        text = self.translation_input_area.GetValue()
        if not text.strip():
            return
        language = self.language_choice.GetStringSelection().lower()
        lang_code = {
            "afrikaans": "af", "albanian": "sq", "arabic": "ar", "armenian": "hy",
            "azerbaijani": "az", "basque": "eu", "belarusian": "be", "bengali": "bn",
            "bosnian": "bs", "bulgarian": "bg", "catalan": "ca", "chinese simplified": "zh-CN",
            "chinese traditional": "zh-TW", "croatian": "hr", "czech": "cs", "danish": "da",
            "dutch": "nl", "english": "en", "estonian": "et", "finnish": "fi", "french": "fr",
            "galician": "gl", "georgian": "ka", "german": "de", "greek": "el", "gujarati": "gu",
            "haitian creole": "ht", "hebrew": "iw", "hindi": "hi", "hungarian": "hu",
            "icelandic": "is", "indonesian": "id", "irish": "ga", "italian": "it",
            "japanese": "ja", "kazakh": "kk", "korean": "ko", "kurdish (kurmanji)": "ku",
            "kyrgyz": "ky", "latvian": "lv", "lithuanian": "lt", "luxembourgish": "lb",
            "macedonian": "mk", "malagasy": "mg", "malay": "ms", "maltese": "mt",
            "maori": "mi", "marathi": "mr", "mongolian": "mn", "nepali": "ne",
            "norwegian": "no", "pashto": "ps", "persian": "fa", "polish": "pl",
            "portuguese": "pt", "romanian": "ro", "russian": "ru", "scottish gaelic": "gd",
            "serbian": "sr", "slovak": "sk", "slovenian": "sl", "spanish": "es",
            "swahili": "sw", "swedish": "sv", "tajik": "tg", "tamil": "ta",
            "tatar": "tt", "telugu": "te", "thai": "th", "turkish": "tr",
            "ukrainian": "uk", "urdu": "ur", "uzbek": "uz", "vietnamese": "vi",
            "welsh": "cy", "xhosa": "xh", "yiddish": "yi", "zulu": "zu"
        }.get(language, "hi")
        translated = self.translator.translate(text, dest=lang_code).text
        self.translation_output_area.SetValue(translated)

    def on_speak_translation(self, event):
        text = self.translation_output_area.GetValue()
        if not text.strip():
            return
        language = self.language_choice.GetStringSelection().lower()
        lang_code = {
            "afrikaans": "af", "albanian": "sq", "arabic": "ar", "armenian": "hy",
            "azerbaijani": "az", "basque": "eu", "belarusian": "be", "bengali": "bn",
            "bosnian": "bs", "bulgarian": "bg", "catalan": "ca", "chinese simplified": "zh-CN",
            "chinese traditional": "zh-TW", "croatian": "hr", "czech": "cs", "danish": "da",
            "dutch": "nl", "english": "en", "estonian": "et", "finnish": "fi", "french": "fr",
            "galician": "gl", "georgian": "ka", "german": "de", "greek": "el", "gujarati": "gu",
            "haitian creole": "ht", "hebrew": "iw", "hindi": "hi", "hungarian": "hu",
            "icelandic": "is", "indonesian": "id", "irish": "ga", "italian": "it",
            "japanese": "ja", "kazakh": "kk", "korean": "ko", "kurdish (kurmanji)": "ku",
            "kyrgyz": "ky", "latvian": "lv", "lithuanian": "lt", "luxembourgish": "lb",
            "macedonian": "mk", "malagasy": "mg", "malay": "ms", "maltese": "mt",
            "maori": "mi", "marathi": "mr", "mongolian": "mn", "nepali": "ne",
            "norwegian": "no", "pashto": "ps", "persian": "fa", "polish": "pl",
            "portuguese": "pt", "romanian": "ro", "russian": "ru", "scottish gaelic": "gd",
            "serbian": "sr", "slovak": "sk", "slovenian": "sl", "spanish": "es",
            "swahili": "sw", "swedish": "sv", "tajik": "tg", "tamil": "ta",
            "tatar": "tt", "telugu": "te", "thai": "th", "turkish": "tr",
            "ukrainian": "uk", "urdu": "ur", "uzbek": "uz", "vietnamese": "vi",
            "welsh": "cy", "xhosa": "xh", "yiddish": "yi", "zulu": "zu"
        }.get(language, "hi")
        tts = gTTS(text=text, lang=lang_code)
        audio_file = "temp_file" + ".mp3"
        tts.save(audio_file)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            wx.Yield()
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        os.remove(audio_file)

    def on_transcribe_mp3(self, event):
        with wx.FileDialog(self, "Open MP3 File", wildcard="MP3 files (*.mp3)|*.mp3",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            self.transcribe_mp3(pathname)

    def transcribe_mp3(self, mp3_file):
        recognizer = sr.Recognizer()
        audio = sr.AudioFile(mp3_file)
        with audio as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                self.speech_text_area.SetValue(text)
            except sr.UnknownValueError:
                wx.LogError("Could not understand audio.")
            except sr.RequestError:
                wx.LogError("Could not request results from Google Speech Recognition service.")

    def check_microphone(self):
        mic_list = sr.Microphone.list_microphone_names()
        return len(mic_list) > 0

    def on_font_change(self, event):
        font = self.font_picker.GetSelectedFont()
        self.text_area.SetFont(font)

    def on_font_size_change(self, event):
        font_size = self.font_size_spinner.GetValue()
        font = self.text_area.GetFont()
        font.SetPointSize(font_size)
        self.text_area.SetFont(font)

    def on_font_change_stt(self, event):
        font = self.font_picker_stt.GetSelectedFont()
        self.speech_text_area.SetFont(font)

    def on_font_size_change_stt(self, event):
        font_size = self.font_size_spinner_stt.GetValue()
        font = self.speech_text_area.GetFont()
        font.SetPointSize(font_size)
        self.speech_text_area.SetFont(font)

    def on_font_change_translation(self, event):
        font = self.font_picker_translation.GetSelectedFont()
        self.translation_input_area.SetFont(font)
        self.translation_output_area.SetFont(font)

    def on_font_size_change_translation(self, event):
        font_size = self.font_size_spinner_translation.GetValue()
        font_input = self.translation_input_area.GetFont()
        font_output = self.translation_output_area.GetFont()
        font_input.SetPointSize(font_size)
        font_output.SetPointSize(font_size)
        self.translation_input_area.SetFont(font_input)
        self.translation_output_area.SetFont(font_output)

if __name__ == '__main__':
    app = wx.App(False)
    frame = TextToSpeechGUI()
    frame.Show()
    app.MainLoop()
