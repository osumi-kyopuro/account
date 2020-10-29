from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .forms import AttendForm
from builtins import str
from _datetime import timezone
from django.utils import timezone
from django.db.models import F, Q
from django.conf.locale import ja
from django.shortcuts import redirect, render
from django import forms
from .models import Attendance
#import .models

# Create your views here.
def list_check(request):#データ整合チェック
    from .models import Attendance
    time_series_flag=True
    data_alignment_flag=True
    time_over_flag=True
    if Attendance.objects.filter(scheduled_attend_time__gt=F('scheduled_leave_time')).exists():
        time_series_flag=False
        Attendance.objects.filter(scheduled_attend_time__gt=F('scheduled_leave_time')).delete()
    check_record=Attendance.objects.all()
    for i in range(Attendance.objects.count()):
        if Attendance.objects.count() <= i:
            break
        if check_record[i].attend_time!=None and check_record[i].leave_time!=None:
            check_record[i].work_time = check_record[i].leave_time - check_record[i].attend_time
        check_record[i].save()
        if check_record[i].scheduled_leave_time - check_record[i].scheduled_attend_time >= timedelta(days=1):
            time_over_flag=False
        check = Attendance.objects.filter(Q(user=check_record[i].user), Q(scheduled_attend_time__range=(check_record[i].scheduled_attend_time-timedelta(minutes=30),check_record[i].scheduled_leave_time+timedelta(minutes=30)))|Q(scheduled_leave_time__range=(check_record[i].scheduled_attend_time-timedelta(minutes=30),check_record[i].scheduled_leave_time+timedelta(minutes=30)))|Q(scheduled_attend_time__lte=check_record[i].scheduled_attend_time,scheduled_leave_time__gte=check_record[i].scheduled_leave_time))
        if check.count() > 1:
            data_alignment_flag=False
            for j in range(check.count()):
                if check.count() <= j:
                    break
                check[check.count()-1].delete()

    
    data = Attendance.objects.all()
    params = {  'message': 'データ一覧', 
                'data': data,#データ整合完了データ
                'time_series_flag' :time_series_flag,
                'time_over_flag' :time_over_flag,
                'data_alignment_flag':data_alignment_flag
            }
    return render(request, 'attendance2/list.html', params)
def shift_addition_menu(request):#シフト追加メニュー
    from .models import Attendance
    return render(request, 'attendance2/shift_addition_menu.html')

def add_shift(request):#シフト1件追加
    from .models import Attendance
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        form = AttendForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_check')#データ整合チェック
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form
    else:
        params['form'] = AttendForm()
    return render(request, 'attendance2/add_shift.html', params)

from django.forms.models import modelformset_factory
from django.db import transaction
 
def add_manyshift(request):#シフト複数件追加
    # フォームセット定義
    # modelformset_factoryを使う。
    # modelformじゃない時はforms.formset_factory
    MyFormSet= modelformset_factory(
        model=Attendance,
        form=AttendForm,
        extra=5, # セットの表示数 defaultは1
        max_num=5, # 最大表示数 defaultは1
    )
 
    if request.method == 'GET' :
        # フォームの初期値を指定する場合
        #form_initial = [{
        #    'field_1' : 'initial_value_1',
        #    'field_2' : 'initial_value_2',
        #}]
        # フォームセットのオブジェクト生成
        form_set = MyFormSet(
            #initial=form_initial,
            # 新規作成フォームのみ表示(既存レコードは表示しない)
            queryset=Attendance.objects.none()
        )
    else : # POST
        form_set = MyFormSet(request.POST)
        if form_set.is_valid() :
            posts = form_set.save(commit=False)
            # 保存処理
            with transaction.atomic() :
                # 各々save(m2mってのもあるらしいが試してない)
                for p in posts :
                    # 他のフォームを併設している場合、そこでsaveしたレコードのPKを使う場合はobject.pkでとれる
                    #p.parent_pk = other_post.pk
                    p.save()
 
            #messages.info(request, f'保存しました。')
            return redirect('list_check')
 
    # レンダリング
    context = {
        'form_set': form_set,
    }
    return render(request, 'attendance2/add_manyshift.html', context)




def sortlist(request):#データ時系列順
    from .models import Attendance
    from django.db.models import Sum
    data = Attendance.objects.order_by("scheduled_attend_time")
    sort_flag=True
    params = {  'message': 'データ一覧', 
                'data': data,
                'sort_flag':sort_flag,
                'title':'全体のシフトデータ(時系列順)'
            }
    return render(request, 'attendance2/list.html', params)
 
 
def list(request):#データ登録順
    from .models import Attendance
    data = Attendance.objects.all()
    params = {  'message': 'データ一覧', 
                'data': data,
                'title':'全体のシフトデータ(登録順)'
            }
    return render(request, 'attendance2/list.html', params)


from django.shortcuts import (
        render,
        redirect,
        get_object_or_404,
    )
from django.views.decorators.http import require_POST  # 追加する
from .models import Attendance
from .forms import AttendForm
def delete_menu(request):#データ削除メニュー
    from .models import Attendance
    data = Attendance.objects.all()
    params = {'message': 'データ一覧', 'data': data}
    return render(request, 'attendance2/delete_menu.html', params)
    
@require_POST
def delete(request):#データ削除関数
    delete_ids = request.POST.getlist('delete')
    if delete_ids:    
        Attendance.objects.filter(id__in=delete_ids).delete()
    return redirect('list')
    




def user_search(request):#user検索機能
    from .models import Attendance
    from .forms import AttendForm
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        form = AttendForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personal_list')#データ整合チェック
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form
    else:
        params['form'] = AttendForm()
    return render(request, 'attendance2/user_search.html', params)

