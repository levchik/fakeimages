# Fake images
----------
Fake images is an open-source Apache2 Licensed HTTP library, written in pure Python, that allows you to get "dummy" images from the server and do whatever the heck you want with them: send to response of your web server or even save on your hard drive (yes, it has Pillow!). You can also set up your own server of fake images and connect to it.

It is built on top of excellent Requests library and it also has tests and follows PEP8! Please feel free to contribute, write tests for untested features, send pull requests and all that good stuff. If you've committed, feel free to include your name in contributors list. History and roadmap are also available below.

Yes, you can install via pip:

    pip install fakeimages

### Example of usage

#### Save an image to hard drive
    from fakeimages import FakeImage
    fake_image = FakeImage(300)
    fake_image.save('test.png') # You'll get fakeimage with 300x300 size


#### Send it straight to response (Tornado example)
    from fakeimages import FakeImage
    from tornado import web

    class TestHandler(web.RequestHandler)
        def get(self):
            fake_image = FakeImage(300)
            self.set_header('Content-Type', 'image/png')
            self.write(fake_image.content)


#### Shuffle image parameters and get new image
    from fakeimages import FakeImage
    fake_image = FakeImage(width=300, text='Hello world', retina=True) # Get retina image
    fake_image.save(path='hello_world_retina.png', format='png') # Save it as png
    fake_image.retina = False
    fake_image.get() # Now get non retina message from server
    fake_image.save(path='hello_world_non_retina.jpg', format='jpg') # Save it as jpg


#### You can also receive response only with get()
    from fakeimages import FakeImage
    fake_image = FakeImage(300)
    fake_image.save('../300.png')
    fake_image.get(width=500, font_size=18)
    fake_image.save('../500.png')

### Useful links

[ROADMAP](ROADMAP.md)
[HISTORY](HISTORY.md)
[LICENSE](LICENSE)

