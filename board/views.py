from django.shortcuts import redirect, render
from .models import Board,Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
# 페이징 기능 구현====================================================================
def index(req):
    pg = req.GET.get("page", 1)
    b = Board.objects.all()

    cate = req.GET.get("cate","")
    ss = req.GET.get("ss","")  

    if ss:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=ss)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=ss)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none() #아무것도 없는 레코드 설정할때

        elif cate == "con":
            b = Board.objects.filter(content__contains=ss)
        else:
            b = Board.objects.all()
    else:
        b = Board.objects.all()
    
    b = b.order_by('-pubdate')
    
    pag = Paginator(b,5)
    obj = pag.get_page(pg)

    context = {
        "bset" : obj,
        "ss" : ss,
        "cate" : cate,

    }
    return render(req, "board/index.html", context)
#CRUD=================================================================================
 
def detail(req,bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context ={
        "b" : b,
        "rset" : r
    }
    return render(req, "board/detail.html", context)

def delete(req,bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == req.user:
        b.delete()
    else:    # hacking
        messages.error(req, "Invalid connection")
    return redirect("board:index")


def create(req):
    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        Board(subject=s, writer=req.user, content=c, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(req, "board/create.html")

def update(req,bpk):
    b = Board.objects.get(id=bpk)

    if b.writer != req.user:
        pass
        return redirect("board:index")

    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        b.subject = s
        b.content = c
        b.save()
        return redirect("board:index")
    context ={
        "b":b
    }    
    return render(req, "board/update.html",context)

# 댓글기능 구현=====================================================================
def creply(req,bpk):
    b = Board.objects.get(id=bpk)
    c = req.POST.get('com')
    Reply(board=b,replyer=req.user,comment=c).save()

    return redirect("board:detail",bpk)



def dreply(req,bpk,rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == req.user:    
        r.delete()
    else:
        messages.error(req, "Invalid connection")
    return redirect("board:detail",bpk)


def likey(req,bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(req.user)
    
    return redirect("board:detail",bpk)

def unlikey(req,bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(req.user)

    return redirect("board:detail",bpk)


