# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
from ..users.models import User
from .forms import PinForm, BoardForm, TopicForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'pinterest/index.html')


def pin_index(request):
    current_user = User.objects.get(email=request.session['email'])
    pins = Pin.objects.exclude(Q(created_by=current_user) | Q(saved_by=current_user))
    context = {
        'pins': pins
    }
    return render(request, 'pinterest/pin_index.html', context)


def create_pin(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.session['email'])
            topic = Topic.objects.get(id=request.POST['topic'])
        except Exception as problem:
            return redirect('/')
        data = {}
        data['title'] = request.POST['title']
        data['description'] = request.POST['description']
        data['image'] = request.FILES['image']
        data['topic'] = [topic]
        data['created_by'] = user
        form = PinForm(data)
        print form
        new_pin = form.save(commit=False)
        new_pin.image = request.FILES['image']
        new_pin.created_by = user
        new_pin.save()
        return redirect(reverse('pinterest:user_show'))
    elif request.method == "GET":
        form = PinForm()
        topicForm = TopicForm()
        context = {
            'form': form,
            'topicForm': topicForm
        }
        return render(request, 'pinterest/create_pin.html', context)


def show_pin(request, id):
    try:
        pin = Pin.objects.find(id=id)
    except Exception as problem:
        return redirect('/')
    context = {
        'pin': pin
    }
    return render(request, 'pinterest/show_pin.html', context)


def edit_pin(request, id):
    try:
        pin = Pin.objects.find(id=id)
        context = {
            'pin': pin
        }
    except Exception as problem:
        return redirect('/')
    if request.method == "POST":
        return redirect('/')
    elif request.method == "GET":
        return render(request, 'pinterest/edit_pin.html', context)


def unpin(request, id):
  
    pin = Pin.objects.get(id=id)
    current_user = User.objects.get(email=request.session['email'])

    # if the user is the one who created the pin, then delete it from pinterest
    if current_user == pin.created_by:
        pin.delete()
    else: # remove it from the saved pins list
        current_user.pins_saved.remove(pin)
    user_pins = Pin.objects.filter(Q(created_by=current_user) | Q(saved_by=current_user))
    context = {
        'pins':user_pins
    }
    return render(request, 'pinterest/switch_pin.html', context)

def user_show(request):
   
    current_user = User.objects.filter(email=request.session['email'])
    following = current_user[0].following.all()
    following_num = len(following)
    
    followers = current_user[0].followers.all()
    followers_num = len(followers)

    pin_form = PinForm()
    board_form = BoardForm()

    user_pins = Pin.objects.filter(Q(created_by=current_user[0]) | Q(saved_by=current_user[0]))
    
    context = {
        'user': current_user[0],
        'follower': followers_num,
        'following': following_num,
        'pin_form': pin_form,
        'board_form': board_form,
        'pins': user_pins

    }
    return render(request, 'pinterest/user_show.html', context)

def logout(request):
    
    del request.session['username']
    del request.session['email']
    return redirect(reverse('users:greeting'))

def show_user_pins(request):
    
    user_pins = Pin.objects.filter(Q(created_by=User.objects.get(email=request.session['email'])) | Q(saved_by=User.objects.get(email=request.session['email'])))
    context = {
        'pins': user_pins
    }
    return render(request, 'pinterest/user_pin.html', context)

def create_topic(request):
    if request.method == 'POST':
        print "CREATING A TOPIC BABY"
        Topic.objects.create(name=request.POST['name'])
        return redirect(request.META.get('HTTP_REFERER', '/'))

def board_index(request):
    user_boards = Board.objects.filter(created_by=User.objects.get(email=request.session['email']))
    context = {
        'boards': user_boards
    }
    return render(request, 'pinterest/board_index.html', context)

def show_another_user_boards(request, id):
    show_user = User.objects.get(id=id)
    user_boards = Board.objects.filter(created_by=show_user)
    num_pin_in_boards = {}
    for board in user_boards:
        num_pin_in_boards[board.id] = len(board.pins.all())
        print('num pin -------', num_pin_in_boards[board.id])
    
    context = {
        'another_user': show_user,
        'another_user_boards': user_boards,
        'num_pin': num_pin_in_boards
    }

    return render(request, 'pinterest/another_user_boards.html', context)