@require_POST
def personal_list(request):#個人シフトデータ
    from .models import Attendance
    from django.db.models import Sum
    if request.method == 'POST':
        form = AttendForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('user')#ユーザー名
            user_data=Attendance.objects.filter(Q(user=username))
            data = user_data.order_by("scheduled_attend_time")
            absence_count=user_data.filter(attend_time=None ,leave_time=None,scheduled_leave_time__lt= datetime.now()).count()
            late_count = user_data.filter(attend_time__gt = F('scheduled_attend_time')).count()
            early_count = user_data.filter(leave_time__lt=F('scheduled_leave_time')).count()
            sum = data.aggregate(Sum('work_time'))
            params = {  'message': 'データ一覧', #メッセージ
                        'data': data,#自分のシフトデータ
                        'sum':sum,#総労働時間
                        'user':username,#ログインユーザー名
                        'absence_count':absence_count,#欠席回数
                        'late_count':late_count,#遅刻回数
                        'early_count':early_count#早退回数
                    }
            return render(request, 'attendance2/mylist.html', params)
        else :
            return render(request, 'attendance2/mylist.html')





def mylist(request):#自分のシフトデータ
    from .models import Attendance
    from django.db.models import Sum
    data = Attendance.objects.filter(user=request.user).order_by("scheduled_attend_time")
    absence_count=Attendance.objects.filter(user=request.user,attend_time=None ,leave_time=None,scheduled_leave_time__lt= datetime.now()).count()
    late_count = Attendance.objects.filter(user=request.user,attend_time__gt = F('scheduled_attend_time')).count()
    early_count = Attendance.objects.filter(user=request.user,leave_time__lt=F('scheduled_leave_time')).count()
    sum = data.aggregate(Sum('work_time'))
    params = {  'message': 'データ一覧', #メッセージ
                'data': data,#自分のシフトデータ
                'sum':sum,#総労働時間
                'user':request.user,#ログインユーザー名
                'absence_count':absence_count,#欠席回数
                'late_count':late_count,#遅刻回数
                'early_count':early_count#早退回数
            }
    return render(request, 'attendance2/mylist.html', params)



    
def attend_time(request):#出勤
    from .models import Attendance
    data=Attendance.objects.get(Q(user=request.user),Q(scheduled_attend_time__lt=datetime.now()+timedelta(minutes=30)),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None),Q(leave_time=None))
    data.attend_time = timezone.now()
    if data.attend_time > data.scheduled_attend_time:
        data.late=True
    data.save()
    params = {  'message': request.user,#アカウントユーザー名
                'attend_time':datetime.now().strftime('%H:%M:%S')#出勤時刻
            }
    return render(request, 'attendance2/attend_time.html',params)


 

def leave_time(request):#退勤
    from .models import Attendance
    data=Attendance.objects.get(Q(user=request.user),Q(leave_time=None),Q(attend_time__isnull=False))
    data.leave_time = timezone.now()
    if data.leave_time < data.scheduled_leave_time:
        data.early=True
    data.work_time=data.leave_time - data.attend_time
    data.save()
    params = {  'message': request.user,#アカウントユーザー名
                'leave_time':datetime.now().strftime('%H:%M:%S'),#退勤時刻
                'work_time':data.work_time#労働時間
            }
    return render(request, 'attendance2/leave_time.html',params)

def home(request):#TOPページ
    from .models import Attendance
    params = {'message': str(request.user)}
    #現在時刻が出勤予定時刻から30分以内であり、出勤も退勤もしていない時
    if Attendance.objects.filter(Q(user=request.user),Q(scheduled_attend_time__lt=datetime.now()+timedelta(minutes=30)),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None),Q(leave_time=None)).exists():
        #シフトデータがある時
        if Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).exists():
            data=Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).earliest('scheduled_attend_time')
            params = {  'message': request.user,#アカウントユーザー名表示
                        'attend_flag':True,#出勤ボタン表示flag
                        'leave_flag':False,#退勤ボタン表示flag
                        'data_flag':True,#データ存在flag
                        'data':data#次のシフト表示
                    }
        #シフトデータがない時
        else:
            params = {  'message': request.user,
                        'attend_flag':True,
                        'leave_flag':False,
                        'data_flag':False
                    }
    #出勤している時
    elif Attendance.objects.filter(Q(user=request.user),Q(leave_time=None),Q(attend_time__isnull=False)).exists():
        #シフトデータがある時
        if Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).exists():
            data=Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).earliest('scheduled_attend_time')
            params = {  'message': request.user,
                        'attend_flag':False,
                        'leave_flag':True,
                        'data_flag':True,
                        'data':data
                    }
        #シフトデータがない時
        else:
            params = {  'message': request.user,
                        'attend_flag':False,
                        'leave_flag':True,
                        'data_flag':False
                    }
    #退勤したか欠勤した時
    elif Attendance.objects.filter(user=request.user,scheduled_leave_time__gt=datetime.now()).exists():
        #シフトデータがある時
        if Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).exists():
            data=Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).earliest('scheduled_attend_time')
            params = {  'message': request.user,
                        'attend_flag':False,
                        'leave_flag':False,
                        'data_flag':True,
                        'data':data
                    }
        #シフトデータがない時
        else:
            params = {  'message': request.user,
                        'attend_flag':False,
                        'leave_flag':False,
                        'data_flag':False
                    }
    #シフトデータがない場合
    else:
        params = {  'message': request.user,
                    'attend_flag':False,
                    'leave_flag':False,
                    'data_flag':False
                }
    return render(request, 'attendance2/home.html',params)

