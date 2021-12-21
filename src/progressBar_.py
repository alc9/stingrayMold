import progressbar
#source: https://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage
class appProgressBar:
    def __init__(self):
        self.bar = progressbar.ProgressBar(maxval=100, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
