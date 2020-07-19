import socket
import string
import unittest

import hammer


class TestHammer(unittest.TestCase):
    def test_randomString(self):
        # res =
        self.assertEqual(len(hammer.randomString(10)), 10)
        self.assertTrue(hammer.randomString().isprintable())
        self.assertTrue(set(hammer.randomString()) <= set(string.ascii_letters + string.digits + string.punctuation))

        # self.assertRaises(socket.error, hammer.init_socket())
        #

    def test_initSocket(self):
        self.assertIsInstance(hammer.init_socket(), socket.socket)

    def test_get(self):
        self.assertIn("GET / HTTP/1", hammer.get("nginx").split('\n')[0])  # Assert GET nginx
        self.assertRegex(hammer.get("nginx").split('\n')[1], "Host\:\ \w+\.(\.?\w+)*")  # Assert valid Hostname
        for i, line in enumerate(hammer.get("nginx").split("\n")):
            try:
                self.assertEqual(line[-1].encode("ascii"), b'\r')
            except IndexError as e:
                pass
        self.assertEqual(hammer.get("nginx")[-4:], "\r\n\r\n")

        self.assertIn("GET / HTTP/1", hammer.get("apache2").split('\n')[0])  # Assert GET apache2
        self.assertRegex(hammer.get("apache2").split('\n')[1], "Host\:\ \w+\.(\.?\w+)*")  # Assert valid Hostname
        for i, line in enumerate(hammer.get("apache2").split("\n")):
            try:
                self.assertEqual(line[-1], '\r')
            except IndexError as e:
                pass
        self.assertEqual(hammer.get("apache2")[-4:], "\r\n\r\n")

        self.assertFalse(hammer.get("ANYTHING-ELSE"))


    def test_post(self):
        post = hammer.post()
        self.assertIn("POST / HTTP/1", post)
        self.assertRegex(post, "Host\:\ \w+\.(\.?\w+)*")
        self.assertIn("Content-Length:", post)

        payload = "haha test this is test, x=0&y=12"
        post = hammer.post(payload)
        content_length = int(
            post[post.index("-Length: ") + len("-Length: "): post.index("-Length: ") + len("-Length: ") + 5:])
        self.assertEqual(len(payload), content_length)

        self.assertEqual(hammer.post()[-2:], "\r\n")

if __name__ == "__main__":
    unittest.main()