def view_board(reqeust, id):
    pass

def create_board(request):
    
    if request.method == "POST":
            try:
                user = User.objects.get(email=request.session['email'])
                topic = Topic.objects.get(id=request.POST['topic'])
            except Exception as problem:
                return redirect('/')
            try:
                topic = Topic.objects.get(name=request.POST['topic'])
            except:
                topic = Topic.objects.create(name=request.POST['topic'])
            data = {}
            data['title'] = request.POST['title']
            data['description'] = request.POST['description']
            data['created_by'] = user
            data['topic'] = [topic]
            form = BoardForm(data)
            new_board = form.save(commit=False)
            new_board.created_by = user
            new_board.save()
            return redirect(reverse('pinterest:user_show'))
    elif request.method == "GET":
        form = BoardForm()
        context = {
            'form': form
        }
        return render(request, 'pinterest/create_board.html', context)

# def show_board(request):
def show_board(request, id):
    user_boards = Board.objects.filter(created_by=User.objects.get(id=id))
    num_pin_in_boards = {}
    for board in user_boards:
        num_pin_in_boards[board.id] = len(board.pins.all())
        print('num pin -------', num_pin_in_boards[board.id])
    # pin_in_boards = {}
    # for board in user_boards:
    #     pin_in_boards[board.id] = Pin.objects.filter(boards=board)[0]
    #     print('###show board ###', Pin.objects.filter(boards=board))
    #     print(pin_in_boards[board.id])
    context = {
        'boards': user_boards,
        # 'board_pins': pin_in_boards
        'num_pin': num_pin_in_boards
    }

    return render(request, 'pinterest/show_board.html', context)


def edit_board(request, id):
    selected_board = Board.objects.get(id=id)
    board_pins = Pin.objects.filter(boards=selected_board)
    current_user = User.objects.get(email=request.session['email'])
    user_pins = Pin.objects.filter(Q(created_by=current_user) | Q(saved_by=current_user)).exclude(boards=selected_board)
    context = {
        'pins': board_pins,
        'all_pins': user_pins,
        'board': selected_board
    }

    return render(request, 'pinterest/edit_board.html', context)

def board_add_pin(request, id):
    selected_pins = request.POST
    print('----selected pins-----', selected_pins)
    edited_board = Board.objects.get(id=id)
    for key in selected_pins:
        if key != 'csrfmiddlewaretoken':
            print('----key-----',key)
            edited_board.pins.add(Pin.objects.get(id=key))
    
    return redirect(reverse('pinterest:edit_board', kwargs={'id': id}))



def unpin_from_board(request, id, board_id):
    selected_pin = Pin.objects.get(id=id)
    selected_board = Board.objects.get(id=board_id)
    selected_board.pins.remove(selected_pin)
    selected_board.save()
    remaining_pins = selected_board.pins.all()
    context = {
        'pins': remaining_pins,
        'board': selected_board
    }

    return render(request, 'pinterest/board_pins.html', context)
    
# def delete_board(request):

def search(request):
    if 'search_bar' in request.POST:
        search_term = request.POST.get('search_bar')
        if search_term == "":
            searched_pin = Pin.objects.exclude(created_by=User.objects.get(email=request.session['email']))
            context = {
                'pins': searched_pin
            }
            return render(request, 'pinterest/search_result.html', context)
        current_user = User.objects.get(email=request.session['email'])
        searched_pin = Pin.objects.filter(Q(title__contains=search_term) | Q(description__contains=search_term)).exclude(Q(created_by=current_user) | Q(saved_by=current_user))
        context = {
            'pins': searched_pin
        }
        return render(request, 'pinterest/search_result.html', context)
    elif 'search_user' in request.POST:
        search_term = request.POST.get('search_user')
        if search_term == "":
            searched_user = User.objects.filter(name=search_term)
            context = {
                'users': searched_user
            }
            return render(request, 'pinterest/search_result.html', context)
        searched_user = User.objects.filter(Q(name__startswith=search_term) | Q(email__startswith=search_term))
        print(searched_user)
        context = {
            'users': searched_user
        }
        return render(request, 'pinterest/search_result.html', context)
    else:
        search_term = request.POST.get('search_board')
        if search_term == "":
            searched_board = Board.objects.filter(title=search_term)
            context = {
                'boards': searched_user
            }
            return render(request, 'pinterest/search_result.html', context)
        searched_boards = Board.objects.filter(Q(title__startswith=search_term) | Q(topic__startswith=search_term))
        context = {
            'boards': searched_user
        }
        return render(request, 'pinterest/search_result.html', context)

