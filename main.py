from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.spinner import Spinner
import yt_dlp
import threading

class VideoDownloaderApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label = Label(text="Enter video URL:")
        self.root.add_widget(self.label)

        self.url_entry = TextInput(multiline=False)
        self.root.add_widget(self.url_entry)

        self.download_type = 'video'
        self.quality_var = Spinner(text='Select Quality')

        self.video_button = Button(text="Download Video")
        self.video_button.bind(on_press=self.start_download)
        self.root.add_widget(self.video_button)

        self.progress_label = Label(text="0%")
        self.root.add_widget(self.progress_label)

        self.progress = ProgressBar(max=100)
        self.root.add_widget(self.progress)

        return self.root

    def start_download(self, instance):
        url = self.url_entry.text
        if not url:
            self.progress_label.text = "Please enter a video URL."
            return

        path = "/storage/emulated/0/Download/"  # Adjust path as needed

        download_thread = threading.Thread(target=self.download_video, args=(url, path))
        download_thread.start()

    def download_video(self, url, path):
        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'progress_hooks': [self._progress_hook],
            'format': 'bestaudio/best' if self.download_type == 'audio' else 'best',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.root.after(0, lambda: self.show_success())
        except Exception as e:
            self.root.after(0, lambda: self.show_error(e))

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
            self.progress.value = percent
            self.progress_label.text = f"{int(percent)}%"

    def show_success(self):
        self.progress_label.text = "Download completed successfully!"

    def show_error(self, e):
        self.progress_label.text = f"Error: {e}"

if __name__ == "__main__":
    VideoDownloaderApp().run()
