class Pbar:
    def __init__(self, display):
        self.show = display

    def create(self, message, max_bar):
        if self.show:
            from progressbar import *
        else:
            return
        widgets = ['Progress: ', Percentage(), ' ',
                   Bar(marker=RotatingMarker())]
        print(message)
        self.bar = ProgressBar(widgets=widgets, maxval=max_bar).start()
        self.max = max_bar

    def update(self, cnt):
        if not self.show:
            return
        if cnt > self.max:
            return

        self.bar.update(cnt)

    def finish(self):
        if not self.show:
            return
        self.bar.finish()