def user_show_info(request, id):
    current_user = User.objects.get(email=request.session['email'])
    show_user = User.objects.get(id=id)

    following = show_user.following.all()
    following_num = len(following)
    followers = show_user.followers.all()
    followers_num = len(followers)

    followed = False
    if current_user in show_user.followers.all():
        followed = True
    context = {
        'show_user': show_user,
        'current_user': current_user,
        'follower': followers_num,
        'following': following_num,
        "followed": followed
    }
    print('------Follower List-----------')
    print(show_user.followers.all())
    print(followed)
    return render(request, 'pinterest/user_info.html', context)

def add_pin(request, id):
    current_user = User.objects.get(email=request.session['email'])
    print('#############################',id)
    current_user.pins_saved.add(Pin.objects.get(id=id))
    current_user.save()
    return redirect(reverse('pinterest:user_show'))

def follow(request, id):
    current_user = User.objects.get(email=request.session['email'])
    current_user.following.add(User.objects.get(id=id))
    current_user.save()
    return redirect(reverse('pinterest:user_show'))
def unfollow(request, id):
    current_user = User.objects.get(email=request.session['email'])
    current_user.following.remove(User.objects.get(id=id))
    current_user.save()
    return redirect(reverse('pinterest:user_show'))

def show_another_user_pins(request, id):
    current_user = User.objects.get(email=request.session['email'])
    another_user = User.objects.get(id=id)
    another_user_pins = Pin.objects.filter(Q(created_by=another_user) | Q(saved_by=another_user)).exclude(Q(saved_by=current_user) | Q(created_by=current_user))

    context = {  
        'another_user_pins': another_user_pins,
        'another_user': another_user
    }
    return render(request, 'pinterest/user_pin.html', context)

def show_pin(request, id):
    pin = Pin.objects.get(id=id)
    created_user = pin.created_by
    saved_by = len(pin.saved_by.all())

    popular = False
    if saved_by > 1:
        popular = True

    comments = PinComment.objects.filter(pin=pin)
    context = {
        'pin': pin,
        'created_user': created_user,
        'saved_by': saved_by,
        'popular': popular,
        'comments': comments
    }
    return render(request, 'pinterest/show_pin.html', context)

def create_comment(request):
    print(request.POST, "=======post=======")
    comment = request.POST.get('comment')
    print('commet', comment)
    print('pin-id', request.POST.get('pin-id'))
    pin_id = int(request.POST.get('pin-id'))
    current_pin = Pin.objects.get(id=pin_id)
    current_user = User.objects.get(email=request.session['email'])
    new_comment = PinComment.objects.create(comment=comment, author=current_user, pin=current_pin)
    new_comment.save()
    # current_user_comments = PinComment.objects.filter(Q(authour=current_user) & Q(pin=current_pin))

    context = {
        'comment': new_comment
    }
    # return redirect(reverse('pinterest:show_pin', kwargs={'id':current_pin.id}))
    return render(request, 'pinterest/comment.html', context)

def delete_comment(request, id, pin_id):
    
    print(pin_id, '----------pin_id')
    PinComment.objects.get(id=id).delete()
    comments = PinComment.objects.filter(pin=Pin.objects.get(id=pin_id))
    
    delete_comment = True

    context = {
        'delete_comment': delete_comment,
        'comments': comments
    }

    return render(request, 'pinterest/comment.html', context)

def switch_to_pin(request):
    
    current_user = User.objects.filter(email=request.session['email'])
    user_pins = Pin.objects.filter(Q(created_by=current_user[0]) | Q(saved_by=current_user[0]))

    context = {
        'pins':user_pins
    }

    return render(request, 'pinterest/switch_pin.html', context)