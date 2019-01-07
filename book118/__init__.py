from book118.core import book118
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def getPDF(pid):
    pdf = book118(pid)
    pdf.getPDF()
