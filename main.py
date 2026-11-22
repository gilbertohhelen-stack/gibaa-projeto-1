from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import threading
import os

try:
    import yt_dlp
    TEM_YTDLP = True
except:
    TEM_YTDLP = False

class AssistenteApp(App):
    def build(self):
        self.title = "Assistente Baixar Video"
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.titulo = Label(
            text="ASSISTENTE DE DOWNLOAD\nFale ou cole o link",
            font_size=22,
            size_hint_y=0.3
        )
        layout.add_widget(self.titulo)

        self.input_link = TextInput(
            hint_text="Cole aqui o link do YouTube ou Kwai...",
            multiline=False,
            size_hint_y=0.2,
            font_size=18
        )
        layout.add_widget(self.input_link)

        self.btn_baixar = Button(
            text="BAIXAR VIDEO",
            size_hint_y=0.2,
            font_size=20,
            background_color=(0, 0.7, 0, 1)
        )
        self.btn_baixar.bind(on_press=self.baixar)
        layout.add_widget(self.btn_baixar)

        self.btn_voz = Button(
            text="FALAR COMANDO",
            size_hint_y=0.2,
            font_size=20,
            background_color=(0.1, 0.4, 0.9, 1)
        )
        self.btn_voz.bind(on_press=self.ouvir_comando)
        layout.add_widget(self.btn_voz)

        self.status = Label(
            text="Pronto para baixar...",
            font_size=16,
            size_hint_y=0.3
        )
        layout.add_widget(self.status)
        return layout

    def ouvir_comando(self, instance):
        self.status.text = "Fale agora: baixar video + cole o link"

    def baixar(self, instance):
        link = self.input_link.text.strip()
        if not link:
            self.status.text = "Cole um link primeiro!"
            return
        self.status.text = "Baixando... aguarde..."
        threading.Thread(target=self.fazer_download, args=(link,)).start()

    def fazer_download(self, link):
        if not TEM_YTDLP:
            self.status.text = "Erro: yt-dlp nao instalado"
            return
        try:
            pasta = "/storage/emulated/0/Download/AssistenteVideos"
            os.makedirs(pasta, exist_ok=True)
            opcoes = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(pasta, '%(title)s.%(ext)s'),
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                ydl.download([link])
            self.status.text = "Baixado! Pasta Download/AssistenteVideos"
        except Exception as e:
            self.status.text = f"Erro: {str(e)[:100]}"

if __name__ == '__main__':
    AssistenteApp().run()