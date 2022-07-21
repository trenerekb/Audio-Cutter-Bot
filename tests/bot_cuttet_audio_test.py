import unittest
from audio_cutter_bot.bot import bot_main
import os.path
from pytube import YouTube


class BotCutterAudio(unittest.TestCase):

    def setUp(self) -> None:
        test_url = 'https://youtu.be/XUcpmN0abno'
        self.yt = YouTube(test_url)
        self.test_path = 'd:\\Python\\audio_cutter_bot\\Requenze, WAYVEE, N.E.B - Talk My Crap (Magic Free Release).mp3'
        self.download_path = "d:\\Python\\audio_cutter_bot"
        self.name_audio = bot_main.editing_name_track(self.yt.title)

    def test_a_del_letter(self):
        self.assertEqual(bot_main.editing_name_track('П/р|\<ив:е!т, к*ак д>е;л"а?'), 'Привет, как дела')

    def test_b_download_audio(self):
        bot_main.download_audio(self.yt, self.download_path, self.name_audio)
        self.assertTrue(os.path.isfile(self.test_path))

    def test_c_del_audio(self):
        bot_main.del_audio(self.download_path, self.name_audio)
        self.assertFalse(os.path.isfile(self.test_path))


if __name__ == '__main__':
    unittest.main()
