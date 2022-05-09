from django.shortcuts import render
from googletrans import Translator
import googletrans
 
#googletrans.LANGUAGES
 
# text1 = "Have a nice day"
  
# translator = Translator()
# print(translator.detect(text1))

# trans1 = translator.translate(text1, src='ko', dest='en') 
   


def index(req):
    context = {
        "nd" : googletrans.LANGUAGES
    }
    if req.method == "POST":
        b = req.POST.get("bf")
        f = req.POST.get("fr")
        t = req.POST.get("to")
        trans = Translator()
        af = trans.translate(b, src=f , dest=t)
        context.update({
            "af" : af.text,
            "b" : b,
            "fr": f,
            "to": t,

        })
    return render(req, 'trans/index.html', context)

